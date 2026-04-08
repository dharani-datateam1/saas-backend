# password secure panna use pannuvom
from passlib.context import CryptContext

# token create panna use pannuvom
from jose import jwt, JWTError

# time handle panna
from datetime import datetime, timedelta

# fastapi imports
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


# 🔐 password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔑 token settings
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# 👉 OAuth setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 👉 password ah secure ah convert pannum (hash)
def hash_password(password):
    return pwd_context.hash(password)


# 👉 password correct ah nu check pannum
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 👉 login aprm token create pannum
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


# 👉 current user get pannum (FIXED 🔥)
def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token ❌")

        # 🔥 IMPORTANT: only email return
        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token ❌")