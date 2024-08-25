from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.templating import Jinja2Templates
from src import team_parse
from starlette.responses import FileResponse
import os
from fastapi.requests import Request

app = FastAPI()

# Enable CORS
origins = [
    "http://localhost:8080",  # Vue.js dev server
    "http://0.0.0.0:8000",
    "http://0.0.0.0:8080",   # FastAPI server
    "http://localhost:8000",
]
# templates = Jinja2Templates(directory="../ui/build")
# Serve the static files from the 'dist' directory
app.mount("/static", StaticFiles(directory="./f1_fantasy_ui/dist/"), name="static")
# @app.get("/")
# async def serve_frontend():
#     return FileResponse(os.path.join("dist", "index.html"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    raceLoc: str
    session: str
    constructor: str
    driver1: str
    driver2: str
    driver1_pos: int 
    driver2_pos: int
    # data_override: bool
    # substitute_driver: bool
    # substitute_driver_name: str
    # substitute_driver_pos: int

class utils():
    def _parse_list(file_name: str):
        with open(f"./input_files/{file_name}","r+") as item_list:
            return [item.split('\n')[0] for item in item_list.readlines()]

@app.get('/api/gp_locs/')
def send_gp_dropdown():
    return {'entity':utils._parse_list("list_gp_locs.txt")}

@app.get('/api/sessions/')
def send_session_types():
    return {'entity':utils._parse_list("list_session_types.txt")}

@app.get('/api/constructors/')
def send_constructors():
    return {'entity':team_parse.getTeams()}

# @app.post('/api/selected_constructor/')
# def get_constructors(item: Item):
#     print(team_parse.getDrivers(item.constructor))
#     return {"status": "success", "entity": item}
    # return {'entity':team_parse.getDrivers(item.constructor)}

@app.post('/api/submit/')
def post_gp_dropdown(item: Item):
    inputs = {}
    print(item)
    for entity in list(item):
        inputs[entity[0]] = entity[1]
        if item.constructor in team_parse.getTeams():
            drivers = team_parse.getDrivers(item.constructor)
            inputs['driver1'] = drivers[0]
            inputs['driver2'] = drivers[1]
    print(f"{inputs}")
    return {"status": "success", "entity": inputs}

# Defines a route handler for `/*` essentially.
# NOTE: this needs to be the last route defined b/c it's a catch all route
# @app.get("/{rest_of_path:path}")
# async def vue_app(req: Request, rest_of_path: str):
#     return templates.TemplateResponse('index.html', { 'request': req })

# Route to serve React index.html (for client-side routing)
@app.get("/{catchall:path}")
async def serve_app(catchall: str):
    return FileResponse("f1_fantasy_ui/dist/index.html")

if __name__ == '__main__':
    # print(team_parse.getDrivers(team='Redbull'))
    import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)