import requests
import json
import datetime as pt
from datetime import datetime as dt


def send_data(player_id, time, fatigue_result):
    player_base = [{"name": "Subject_1", "id": "b263d9e5-8161-4ffb-80c9-159fb3d2e04b"},
                   {"name": "Subject_2", "id": "a363aae2-22f7-43df-a0a4-3a25c841b068"}]

    API_URL = 'http://localhost:5000/api'

    data_route = '/data'

    date = dt.strptime(time, '%Y-%m-%d')
    formatted_date = pt.date.strftime(date, "%m/%d/%Y")
    result = [[str(formatted_date), fatigue_result]]
    result = str(result).replace("'",'"')
    data = {"playerId": player_id,
            "data": str(result)}

    response = requests.post(API_URL + data_route + '/set', data = data)