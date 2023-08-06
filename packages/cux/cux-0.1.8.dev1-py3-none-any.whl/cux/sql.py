#!/usr/bin/env python
import os
import random
import re
import sys
from cux.jupytersql import JupyterSQL
from contextlib import contextmanager
from typing import List, Tuple

import codefast as cf
import pymysql
from sshtunnel import SSHTunnelForwarder

from .config import AI_PROCESS_DEMO, INTELLIGENCE_DEMO, SQL_CONFIG


class SQLClient:
    def __init__(self) -> None:
        ...

    @contextmanager
    def _tunnel(self, sql_command: str):
        with SSHTunnelForwarder(
            ssh_address_or_host=(SQL_CONFIG["ip"], 22),  # ssh 目标服务器 ip 和 port
            ssh_username=SQL_CONFIG["username"],  # ssh 目标服务器用户名
            # ssh_pkey=SQL_CONFIG['ssh_pkey'],     # ssh 目标服务器证书
            ssh_password=SQL_CONFIG["ssh_password"],
            remote_bind_address=(SQL_CONFIG["sql_ip"], 3307),  # mysql 服务ip 和 part
            local_bind_address=(
                "127.0.0.1",
                5143,
            ),  # ssh 目标服务器的用于连接 mysql 或 redis 的端口，该 ip 必须为 127.0.0.1
            allow_agent=False,
        ) as server:
            conn = pymysql.connect(
                host=server.local_bind_host,
                port=server.local_bind_port,
                user=SQL_CONFIG["app_username"],
                password=SQL_CONFIG["app_password"],
                db="megaview_db",
                charset="utf8",
            )
            cursor = conn.cursor()
            cursor.execute(sql_command)
            yield cursor.fetchall()
            cursor.close()


class Organizations:
    @classmethod
    def load(cls) -> dict:
        """ load organization id to name dict """
        from cux.data import MEGAVIEW_ORGANIZATIONS

        return MEGAVIEW_ORGANIZATIONS
        # app = SQLClient()
        # organizations = {}
        # with app._tunnel('select * from megaview_db.organization;') as data:
        #     for ln in data:
        #         organizations[str(ln[0])] = ln[1]
        # return organizations


class config:
    APP_PREFIX = "https://megaview.oss-cn-zhangjiakou.aliyuncs.com"
    APP_ORGANIZATION = Organizations.load()


class TranscriptionTable:
    def __init__(self, tple) -> None:
        (
            self.id,
            self.conversation_id,
            _,
            self.nsq_task_id,
            self.audio_file_path,
            self.trans_file_path,
            self.create_time,
            self.udpate_time,
            self.organization_id,
            self.modified,
        ) = tple
        self.single_file_path = f"{config.APP_PREFIX}/single/{self.organization_id}_{self.conversation_id}.json"
        # self.trans_file_path = config.APP_PREFIX + self.trans_file_path
        self.audio_file_path = config.APP_PREFIX + self.audio_file_path
        self.company = config.APP_ORGANIZATION[str(self.organization_id)]
        self.trans_file_path = config.APP_PREFIX + "/single/{}_{}.json".format(
            self.organization_id, self.conversation_id
        )

    def __repr__(self) -> str:
        return "\n".join(f" {k:<20} {v}" for k, v in self.__dict__.items())


class AIProcessTable:
    """AI process table display"""

    def __init__(self, tple, env: str = "dev") -> None:
        assert len(tple) == len(AI_PROCESS_DEMO), "Found inquivalent length"
        self.__dict__.update(zip(AI_PROCESS_DEMO, tple))
        _prefix = SQL_CONFIG[f"{env}_oss_prefix"]
        _oid = self.organization_id
        _cid = self.conversation_id
        self.single_file_path = f"{_prefix}/single/{_oid}_{_cid}.json"

    def __repr__(self) -> str:
        return "\n".join(f"{k:<30} {v}" for k, v in self.__dict__.items())


class IntelligenceTable:
    """Intelligence table display"""

    def __init__(self, tple, env: str = "dev") -> None:
        assert len(tple) == len(INTELLIGENCE_DEMO), "Found inquivalent length"
        self.__dict__.update(zip(INTELLIGENCE_DEMO, tple))

    def __repr__(self) -> str:
        return "\n".join(f"{k:<30} {v}" for k, v in self.__dict__.items())


