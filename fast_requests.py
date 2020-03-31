import asyncio
from aiohttp import ClientSession

# Notes:
#
# Response Processor: final_callback should be a function that consumes a
# byte sequence (the body of the response)
# > final_callback: (b'') => ?
#
# Middle Response Processor: initial_callback shoudl be a function that
# consumes an HTTP response (and doesn't do
# any operations with the body of it)
# > initial_callback: (response) => ?
#
# Generation Data: gen_data should be a list of type DATA
# > gen_data: DATA
#
# Request Generator: req_gen should be a function that consumes type DATA,
# and returns a map (that can be turned into kwargs
# for a request).
# > req_gen: (DATA) => map()

### Hello World (Wide Web) ###
#
# >     import fast_requests as fastr
# >     
# >     fastr.get('https://postman-echo.com/get', final_callback=print)
# >     # Sends a single request and prints the result.
# >     
# >     fastr.get('https://postman-echo.com/get', reps=10000)
# >     # Sends 10000 requests in around 15 seconds ( > 650rps) (!)


### Example Usage (with a wacky request) ###
#
# >     import fast_requests as fastr
# >
# >     gen_data = [1,2,3]
# >     
# >     def req_gen(num):
# >         headers = {'auth': 'i_promise_i_know_the_password', 'api-key': '17-a'}
# >         json = {'number': num, 'animals': {'dog', 'cat', 'mouse'}
# >         return {'headers': headers, 'json': json}
# >     
# >     fastr.post('https://postman-echo.com/post', gen_data=gen_data, req_gen=req_gen, final_callback=print)
# >         

def get(url, params=None, **kwargs):
    return request('get', url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    return request('post', url, **kwargs)


def request(method, url, reps=1, final_callback=None, initial_callback=None, kwargs_list=None, **kwargs):

    async def run(kwargs_list):
        tasks = []
        sem = asyncio.Semaphore(1000)

        async with ClientSession() as session:
            if kwargs_list is None:
                for i in range(reps):
                    task = asyncio.ensure_future(bound_fetch(sem, session, **kwargs))
                    tasks.append(task)
            else:
                for kwargs_elt in kwargs_list:
                    task = asyncio.ensure_future(bound_fetch(sem, session, **{**kwargs, **kwargs_elt}))
                    tasks.append(task)

            responses = asyncio.gather(*tasks)
            return await responses

    async def fetch(session, **req_kwargs):
        async with session.request(method, url, **req_kwargs) as response:
            if initial_callback != None:
                initial_callback(response)
            return await response.read()

    async def bound_fetch(sem, session, **req_kwargs):
        async with sem:
            if final_callback != None:
                final_callback( await fetch(session, **req_kwargs) )
            return await fetch(session, **req_kwargs)

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(kwargs_list))
    return loop.run_until_complete(future)
