import asyncio
import aiohttp


async def get_available_time_slots(id: int):
    recommendation_data = await get_recommendation_data(id)
    return recommendation_data['placement_time']

# async def get_disabled_times():
#     recommendation_id = 25 # 26
#     recommendation_data = await get_recommendation_data()
#     return recommendation_data['placement_time']

async def test_update_time_query():
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:3001/recommendations/edit-time'
        payload = {'id': '7', 'booking_time': 'morning/15.12_morning/17.12'}
        async with session.post(url, data=payload) as resp:
            data = await resp.json()
            # print(data)
            return data

async def update_booking_time(booking_time: str, user_id: str, channel: str):
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:3001/recommendations/edit-time'
        # 'id': '7'
        payload = {'user_id': user_id, 'channel': channel, 'booking_time': booking_time}
        async with session.post(url, data=payload) as resp:
            data = await resp.json()
            # print(data)
            return data

# Data source services
async def get_recommendation_data(id: int):
    # recommendation_id = 26 # 25
    async with aiohttp.ClientSession() as session:
        url = f'http://localhost:3001/recommendations/individual?idRecommendation={id}'
        async with session.get(url) as resp:
            data = await resp.json()
            # print(data)
            return data


# misc
def is_serialized_object(x):
    import json
    try:
        json.loads(x)
        # print('Is object')
        return True
    except:
        # print('Is not object')
        return False
