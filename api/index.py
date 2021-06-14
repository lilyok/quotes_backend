import json
import random

from sanic import Sanic
from sanic.response import json as sjson

from .notifications import NotificationClient


app = Sanic('quotes')
notifications = NotificationClient()


def get_quote():
    # TODO replace to reading random from database
    quotes = ['test quote', 'another test quote', 'quote with a\nnewline', 'ololol ohoho', 'pomodoro roror', '123', '324234dsdsa']
    index = random.randrange(len(quotes))
    import uuid
    return {'id': str(uuid.uuid4()), 'quote': quotes[index], 'like': random.choice([True, False])}


@app.route('/', methods=['GET'])
@app.route('/api', methods=['GET'])
async def index(request):
    user_id = request.args.get('id') or None
    # print('user_id=', user_id)
    result = get_quote()
    result.update({'status': 'ok'})
    return sjson(result)


@app.route('/like', methods=['POST'])
@app.route('/api/like', methods=['POST'])
async def like_post(request):
    # print(request.body)  #  user_id, quote_id, is_like
    return sjson({'status': 'ok'})


@app.route('/settings', methods=['POST'])
@app.route('/api/settings', methods=['POST'])
async def settings_post(request):
    # print(request.body)  #  user_id, quote_id, is_like
    # notifications.create_or_update_notifications(**json.loads(request.body))
    notifications.update_settings(**json.loads(request.body))
    return sjson({'status': 'ok'})


@app.route('/timezone', methods=['POST'])
@app.route('/api/timezone', methods=['POST'])
async def timezone_post(request):
    # print(request.body)  #  user_id, quote_id, is_like
    notifications.create_or_update_notifications(**json.loads(request.body))
    return sjson({'status': 'ok'})




#########################################################


# need to research
@app.route('/payment', methods=['POST'])
@app.route('/api/payment', methods=['POST'])
async def ad_post(request):
    # print(request.body)  #  {user_id: 666}
    return sjson({'status': 'ok'})

@app.route('/test_notification', methods=['GET'])  # TODO delete
@app.route('/api/test_notification', methods=['GET'])  # TODO delete
async def test_notification(request):
    # notifications.send()  # TODO disabled notification until the logic is implemented
    return sjson({'status': 'ok'})


#  sanic api.index.app