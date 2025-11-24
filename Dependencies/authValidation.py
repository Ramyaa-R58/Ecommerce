from datetime import datetime,timedelta
import secrets
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from Helpers.constants import ADMIN_USER

algorithm = "HS256"
secret_key = secrets.token_urlsafe(32)
security = HTTPBearer()
def get_current_login(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token = credentials.credentials
    payload = jwt.decode(token,secret_key,algorithms=[algorithm])
    if payload:
        return payload

def check_admin(current_login:dict):
    if current_login['user_role'] == ADMIN_USER:
        return True
    return False


def create_user_token(data:dict):
    encode_data = data.copy()
    encode_data['exp'] = datetime.utcnow() + timedelta(minutes=10)
    token = jwt.encode(encode_data,secret_key,algorithm=algorithm)
    return token