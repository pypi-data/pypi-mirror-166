#!/usr/bin/env python
import datetime
import os
import sys

import arrow
import codefast as cf
import requests
from authc.myredis import get_redis
from codefast.argparser import ArgParser
from sshtunnel import DEFAULT_SSH_DIRECTORY

from cux.config import AI_PROCESS_DEMO
from cux.oss import AliyunOSS
from cux.redis import redis_cli
from cux.redo import BaseRedo
from cux.turbo import Env, Turbo

from .sql import (AppSlave, Dev, ExtractTestConversation, IntelligenceTable,
                  Test)

cf.logger.level = 'info'


def url_shortener(url: str) -> str:
    host = 'https://bitly.ddot.cc'
    host = 'http://47.105.143.5:5000/shorten'
    js = requests.post(host, json={'url': url}).json()
    return js['url'].replace('http', ' http')


def local_url_shortener(url: str) -> str:
    host = 'http://localhost:5000/shorten'
    js = requests.post(host, json={'url': url}).json()
    return js['url']


def display_intelligence_time_periods(cid: int = 54795):
    '''display intelligence time periods
    '''
    if len(sys.argv) >= 2:
        cid = sys.argv[1]
    cmd = f'SELECT * FROM megaview_db.wby_public_sentiment WHERE conversation_id = {cid}'
    CONV_URL = 'https://megaview.oss-cn-zhangjiakou.aliyuncs.com/single/21_{}.json'.format(
        cid)
    AppSlave().transcription(cid)
    dt = cf.js(CONV_URL)

    def format_time(time_str):
        return round(float(time_str) / 60, 2)

    for e in AppSlave().exec_command(cmd):
        item = IntelligenceTable(e)
        pieces = item.content.split('\n')
        for _line in pieces:
            _line = _line.strip('候选人:').strip('顾问:')
            if len(_line) < 5:
                continue
            matched = next((e for e in dt if e['content'] == _line), None)
            if matched:
                print(_line, '\n', format_time(matched['begin_time']), ' ~ ',
                      format_time(matched['end_time']))
                break


def check_intelligence_result():
    cmd = 'SELECT * FROM megaview_db.wby_public_sentiment ORDER BY create_at DESC LIMIT 100'
    CID_SET_NAME = 'intelligence'
    _text = ''
    for e in AppSlave().exec_command(cmd):
        item = IntelligenceTable(e)

        if not redis_cli.sismember(CID_SET_NAME, item.id):
            if item.status != 'review':
                continue
            redis_cli.sadd(CID_SET_NAME, item.id)
            _text += str(item.conversation_id) + item.content + str(
                item.predict_is_real)


class _RedisHelper(object):
    def __init__(self):
        self.cli = get_redis()

    def set(self, conversation_id: str) -> bool:
        if self.cli.exists(conversation_id):
            cf.warning('conversation_id: {} already RERUNED at {}'.format(
                conversation_id, self.cli.get(conversation_id)))
            return False
        else:
            self.cli.set(conversation_id, str(datetime.datetime.now()), ex=120)
            return True


def auto_redo(nearly_timeout: int = 1500):
    '''audo redo ai_process time out conversations'''
    res = AppSlave().ai_timeouted_cids()
    redo_ids = []
    for ln in res:
        _id, _date = ln
        _diff = arrow.now() - arrow.get(_date, 'Asia/Shanghai')
        _diff_seconds = _diff.seconds

        if _diff_seconds > nearly_timeout:
            cf.info(_date, _diff_seconds, _id)
            redo_ids.append(_id)

    if redo_ids:
        BaseRedo(Env.PRODUCT).redo_all(redo_ids)
        helper = _RedisHelper()
        for _id in redo_ids:
            helper.set(_id)
        msg = 'conversations rerun completed: [{}] '.format(','.join(
            map(str, redo_ids)))
        os.system(
            '/usr/bin/proxychains4 /home/gaoang/anaconda3/envs/dl/bin/sli -tgbot "{}"'
            .format(msg))


