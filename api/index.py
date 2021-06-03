import json
from sanic import Sanic
from sanic.response import json as sjson

import random

app = Sanic("quotes")


def get_quote():
    # TODO replace to reading random from database
    return random.choice(["test quote", "another test quote", "quote with a\nnewline"])


@app.route('/', methods=['GET'])
async def index(request):

    user_id = request.args.get('id') or None
    return sjson({'quote': get_quote()})


@app.route('/like', methods=['POST'])
async def ad_post(request):

    print(request.body)  #  quote_id, is_like
    return sjson({'status': 'ok'})


@app.route('/categories', methods=['POST'])
async def ad_post(request):

    print(request.body)  #  {categories: [1,2,3]}
    return sjson({'status': 'ok'})



@app.route('/notifications', methods=['POST'])
async def ad_post(request):

    print(request.body)  #  {start_time: ?, stop_time: ?, number: 5} to reasearch about time\timezone and sending time to server
    return sjson({'status': 'ok'})


# need to research
@app.route('/payment', methods=['POST'])
async def ad_post(request):

    print(request.body)  #  {user_id: 666}
    return sjson({'status': 'ok'})


#  sanic api.index.app