from fastapi.exceptions import HTTPException
from fastapi import status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

incorrect_username_or_password = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

access_token_already_expired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="access token already expired",
    headers={"WWW-Authenticate": "Bearer"},
)

user_not_found = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="user not found",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid token",
    headers={"WWW-Authenticate": "Bearer"},
)

user_alredy_exist = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='user with that login\email alredy exist'
)


referal_not_exist = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='referal_not_exist'
)

referal_time_expired = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='referal time expired'
)
