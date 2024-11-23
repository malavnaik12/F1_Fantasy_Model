from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from positions_routes import router as pos_router
from prices_routes import router as prices_router
from ga_inputs_routes import router as ga_inputs_router
from team_generate_routes import router as generate_team_router

app = FastAPI()
# Enable CORS
origins = [
    "http://localhost:8080",
    "http://localhost:8000",
    "https://f1-fantasy-model-backend.onrender.com",
    "https://f1-fantasy-model.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pos_router, prefix="/positions")
app.include_router(prices_router, prefix="/prices")
app.include_router(ga_inputs_router, prefix="/inputs")
app.include_router(generate_team_router, prefix="/generate")


# Route to serve React index.html (for client-side routing)
@app.get("/{full_path:path}")
async def serve_app(full_path: str):
    return FileResponse("../f1_fantasy_ui/dist/index.html")


app.mount("/static", StaticFiles(directory="../f1_fantasy_ui/dist/", html=True))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
