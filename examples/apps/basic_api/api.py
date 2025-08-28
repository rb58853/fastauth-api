from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastauth import Fastauth

app = FastAPI(root_path="/test-api")
auth = Fastauth()
auth.set_auth(app)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/access/health")
async def access_health_check():
    return {"status": "healthy", "service": "access health that need access token"}


@app.get("/master/health")
async def master_health_check():
    return {"status": "healthy", "service": "master health that need master token"}
