#!/usr/bin/env python
# -*- coding: utf-8 -*-
from codefast.betterargs import AbstractClient, Context
from enum import Enum, auto
import codefast as cf
import re
from cux.sql import ExtractTestConversation
from cux.turbo import Turbo, Env
from typing import List, Dict, Tuple, Any


class RedoType(Enum):
    CONVERSATION = auto()
    EVENT_ENGINE = auto()
    ALL = auto()


class AbstractRedoClass(object):
    def __init__(self, env_type: Env):
        self.env_type = env_type


class BaseRedo(AbstractRedoClass):
    def __init__(self, env_type: Env):
        self.env_type = env_type
        self.turbo_client = Turbo(self.env_type)

    def redo_conversation(self, cids: list):
        """Redo transcription for a list of conversations."""
        cf.info('Conversation redo list: {}'.format(cids))
        self.turbo_client.login()
        _url = self.turbo_client.url + '/api/megaview_display/conversation_redo/transcript'
        params = {'conversation_ids': cids, 'is_full_amount': 1}
        resp = self.turbo_client.session.post(
            _url,
            headers={'Cookie': f'turbo_session={self.turbo_client.token}'},
            data=params)
        cf.info(resp.json())
        return resp.json()

    def redo_event_engine(self, cids: List[int]):
        """Redo event engine for a list of conversations. 
        Full amount is set to 1.
        """
        cf.info('EventEngine redo list: {}'.format(cids))
        self.turbo_client.login()
        _url = self.turbo_client.url + '/api/megaview_display/conversation_redo/event_engine'
        params = {'conversation_ids': cids}
        resp = self.turbo_client.session.post(
            _url,
            headers={'Cookie': f'turbo_session={self.turbo_client.token}'},
            data=params)
        cf.info(resp.json())
        return resp.json()

    def redo_all(self, cids: list):
        """Redo event engine for a list of conversations. 
        Full amount is set to 1.
        """
        cf.info('ALL redo list: {}'.format(cids))
        self.turbo_client.login()
        _url = self.turbo_client.url + '/api/megaview_display/conversation_redo/redo'
        params = {'conversation_ids': cids}
        resp = self.turbo_client.session.post(
            _url,
            headers={'Cookie': f'turbo_session={self.turbo_client.token}'},
            data=params)
        cf.info(resp.json())
        return resp.json()

    def _strip_invalid_cids(self, func, cids):
        if not cids:
            cf.info('No conversation id left.')
            return

        msg = func(cids)['msg']
        if '部分会话无法进行重跑' in msg or '一些会话不存在或已删除' in msg:
            for failed_id in re.findall(r'(\d{5,7})', msg):
                failed_id = int(failed_id)
                if failed_id in cids:
                    cf.info('removing {} from redo list'.format(failed_id))
                    cids.remove(failed_id)
            self._strip_invalid_cids(func, cids)

    def random_redo(self, n: int, redo_type: RedoType):
        """randomly choose 'n' conversations from SQL """
        cids = ExtractTestConversation().sample(10000, 80000, n)
        if redo_type == RedoType.CONVERSATION:
            self._strip_invalid_cids(self.redo_conversation, cids)
        elif redo_type == RedoType.EVENT_ENGINE:
            self._strip_invalid_cids(self.redo_event_engine, cids)
        elif redo_type == RedoType.ALL:
            self._strip_invalid_cids(self.redo_all, cids)
        else:
            raise ValueError("invalid redo type")


class ClientCreator(AbstractClient):
    def __init__(self, env_type: Env):
        super().__init__()
        self.name = env_type.name
        self.subcommands = [['e', 'ee', 'event_engine'], ['rd', 'r', 'random', 'random_redo'],
                            ['c', 'conversation', 'conv'], ['all', 'a']]
        self.demos = {'event_engine': 'redo -t -e 123',
                      'random_redo': 'redo -t -c 123'}
        self.cli = BaseRedo(env_type)
        _help_message = '''Examples:
        redo -t -e 12345, to run event engine for conversation 123
        redo -t -c 12345, to run transcription for conversation 123
        redo -t -a 12345, to run both event engine and transcription for conversation 123
        redo -t -r 10 c, to randomly pick 10 conversations and run transcription for them
        redo -t -r 10 e, to randomly pick 10 conversations and run event engine for them'''
        self.description = 'redo {} data'.format(
            env_type.name)
        if env_type == Env.TEST:
            self.description += '\n' + _help_message

    def event_engine(self, cids: List[int]):
        self.cli.redo_event_engine(cids)

    def conversation(self, cids: List[int]):
        self.cli.redo_conversation(cids)

    def all(self, cids: List[int]):
        self.cli.redo_all(cids)

    def random_redo(self, xs: List[str]):
        """ Two args are needed:
        -n: number of conversation to redo
        -t: redo type, can be conversation, event_engine, all
        """
        n = int(xs[0])
        types_map = {'c': RedoType.CONVERSATION,
                     'e': RedoType.EVENT_ENGINE, 'a': RedoType.ALL}
        redo_type = types_map[xs[1].replace('-', '')[0].lower()]
        self.cli.random_redo(n, redo_type)


def entry():
    cxt = Context()
    cxt.add_command(['test', 't'], ClientCreator(Env.TEST))
    cxt.add_command(['pro', 'p', 'product'], ClientCreator(Env.PRODUCT))
    cxt.add_command(['dev', 'd', 'develop'], ClientCreator(Env.DEV))
    cxt.execute()