class AppSlave:
    def __init__(self) -> None:
        ...

    @contextmanager
    def _tunnel(self, sql_command: str):
        with SSHTunnelForwarder(
            ssh_address_or_host=(SQL_CONFIG["ip"], 22),  # ssh 目标服务器 ip 和 port
            ssh_username=SQL_CONFIG["username"],  # ssh 目标服务器用户名
            # ssh_pkey=SQL_CONFIG['ssh_pkey'],     # ssh 目标服务器证书
            ssh_password=SQL_CONFIG["ssh_password"],
            remote_bind_address=(SQL_CONFIG["sql_ip"], 3307),  # mysql 服务ip 和 part
            local_bind_address=("127.0.0.1", 5143),
            allow_agent=False,
        ) as server:
            conn = pymysql.connect(
                host=server.local_bind_host,
                port=server.local_bind_port,
                user=SQL_CONFIG["app_username"],
                password=SQL_CONFIG["app_password"],
                db="megaview_db",
                charset="utf8",
            )
            cursor = conn.cursor()
            cursor.execute(sql_command)
            yield cursor.fetchall()
            cursor.close()

    def ai_process(self, cid: int = 8, with_color=True) -> dict:

        cmd = "SELECT * FROM megaview_db.ai_process where conversation_id={};".format(
            str(cid)
        )
        ret = JupyterSQL(cmd).query()
        _infos = {}
        for k, v in zip(ret[0].split(","), ret[1].split(",")):
            if len(v) == 1:
                v = (
                    cf.fp.red(v, attrs=["bold"])
                    if v == "0"
                    else cf.fp.green(v, attrs=["bold"])
                ) if with_color else v
            print("{:<30} {:<20}".format(k, v))
            _infos[k] = v
        return _infos

    def incomplete_conversation(self) -> List[int]:
        sql = "SELECT conversation_id, update_at FROM megaview_db.ai_process\
            where (is_complete=0 or is_event_engine_complete=0) and single_file_path > '';"

        with self._tunnel(sql) as data:
            return data

    def transcription(self, cid: int = 8) -> dict:
        sql = "SELECT * FROM megaview_db.transcription where conversation_id={};".format(
            str(cid)
        )
        ret = JupyterSQL(sql).query()
        if len(ret) < 2:
            cf.info(ret)
            raise ValueError("Found no data from megaview_db.transcription table")
        return TranscriptionTable(ret[1].split(","))

    def ai_timeouted_cids(self) -> List[str]:
        """Get timeout AI precess conversation ids"""
        sql = "SELECT conversation_id, update_at FROM megaview_db.ai_process \
            WHERE (is_event_engine_complete=0 or is_complete=0) and single_file_path > '';"

        with self._tunnel(sql) as data:
            return data

    def exec_command(self, cmd) -> List[str]:
        with self._tunnel(cmd) as data:
            return data


# Base class for DEV / Test SQL commands


class SQLServer:
    def __init__(self, _host: str, _pass: str, _env: str) -> None:
        self._host = _host
        self._pass = _pass
        self._env = _env

    @contextmanager
    def connect(self, _host: str, _pass: str):
        yield pymysql.connect(host=_host, user="root", password=_pass, db="megaview_db")

    def execute(self, command: str) -> Tuple:
        with self.connect(self._host, self._pass) as conn:
            cur = conn.cursor()
            cur.execute(command)
            return cur.fetchall()

    def ai_info(self, conversation_id: int) -> dict:
        cmd = f"SELECT * FROM ai_process where conversation_id = {conversation_id};"
        sql_tuple = self.execute(cmd)
        if not sql_tuple:
            cf.info("SQL query return empty result.")
            return {}
        _info = AIProcessTable(sql_tuple[0], self._env)
        print(_info)
        return {}


class Dev(SQLServer):
    def __init__(
        self, _host: str = SQL_CONFIG["dev_ip"], _pass: str = SQL_CONFIG["dev_pass"]
    ) -> None:
        super(Dev, self).__init__(_host, _pass, "dev")


class Test(SQLServer):
    def __init__(
        self, _host: str = SQL_CONFIG["test_ip"], _pass: str = SQL_CONFIG["test_pass"]
    ) -> None:
        super(Test, self).__init__(_host, _pass, "test")


class ExtractTestConversation:
    def __init__(self) -> None:
        self.sql = Test()

    def sample(
        self, left: int = 0, right: int = 1 << 30, sample: int = 10
    ) -> List[int]:
        return random.sample(range(left, right), sample)
