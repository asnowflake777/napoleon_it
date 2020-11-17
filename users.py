import jwt

from http import HTTPStatus
from sanic import Sanic, response
from tortoise.exceptions import IntegrityError

from db.models import User, Offer
from db.utils import connect_to_db
from utils import get_request_data, encrypt_password
from settings import USER_APP_IP, USER_APP_PORT, SALT


app = Sanic("users")


@app.route('/user/registry', {'POST'})
async def registry(request):
    username, password, email = get_request_data(request.json, ('username', 'password', 'email'))

    if all((username, password, email)):
        try:
            password = encrypt_password(username, password)
            await User.create(name=username, password=password, email=email)
            return response.HTTPResponse(status=HTTPStatus.CREATED)

        except IntegrityError:
            return response.json({'msg': 'user with this email already registered'})
    else:
        return response.json(
            {'msg': 'username, password and email are required fields'},
            status=HTTPStatus.BAD_REQUEST
        )


@app.route('/user/auth', {'POST'})
async def auth(request):
    msg = 'username and password are required fields'
    username, password = get_request_data(request.json, ('username', 'password'))

    if all((username, password)):
        user = await User.filter(name=username).first()

        if await user.exists():
            guessed_password = encrypt_password(username, password)
            if guessed_password == user.password:
                token = jwt.encode({username: guessed_password.decode()}, SALT, algorithm='HS256')
                token = token.decode()
                return response.json({'user_id': user.pk, 'token': token})

        msg = 'username or password are incorrect'
    return response.json({'msg': msg}, status=HTTPStatus.BAD_REQUEST)


@app.route('/user/<user_id>', {'GET'})
async def user_info(_, user_id):

    if not str(user_id).isdigit():
        return response.json({'msg': 'user_id should be positive integer'}, status=HTTPStatus.BAD_REQUEST)

    user = await User.filter(id=user_id).first()

    if await user.exists():
        user_offers = await Offer.filter(user_id=user_id).values('id', 'title')
        return response.json({'user_id': user.pk, 'username': user.name, 'offers': user_offers})

    return response.HTTPResponse(status=HTTPStatus.NO_CONTENT)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host=USER_APP_IP, port=USER_APP_PORT)
