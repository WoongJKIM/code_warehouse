import time

#url에서 request 하는 라이브러리 불러오는 패키지
import aiohttp
#파이썬에서 async를 구현하게 하는 패키지
import asyncio

@asyncio.coroutine
def _get(*args, **kwargs):
    yield from asyncio.sleep(2)

    response = yield from aiohttp.request(*args, **kwargs)

    return (yield from response.text())

@asyncio.coroutine
def _read_api(url):
    sem = asyncio.Semaphore(5) 

    headers = {
        'Host' : '',
        'Origin' : '',
        'Referer' : '',
        'User-Agent' : '',
    }

    with (yield from sem ):    

        response = yield from _get('GET', url, headers = headers, compress = True)
        #yield from check_api_result(response, page)
    
    time.sleep(2)

    return response

def _get_info(df):

  url = """https://www.aaaa.co.kr/getDataList.do?a={a}&b={b}"""

  loop = asyncio.get_event_loop()

  asyncio_result = loop.run_until_complete(asyncio.wait([_read_api(url.format(a = row['a'], b = row['b'])) for idx, row in df.iterrows()]))

  loop.close()

  return asyncio_result