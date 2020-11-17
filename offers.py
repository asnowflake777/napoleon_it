from http import HTTPStatus
from sanic import Sanic, response
from tortoise.exceptions import IntegrityError

from db.models import Offer
from db.utils import connect_to_db
from utils import get_request_data
from settings import OFFERS_APP_IP, OFFERS_APP_PORT


app = Sanic("offers")


@app.route('/offer/create', {'POST'})
async def create_offer(request):
    user_id, title, text = get_request_data(request.json, ('user_id', 'title', 'text'))

    if not str(user_id).isdigit():
        return response.json({'msg': 'user_id should be positive integer'})

    if all((user_id, title, text)):
        try:
            await Offer.create(user_id=user_id, title=title, text=text)
            return response.HTTPResponse(status=HTTPStatus.CREATED)

        except IntegrityError:
            return response.json({'msg': 'user_id is not valid'}, status=HTTPStatus.BAD_REQUEST)

    return response.HTTPResponse(status=HTTPStatus.NO_CONTENT)


@app.route('/offer', {'POST'})
async def get_offer(request):
    error, offers = None, None
    user_id, offer_id = get_request_data(request.json, ('user_id', 'offer_id'))

    if all((user_id, offer_id)) or not any((user_id, offer_id)):
        error = {'msg': 'you should set user_id or offer_id'}

    elif user_id and str(user_id).isdigit():
        offers = await Offer.filter(user_id=user_id).values('id', 'title')

    elif offer_id and str(offer_id).isdigit():
        offers = await Offer.filter(id=offer_id).values('id', 'title', 'text')

    else:
        error = {'msg': 'user_id and offer_id should be positive integer'}

    result, status_code = (offers, HTTPStatus.OK) if not error else (error, HTTPStatus.BAD_REQUEST)
    return response.json(result, status_code)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host=OFFERS_APP_IP, port=OFFERS_APP_PORT)
