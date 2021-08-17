import aiohttp
import asyncio


HOST = 'http://127.0.0.1:8080'


async def make_request(path, method='get', **kwargs):
    async with aiohttp.ClientSession() as session:
        request_method = getattr(session, method)
        async with request_method(f'{HOST}/{path}', **kwargs) as response:
            print(response.status)
            return (await response.json())



async def main():
    # response = await make_request('advertisement', 'post', json={'username': 'Футболист', 'header': 'Куплю', "definition": 'Бутсы'})
    # response = await make_request('advertisement/1', 'get')
    # response = await make_request('advertisement/1', 'delete')
    response = await make_request('advertisement/1', 'patch', json={"definition": 'А может и не бутсы'})
    print(response)





asyncio.run(main())