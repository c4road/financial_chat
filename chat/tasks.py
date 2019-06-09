import json
import requests
import csv

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task

channel_layer = get_channel_layer()


@shared_task
def get_stock_code(chat_room, ticker):

    stock_url = "https://stooq.com/q/l/?s={}&f=sd2t2ohlcv&h&e=csv".format(
        ticker)
    response = {
        'message': 'Invalid ticker',
        'username': 'Mr. Bot',
    }
    stock_closes = []

    try:
        with requests.Session() as s:
            csv_file = s.get(stock_url).content.decode('utf-8')
            cr = csv.DictReader(csv_file.splitlines())
            for line in cr:
                stock_closes.append(line['Close'])

    except (requests.exceptions.ConnectionError, Exception) as e:

        response['message'] = e

    if len(stock_closes) > 0 and not stock_closes[-1] == 'N/D':

        response['message'] = "{} quote is ${} per share".format(
            ticker.upper(), stock_closes[-1])

    async_to_sync(channel_layer.group_send)(
        chat_room,
        {
            "type": 'chat_message',
            "text": json.dumps(response)

        }
    )
