import fastapi
from routes import constructors_routes, drivers_routes

app = fastapi.FastAPI(title="F1 Fantasy App Database")

app.include_router(constructors_routes.router)
app.include_router(drivers_routes.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)