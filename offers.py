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

    if all((user_id, title, text)):
        try:
            await Offer.create(user_id=user_id, title=title, text=text)
            return response.HTTPResponse(status=HTTPStatus.CREATED)

        except IntegrityError:
            return response.json({'msg': 'user_id is not valid'}, status=HTTPStatus.BAD_REQUEST)

    return response.HTTPResponse(status=HTTPStatus.NO_CONTENT)


@app.route('/offer', {'POST'})
async def get_offer(request):
    user_id, offer_id = get_request_data(request.json, ('user_id', 'offer_id'))

    if all((user_id, offer_id)) or not any((user_id, offer_id)):
        return response.json(
            {'msg': 'you should set user_id or offer_id'},
            status=HTTPStatus.BAD_REQUEST,
        )
    elif user_id:
        offers = await Offer.filter(user_id=user_id).values('id', 'title')
    elif offer_id:
        offers = await Offer.filter(id=offer_id).values('id', 'title', 'text')
    else:
        return response.json({'msg': 'something went wrong'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return response.json(offers)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host=OFFERS_APP_IP, port=OFFERS_APP_PORT)
