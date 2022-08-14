from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired, BadTimeSignature, BadSignature
from core.config import settings
from pydantic import EmailStr

token_seed = URLSafeTimedSerializer(secret_key=settings.token_secret_key)



def create_token(email:EmailStr)-> str:
    token = token_seed.dumps(email)
    return token

def verify_token(token:str):
    token_data = 0
    try:
        token_data = token_seed.loads(s=token, max_age=3600)

    except (SignatureExpired,BadSignature ,BadTimeSignature):
        return None
    return token_data
    


