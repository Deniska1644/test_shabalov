from fastapi.exceptions import HTTPException
from fastapi import status

save_create_error = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="can`t save referal link in db, probably already exist"
)

ttl_error = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="life time referal link already end"
)

not_generated_link_error = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="referral link has not yet been generated"
)

not_exist_referal = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="that referal not availebel or not exist"
)


not_availebel_email = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="not_availebel_email"
)
