from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/token/access/{client_id}")
async def access_token(client_id: str):
    pass


@router.get("/token/refresh/{client_id}")
async def refresh_token(client_id: str):
    pass
