from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
origins = [
    "http://localhost:8080",  # Vue.js dev server
    "http://10.0.0.159:8000",
    "http://10.0.0.159:8080",   # FastAPI server
    "http://localhost:8000",
]

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
    # data_override: bool
    # constructor: str
    # driver1: str
    # driver2: str
    # driver1_pos: int 
    # driver2_pos: int
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

@app.post('/api/submit/')
def post_gp_dropdown(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    print(f"{inputs}")
    return {"status": "success", "entity": inputs}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000)