from app.auth import create_access_token, verify_password
from jose import jwt
from datetime import timedelta
from app.auth import secret_key

import pytest

def test_token_generation():
    user_id = "test_user_id"
    access_token = create_access_token(data={"sub": user_id}, expires_delta=timedelta(minutes=1))
    payload = jwt.decode(access_token, f"{secret_key}", algorithms=["HS256"])
    assert payload.get("sub") == user_id

def test_token_expiration():
    user_id = "test_user_id"
    access_token = create_access_token(data={"sub": user_id}, expires_delta=timedelta(seconds=5))
    import time
    time.sleep(7)
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(access_token, f"{secret_key}", algorithms=["HS256"])
