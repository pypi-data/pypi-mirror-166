import requests


def botsay(msg: str):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/51f227fe-8240-431d-a45e-cb72d9000c7e"
    requests.post(url, json={"msg_type": "text", "content": {"text": msg}})
