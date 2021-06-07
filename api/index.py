import json
from sanic import Sanic
from sanic.response import json as sjson

import random

app = Sanic("quotes")


def get_quote():
    # TODO replace to reading random from database
    quotes = ["test quote", "another test quote", "quote with a\nnewline", "ololol ohoho", "pomodoro roror", "123", "324234dsdsa"]
    index = random.randrange(len(quotes))
    import uuid
    return {'id': str(uuid.uuid4()), 'quote': quotes[index], 'like': random.choice([True, False])}

@app.route('/', methods=['GET'])
@app.route('/api', methods=['GET'])
async def index(request):
    user_id = request.args.get('id') or None
    # print("user_id=", user_id)
    result = get_quote()
    result.update({'status': 'ok'})
    return sjson(result)


@app.route('/like', methods=['POST'])
@app.route('/api/like', methods=['POST'])
async def ad_post(request):
    # print(request.body)  #  user_id, quote_id, is_like
    return sjson({'status': 'ok'})


@app.route('/categories', methods=['POST'])
@app.route('/api/categories', methods=['POST'])
async def ad_post(request):
    print(request.body)  #  {categories: [1,2,3]}
    return sjson({'status': 'ok'})


@app.route('/notifications', methods=['POST'])
@app.route('/api/notifications', methods=['POST'])
async def ad_post(request):
    print(request.body)  #  {start_time: ?, stop_time: ?, number: 5} to reasearch about time\timezone and sending time to server
    return sjson({'status': 'ok'})


# need to research
@app.route('/payment', methods=['POST'])
@app.route('/api/payment', methods=['POST'])
async def ad_post(request):

    print(request.body)  #  {user_id: 666}
    return sjson({'status': 'ok'})


#  sanic api.index.app