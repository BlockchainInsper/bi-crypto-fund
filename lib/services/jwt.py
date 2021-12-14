import jwt
import datetime
import os

def generate_auth_token(user_id):
    """
    Generates the Auth Token
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            os.environ.get("SECRET_KEY", "myprecious"),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    """
    try:
        payload = jwt.decode(auth_token, os.environ.get("SECRET_KEY", "myprecious"))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
