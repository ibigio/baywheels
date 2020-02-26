import asyncio
from aiohttp import ClientSession

# LAT = 37.776619
# LON = -122.417385

LAT = 37.7730627
LON = -122.4390777

AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
API_KEY = os.environ.get('API_KEY')
MEMBER_ID = os.environ.get('MEMBER_ID')

bike_id = 123
headers = { 'api-key': API_KEY, 'authorization':AUTH_TOKEN }

max_bike_id = 20000

def generate_data(i):
    data = {}
    data['userLocation'] = {'lat':LAT,'long':LON} # TODO: maybe toFloat?
    data['qrCode'] = {'memberId':MEMBER_ID, 'qrCode':str(i)}
    return data

data_list = [generate_data(i) for i in range(max_bike_id)]

def t(resp):
    print(resp)

async def fetch(url, session, i):
    async with session.request('POST', url, headers=headers, json=data_list[i]) as response:
        if response.reason == 'OK':
            print(i)
        return await response.read()


async def bound_fetch(sem, url, session, i):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session, i)
        #print(f)


async def run(r):
    url = "https://layer.bicyclesharing.net/mobile/v2/fgb/rent"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in range(r):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session, i))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(max_bike_id))
loop.run_until_complete(future)
print("Done")