def gate():
    parser = ArgParser()
    parser.input('trans',
                 'transcription',
                 sub_args=[['id', 'conversation_id']],
                 description='Transcription info.')
    parser.input('ai', 'ai_process', description='AI process.')
    parser.input('cids',
                 'failed_conversation',
                 description='print out cids of failed conversation.')
    parser.input('dev', description='AI process.')
    parser.input('test', description='AI process.')
    parser.input('autoredo', description='Auto redo')
    parser.input('ossget', description='Get OSS files.')
    parser.input('ossput', description='Put OSS files.')
    parser.input('sql', description='Execute Jupyter MySQL command.')
    parser.input('sample',
                 sub_args=[['test', 't']],
                 description='sample conversation ids from SQL.')
    parser.input('pipe',
                 description='Donwload audio, transcription and upload again.')

    parser.input('nlpresult',
                 description='Get nlpresult url by conversation_id')

    parser.input('extract_event_input',
                 description='Extract event engine input from log')

    parser.parse()
    alioss = AliyunOSS()

    if parser.extract_event_input:
        import ast
        import re

        import rich
        s = cf.io.reads(parser.extract_event_input.value)
        r = re.search('event engine process, data: (.*), plugins', s)
        js = ast.literal_eval(r.group(1)) if r else {}
        print(js)
        cf.js.write(js, '/tmp/ee123.json')

    elif parser.nlpresult:
        cid = parser.nlpresult.value
        _path = 'nlpcache/' + '%X' % (1631149749 + int(cid)) + '-1.json'
        nlp_url = url_shortener(alioss.sign(_path))
        print('{:<20} {}'.format(' nlp path', nlp_url))

    elif parser.pipe:
        cid = parser.pipe.value
        obj = AppSlave().transcription(cid)
        print(obj)

        if not obj:
            cf.warning(
                'conversation_id: {} not found from database'.format(cid))
            return

        audio_path = obj.audio_file_path.split('com/')[1]
        text_path = obj.trans_file_path.split('com/')[1]
        audio_url = alioss.sign(audio_path)
        audio_url = url_shortener(audio_url)
        text_url = alioss.sign(text_path)
        text_url = url_shortener(text_url)
        print('{:<20} {}'.format(' public audio path', audio_url))
        print('{:<20} {}'.format(' public text path', text_url))
        print('-' * 80 + ' Audio information:')
        os.system('sli -fi "{}"'.format(audio_url))

    elif parser.sample:
        print('Usage jql -sample 23333 55555 10\n')
        left, right, num = 0, 10000, 10
        if len(sys.argv) >= 3:
            left, right, num = int(sys.argv[2]), int(sys.argv[3]), int(
                sys.argv[4])
        print(ExtractTestConversation().sample(left, right, num))

    if parser.ossget:
        AliyunOSS().download(parser.ossget.value)

    elif parser.ossput:
        cf.info(AliyunOSS().upload(parser.ossput.value, 'backend'))

    elif parser.transcription:
        AppSlave().transcription(parser.transcription.value)

    elif parser.cids:
        for d in AppSlave().incomplete_conversation():
            print(d[0], d[1].strftime("%Y-%m-%d %H:%M:%S"))

    elif parser.ai_process:
        AppSlave().ai_process(parser.ai_process.value)

    elif parser.autoredo:
        auto_redo()

    elif parser.dev:
        Dev().ai_info(parser.dev.value)

    elif parser.test:
        Test().ai_info(parser.test.value)

    elif parser.sql:
        from cux.jupytersql import JupyterSQL
        r_list = JupyterSQL(parser.sql.value).query()
        cf.io.write(r_list, '/tmp/sqlresult.csv')
        cf.info("Export result to /tmp/sqlresult.csv")
        BOUND = 10
        for r in r_list[:BOUND]:
            print(r)
        if len(r_list) >= BOUND:
            print('...')
