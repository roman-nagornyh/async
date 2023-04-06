import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path
from flags_theardpool import save_flag, POP20_CC
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


async def supervisor(cc_list: list[str], base_url: str,
                     verbose: bool, concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    semaphore = asyncio.Semaphore(concur_req)
    async with httpx.AsyncClient() as client:
        to_do = [download_one(client, cc, base_url, semaphore, verbose) for cc in cc_list]
        to_do_iter = asyncio.as_completed(to_do)
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
        error: httpx.HTTPError | None = None
        for coro in to_do_iter:
            try:
                status = await coro
            except httpx.HTTPStatusError as exc:
                er_msg = 'Ошибка в статусе запроса'
                error = exc
            except httpx.RequestError as ex:
                er_msg = 'Ошибка запроса'
                error = ex
            except KeyboardInterrupt:
                break
            if error:
                status = DownloadStatus.ERROR
            counter[status] += 1
        return counter


async def download_many(flag_list: list[str], base_url: str, verbose, conq_req):
    
    coro = supervisor()


async def download_one(client: httpx.AsyncClient,
                       cc: str,
                       base_url: str,
                       semaphore: asyncio.Semaphore,
                       verbose: bool) -> DownloadStatus:
    try:
        async with semaphore:
            image = await get_flag(client, base_url, cc)
    except httpx.HTTPStatusError as ex:
        res = ex.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'Флаг не найден {res.url}'
        else:
            raise
    else:
        await asyncio.to_thread(save_flag, image, f'{cc}.gif')
        status = DownloadStatus.OK
        msg = 'ОК'
    if verbose and msg:
        print(cc, msg)
    return status

