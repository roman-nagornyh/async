import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path
from flags_theardpool import save_flag
from concurrent import futures
from enum import Enum
import httpx
import tqdm

DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

DownloadStatus = Enum('DownloadStatus', 'OK NOT_FOUND ERROR')

async def get_flag(client: httpx.AsyncClient, base_url: str, cc: str):
    url = f'{base_url}/{cc}/{cc}.gif'
    res = await client.get(url, timeout=3.1, follow_redirects=True)
    res.raise_for_status()
    return res.content

async def download_one(client:httpx.AsyncClient, base_url:str, sema)
    pass

def main(cc_list: list[str]) -> bool:
    # with futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     res = executor.map(, sorted(cc_list))
    # return True if len(res) > 0 else False
    pass



