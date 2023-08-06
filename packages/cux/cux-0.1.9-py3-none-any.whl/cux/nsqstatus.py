#!/usr/bin/env python
import argparse
import datetime
from collections import defaultdict
import enum
import json
import signal
import subprocess
import sys
import time

import codefast as cf
from authc.myredis import rc


class ServerEnum(enum.Enum):
    TEST = "TEST"
    ALIAI = "AISERVER02"
    TENCENT = "TENCENT-AI2"


from typing import List


class Liner(object):
    def __init__(self,
                 topic_name: str,
                 channel_name: str,
                 channel_depth: int,
                 message_count: int,
                 clients: List[str] = []) -> None:
        self.topic_name = topic_name
        self.channel_name = channel_name
        self.channel_depth = channel_depth
        self.message_count = message_count
        self.clients = clients

    def format_clients(self) -> List[str]:
        # Get (name, message count) for each client
        cmap = {}
        for client in self.clients:
            client_id = client["client_id"]
            message_count = client["message_count"]
            cmap.setdefault(client_id, defaultdict(int))
            # multiple clients with same id is possible
            cmap[client_id]["message_count"] += message_count
        clis = [
            "{}({})".format(k[-2:], v["message_count"])
            for k, v in cmap.items()
        ]
        clis.sort()
        return clis

    def format_print(self) -> str:
        if self.topic_name == "TOPIC":
            print(
                f"{self.topic_name:<20} {self.channel_name:<30} {self.channel_depth:10} {self.message_count:<10} CLIENTS"
            )
        else:
            channel_depth = self.channel_depth
            if int(channel_depth) >= 50:
                channel_depth = cf.fp.red_ansi(channel_depth, [])
            elif int(channel_depth) >= 10:
                channel_depth = cf.fp.yellow_ansi(channel_depth, [])
            elif int(channel_depth) > 0:
                channel_depth = cf.fp.green_ansi(channel_depth, [])
            # channel_depth = str(channel_depth).ljust(20, ' ')
            msg_cnt = str(self.message_count).ljust(20, ' ')
            # channel_depth = cf.fp.green_ansi(self.channel_depth, [])
            if channel_depth != self.channel_depth:
                channel_depth = str(channel_depth).ljust(19, ' ')
            clients = self.format_clients()
            print(
                f"{self.topic_name:<20} {self.channel_name:<30} {channel_depth:<10} {self.message_count:<10} {' '.join(clients)}"
            )


def display_result(status: dict, key):
    topics = status["topics"]
    subprocess.call("clear")
    print(key, end="\n\n")
    Liner("TOPIC", "CHANNEL", "DEPTH", "MSG_COUNT", "CLIENTS").format_print()
    for topic in topics:
        topic_name = topic["topic_name"]
        channels = topic["channels"]
        for channel in channels:
            channel_name = channel["channel_name"]
            channel_depth = channel["depth"]
            message_count = channel["message_count"]
            clients = channel.get("clients", [])

            Liner(topic_name, channel_name, channel_depth, message_count,
                  clients).format_print()


def exit_safely(signum, frame):
    print('safe exit handler: %s' % signum)
    sys.exit(0)


class NSQMonitor(object):
    def __init__(self, prefix: str, step_forward: int = 30) -> None:
        self.prefix = prefix
        self.step_forward = step_forward
        cf.info(f"{self.prefix} NSQ Monitor Start")

    def invoke(self):
        key = f"{self.prefix}_NSQ_STATUS_TOKEN"
        cli = rc.us
        pipe = cli.pipeline()
        for _ in range(self.step_forward + 3):
            pipe.lpush(key, "1")
        pipe.execute()

    def loop(self):
        signal.signal(signal.SIGTERM, exit_safely)
        signal.signal(signal.SIGINT, exit_safely)
        signal.signal(signal.SIGHUP, exit_safely)

        cli = rc.us
        cnt = 0
        self.invoke()
        while True:
            if cnt >= self.step_forward:
                self.invoke()
                cnt = 0
            date = datetime.datetime.now() - datetime.timedelta(seconds=3)
            date = date.strftime("%Y-%m-%d %H:%M:%S")
            key = f"{self.prefix}_NSQ_STATUS_{date}"
            if cli.exists(key):
                display_result(json.loads(cli.get(key).decode("utf-8")), key)
            else:
                time.sleep(1)
            cnt += 1


class EnumMap(object):
    keys = {
        'test': ServerEnum.TEST,
        'ali': ServerEnum.ALIAI,
        'aliyun': ServerEnum.ALIAI,
        'tencent': ServerEnum.TENCENT,
        'tc': ServerEnum.TENCENT
    }


def cli():
    argparser = argparse.ArgumentParser(description='NSQ Monitor')
    argparser.add_argument('--prefix', type=str, default="test", help='prefix')
    argparser.add_argument('--step_forward',
                           type=int,
                           default=30,
                           help='step forward')
    args = argparser.parse_args()

    NSQMonitor(EnumMap.keys[args.prefix].value, args.step_forward).loop()
    # NSQMonitor("MINI.LOCAL", args.step_forward).loop()


if __name__ == "__main__":
    cli()