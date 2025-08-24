from fastapi import FastAPI
from jsondb import router

app = FastAPI(root_path="/mydb")
app.include_router(router=router)
