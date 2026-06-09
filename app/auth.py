from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
import jwt, hashlib

SECRET = "your-secret-key"  # move to .env
security = HTTPBearer()

async def get_current_user(request: Request, db) -> str:
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Missing API key")
    
    key_hash = hashlib.sha256(token.encode()).hexdigest()
    api_key = await db.execute(
        select(APIKey).where(APIKey.key_hash == key_hash)
    )
    result = api_key.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return result.user_id