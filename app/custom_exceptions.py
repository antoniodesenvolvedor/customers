from fastapi import HTTPException, status


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

inactive_user_exception = HTTPException(status_code=400, detail="Inactive user")

invalid_token_exception = HTTPException(status_code=400, detail="X-Token header inválido")

login_unauthorized_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"},
        )

