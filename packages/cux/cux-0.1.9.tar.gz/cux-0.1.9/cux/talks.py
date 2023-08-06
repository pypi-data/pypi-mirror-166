from typing import List, Callable, Dict, Optional
import codefast as cf
import pydantic
from enum import Enum, auto


class EntityType(str, Enum):
    SALESMAN = "host_salesman"
    CUSTOMER = "customer_contact"


class TalkOnline(pydantic.BaseModel):
    """ online talk data structure
    """

    channel: int
    content: str
    begin_time: float
    end_time: float
    entity_type: str
    name: Optional[str] = None
    begin_percent: Optional[float] = None
    end_percent: Optional[float] = None
    order: Optional[int] = None

    """
    TalkOnline.parse_obj(dict_input), create a TalkOnline object
    to_object.dict(), create a dict object
    """


class TalkRaw(pydantic.BaseModel):
    """ raw talk data structure
    """

    Text: str
    ChannelId: int
    BeginTime: float
    EndTime: float
    RoleId: Optional[int] = None
    order: Optional[int] = None
    SilenceDuration: Optional[int] = None
    EmotionValue: Optional[float] = None
    SpeechRate: Optional[int] = None


class TalkTransformer(object):
    @staticmethod
    def online_to_raw(talk: TalkOnline) -> TalkRaw:
        """Reformat conversation from 
        {
            "entity_id": 3761,
            "name": "John",
            "entity_type": "host_salesman",
            "content": "Are u okay",
            "begin_time": 215.46,
            "end_time": 217.71,
            "begin_percent": 42.070856178827505,
            "end_percent": 42.51019260508927,
            "channel": 0,
            "order": 36
        }
        to 
        {
            "Text": "Are u okay。",
            "ChannelId": 0,
            "order": 0,
            "entity_type": "all",
            "BeginTime": 1120,
            "EndTime": 2440,
            "RoleId": 1,
        }
        Args:
            talk, a single dict of one setence conversation
        Returns:
            a dict of reformatted conversation
        """
        dct = {
            "Text": talk.content,
            "ChannelId": talk.channel,
            "BeginTime": talk.begin_time,
            "EndTime": talk.end_time,
            "RoleId": 1 if talk.entity_type == EntityType.SALESMAN else 0,
        }
        if talk.order is not None:
            dct["order"] = talk.order
        return TalkRaw.parse_obj(dct)

    @staticmethod
    def raw_to_online(talk: TalkRaw) -> TalkOnline:
        dct = {
            "content": talk.Text,
            "channel": talk.ChannelId,
            "begin_time": talk.BeginTime,
            "end_time": talk.EndTime,
            "entity_type": EntityType.CUSTOMER
            if talk.RoleId == 0
            else EntityType.SALESMAN,
        }
        if talk.order is not None:
            dct["order"] = talk.order
        return TalkOnline.parse_obj(dct)


def revert_online_talks(file_path: str) -> List[Dict]:
    # load talks from online conversation and revert to raw conversation
    talks = cf.js(file_path)
    talks = [TalkOnline.parse_obj(t) for t in talks]
    talks = [TalkTransformer.online_to_raw(t) for t in talks]
    talks = [t.dict() for t in talks]
    talks = [{"OldRoleId": t["RoleId"], **t} for t in talks]
    return talks
