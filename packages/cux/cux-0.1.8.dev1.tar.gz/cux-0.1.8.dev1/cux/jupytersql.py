#!/usr/bin/env python
import json
import time
import uuid
from threading import Thread
from typing import List

import codefast as cf
import pandas as pd
import pymysql
from authc import gunload
from authc.myredis import get_redis as scf
from pyserverless.apps.rabbitmq import Consumer, Publisher


class consts(object):
    amqp = type('AMQPClass', (object, ), {
        'url': gunload('amqp_url'),
        'queue_name': 'jupytersql',
    })
    CMD_LIST = "mysql_cmd_list"
    CMD_RESULT = "mysql_cmd_result"
    TMP_SQL_RESULT_FILE = "/tmp/sql_result.txt"
    REDIS_API_BIN = "/tmp/myredis-cli"


class JupyterSQL(object):
    """ MySQL can be exclusively accessed through jupyter server
    """

    def __init__(self, cmd: str = None) -> None:
        self.db = scf()     # eloop get_redis is actually get_redis_cn
        self.cmd = cmd
        self.amqp_url = consts.amqp.url
        assert self.amqp_url != '', "Invalid amqp url"
        self.publisher = Publisher(self.amqp_url, consts.amqp.queue_name)

    def exec(self, cmd: str) -> List[str]:
        """cmd demo:
            'select single_file_path, create_at from megaview_db.ai_process \
                where create_at > "2022-05-01" order by create_at desc limit 10;'
        """
        cf.info("cmd is: {}".format(cmd))
        cf.info("command issued, waiting for mysql result ...")
        task_id = str(uuid.uuid4())
        msg = {'task_id': task_id, 'cmd': cmd}

        self.publisher.post(json.dumps(msg).encode('utf-8'))
        cf.info('Task post to {}'.format(self.amqp_url))

        wait_time, period = 0, 0.1
        while wait_time <= 30:
            res = self.db.get(task_id)
            time.sleep(period)
            wait_time += period
            if res:
                return res.split('\n')
        return []

    def query(self) -> List[str]:
        if self.cmd is not None:
            return self.exec(self.cmd)
        return []


class JupyterClientDaemon(object):

    def __init__(self) -> None:
        self.consumer = Consumer(consts.amqp.url, consts.amqp.queue_name)
        self.db = scf()

    def execute_once(self, query_str) -> pd.DataFrame:
        conn = pymysql.connect(
            host="172.18.54.40",
            user="developer",
            passwd="Hq)%33K7HpJGHaavV",
            db="megaview_db",
            port=6447,
        )
        try:
            data = pd.read_sql_query(query_str, conn)
            data.to_csv(consts.TMP_SQL_RESULT_FILE, index=False)
            return data
        except Exception as e:
            cf.io.write(str(e), consts.TMP_SQL_RESULT_FILE)
            return str(e)

    def callback(self, ch, method, properties, body):
        msg = json.loads(body.decode())
        cf.info("[-] processing", msg)
        task_id = msg['task_id']
        cmd = msg['cmd']
        data = self.execute_once(cmd)
        if not isinstance(data, pd.DataFrame):
            cf.info("[-] data is not a dataframe")
            return []
        data.to_csv('/tmp/{}.csv'.format(task_id), index=False)
        js = cf.io.reads('/tmp/{}.csv'.format(task_id))
        resp = self.db.set(task_id, js)
        cf.info(resp.text[:100])
        cf.info("[-] data is ready")
        return js

    def eloop(self):
        self.consumer.consume(self.callback)


def tmp_cleaner():
    # clean /tmp/*.csv file every few minutes
    while True:
        for f in cf.io.walk('/tmp/'):
            if f.endswith('.csv'):
                cf.io.rm(f)
        cf.info("[-] cleaned")
        time.sleep(86400)


def eloop():
    try:
        Thread(target=tmp_cleaner).start()
        JupyterClientDaemon().eloop()
    except KeyboardInterrupt:
        cf.info("Exit")
