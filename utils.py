import bcrypt
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"  # Replace with a secure key

def hash_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)

def check_password(password, hashed):
    bytes = password.encode('utf-8')
    return bcrypt.checkpw(bytes, hashed)

def generate_jwt(payload, expires_in=3600):
    """
    Generate a JWT token.

    :param payload: Dictionary containing the payload data.
    :param expires_in: Expiration time in seconds (default: 1 hour).
    :return: Encoded JWT token as a string.
    """
    payload['exp'] = datetime.utcnow() + timedelta(seconds=expires_in)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token):
    """
    Decode a JWT token.

    :param token: Encoded JWT token as a string.
    :return: Decoded payload as a dictionary.
    :raises: jwt.ExpiredSignatureError, jwt.InvalidTokenError
    """
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
