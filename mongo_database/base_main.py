import fastapi
from routes import base_routes

app = fastapi.FastAPI()

app.include_router(base_routes.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)