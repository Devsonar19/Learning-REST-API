from jose import JWTError, jwt
from datetime import datetime, timedelta
#secret key
SECRET_KEY = 'a23777505b7ac76ba98e639a65e0f885bf8f7e795c359fb1de1f43df85f3fc59'

#algo
ALGORITHM = "HS256"

#expiration
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expiration":int(expire.timestamp())})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
