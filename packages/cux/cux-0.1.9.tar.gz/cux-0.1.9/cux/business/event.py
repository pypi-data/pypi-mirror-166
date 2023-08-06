#!/usr/bin/env python
import json
import os
import random
import re
import sys
from collections import defaultdict
from functools import reduce
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import codefast as cf
import joblib
import numpy as np
import pandas as pd
from rich import print


class EventResult(object):

    def csv2json(csvfile: str) -> Dict:
        ds = pd.read_csv(csvfile)
        js = json.loads(ds.to_json(orient='records'))
        for e in js:
            e['context'] = json.loads(e['context'])
            e['rule_path'] = json.loads(e['rule_path'])
            e['res']=e['context']
            if isinstance(e['res'], dict):
                e['res']=[e['res']]
            e['rule_name']=e['rule_path'][0]
        return js


