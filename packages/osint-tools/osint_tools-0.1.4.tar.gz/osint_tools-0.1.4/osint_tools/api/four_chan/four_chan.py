from ..base import *
import asyncio
import json
import httpx
import requests
# from fastapi.encoders import jsonable_encoder
import urllib.parse
from time import sleep

def get_catalog(board: Board) -> List[CatalogThread]:
    url = f'https://a.4cdn.org/{board}/catalog.json'
    data = requests.get(url).json()
    all_posts = []
    for page in data:
        for thread in page['threads']:
            '''attach board to thread'''
            thread['board'] = board
            all_posts.append(CatalogThread(**thread))
    return all_posts



def catalog_image_generator(board: Board):
    url = f'https://a.4cdn.org/{board}/catalog.json'
    r = requests.get(url).json()
    lst = []
    for idx, page in enumerate(r):
        for thread in r[idx]['threads']:
            if 'last_replies' in thread:
                for comment in thread['last_replies']:
                    if 'ext' in comment and 'tim' in comment:
                        url = 'http://i.4cdn.org/{0}/{1}{2}'.format(
                            board, 
                            str(comment['tim']), 
                            str(comment['ext'])
                        )
                        lst.append(url)
    print(lst)
    print(len(lst))
    for i in lst:
        yield i

def iter_img_lst():
    counter = 0
    for img in catalog_image_generator():
        sleep(1.01)
        file_name = img.split('/')[-1]
        filename, headers = urllib.request.urlretrieve(img, f'./chan_images/{file_name}')
        counter += 1
        print(f'{counter}: {filename} {headers}')



# if __name__ == "__main__":
    # iter_img_lst()





























class AsyncHTTP:

    def get_or_create_eventloop(self):
        # https://techoverflow.net/2020/10/01/how-to-fix-python-asyncio-runtimeerror-there-is-no-current-event-loop-in-thread/
        try:
            return asyncio.get_event_loop()
        except RuntimeError as err:
            if "There is no current event loop in thread" in str(err):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()

    async def _read_lines(self, url: str, client: httpx.AsyncClient):
        assert len(url) > 10
        try:
            async with client.stream("GET", url) as resp:
                async for line in resp.aiter_lines():
                    yield json.loads(line)
        except httpx.RemoteProtocolError as e:
            print('read_lines: ', e)
            yield e


async def get_catalog_v2():
    url = 'https://a.4cdn.org/wg/catalog.json'
    client = httpx.AsyncClient()
    aa = AsyncHTTP()
    async_gen = aa._read_lines(url, client)

    all_posts = []
    # _type = ''
    async for page in async_gen:
        # _type = type(page)
        for thread in page:
            for item in thread['threads']:
                all_posts.append(item)

            # all_posts.append(thread)
            # thread = jsonable_encoder(thread)
            # all_posts.append(CatalogThread(**thread))
    # print(_type)
    await async_gen.aclose()
    await client.aclose()
    return all_posts
