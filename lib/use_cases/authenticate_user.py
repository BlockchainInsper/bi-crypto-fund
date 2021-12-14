from hashlib import sha256
from lib.services.jwt import generate_auth_token
from lib.repository.mongo import UserRepository

def authenticate_user_use_case(username: str, password: str, user_repository: UserRepository):
    user = user_repository.get_user_by_username(username)

    m = sha256()
    m.update(password.encode())

    if (user == None) or (m.hexdigest() != user["password_hash"]):
        return { "error": "Invalid username or password" }, 401
    
    token = generate_auth_token(user["_id"]["$oid"])

    return { "token": token.decode("utf-8") }, 200
