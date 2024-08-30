from fastapi import FastAPI
from typing import Optional
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from team_parse import getTeams,getDrivers
from weekend_parse import WeekendParser
from starlette.responses import FileResponse

app = FastAPI()
weekend_info = WeekendParser()
# Enable CORS
origins = [
    "http://localhost:8080",  # Vue.js dev server
    "http://0.0.0.0:8000",
    "http://0.0.0.0:8080",   # FastAPI server
    "http://localhost:8000",
    "https://f1-fantasy-model-backend.onrender.com",
    "https://f1-fantasy-model.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    raceLoc: Optional[str] = None
    session: Optional[str] = None
    constructor: Optional[str] = None
    driver1: Optional[str] = None
    driver2: Optional[str] = None
    driver1_pos: Optional[int] = None
    driver2_pos: Optional[int] = None
    data_override: Optional[bool] = None
    substitute_driver: Optional[bool] = None
    substitute_driver_name: Optional[str] = None
    substitute_driver_pos: Optional[int] = None

@app.get('/api/gp_locs/')
def send_gp_dropdown():
    return {'entity':weekend_info.gp_parse()}

@app.post('/api/sessions/')
def send_session_types(item: Item):
    print(item)
    return {'entity':weekend_info.sessions_parse(item.raceLoc)}

@app.get('/api/constructors/')
def send_constructors():
    return {'entity':getTeams()}

@app.post('/api/submit/')
def post_gp_dropdown(item: Item):
    inputs = {}
    print(item)
    for entity in list(item):
        inputs[entity[0]] = entity[1]
        if item.constructor in getTeams():
            drivers = getDrivers(item.constructor)
            inputs['driver1'] = drivers[0]
            inputs['driver2'] = drivers[1]
    print(f"{inputs}")
    return {"status": "success", "entity": inputs}

# Route to serve React index.html (for client-side routing)
@app.get("/{full_path:path}")
async def serve_app(full_path: str):
    return FileResponse("../f1_fantasy_ui/dist/index.html")

app.mount("/static", StaticFiles(directory="../f1_fantasy_ui/dist/",html=True))

if __name__ == '__main__':
    # print(team_parse.getDrivers(team='Redbull'))
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000)