# from datetime import datetime
# from typing import List, Optional, Dict, Any, Union
# from pydantic import BaseModel, Field, root_validator, AnyHttpUrl
# import httpx
from pprint import pprint
# import json
# from fastapi import Depends
# from fastapi.encoders import jsonable_encoder
import asyncio

# from ..settings import get_settings
from ..schemas import *
# from ..db import *

# settings = get_settings()

# class BaseData:

#     def __init__(self):
#         self.data_dir = settings.DATA_DIR
#         self.coingecko_url = settings.COIN_GECKO_MARKETS
#         # timeout = httpx.Timeout(connect=60.0, read=60.0, write=60.0, pool=60.0)
#         # timeout = httpx.Timeout(None)
#         # URL = 'https://farm.army/api/v0/farms'
#         # URL = "https://httpbin.org/stream/10"
#         # URL = 'https://farm.army/api/v0/liquidity-tokens'

#     def _write_json(self, json_file, data):
#         try:
#             path = self.data_dir + "/" + json_file
#             json_object = json.dumps(jsonable_encoder(data), indent=4)
#             with open(path, "w") as outfile:
#                 outfile.write(json_object)
#         except Exception as e:
#             print(e)

#     def _read_json(self, json_file):
#         path = self.data_dir + "/" + json_file
#         with open(path, "r") as f:
#             data = json.load(f)

#             # json_object = json.dumps(jsonable_encoder(data.read()), indent=4)
#             f.close()
#         return data

#     def _get_request(self, *args, **kwargs):
#         r = httpx.get(*args, **kwargs).json()
#         return r

#     async def _read_lines(self, url: str, client: httpx.AsyncClient):
#         assert len(url) > 10
#         try:
#             async with client.stream("GET", url) as resp:
#                 async for line in resp.aiter_lines():
#                     yield json.loads(line)
#         except httpx.RemoteProtocolError as e:
#             print('read_lines: ', e)
#             yield e

#     def get_or_create_eventloop(self):
#         # https://techoverflow.net/2020/10/01/how-to-fix-python-asyncio-runtimeerror-there-is-no-current-event-loop-in-thread/
#         try:
#             return asyncio.get_event_loop()
#         except RuntimeError as err:
#             if "There is no current event loop in thread" in str(err):
#                 loop = asyncio.new_event_loop()
#                 asyncio.set_event_loop(loop)
#                 return asyncio.get_event_loop()
