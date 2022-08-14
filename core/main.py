from fastapi import FastAPI
from core.config import settings 
from core.user_auth import user_auth_router













app = FastAPI(
    title=settings.app_name,
    description="An attempt to automate bills.",
)



app.include_router(user_auth_router.auth)



@app.get("/")
def server_root()->dict:
    response = {
        "info": "This is the Root of the server: My name is Groot."
    }
    if settings.environment is None:
        response["docs"] = "/docs"
    return response
    
    
    
    
    
    
    
    