from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
origins = [
    "http://localhost:8080",  # Vue.js dev server
    "http://localhost:8000",
    "http://10.0.0.159:8000",
    "http://10.0.0.159:8080"   # FastAPI server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    raceName: str

@app.get('/api/get_list/')
def send_gp_dropdown():
    with open("./input_files/local_gp_list.txt","r+") as gp_list:
        gp_list = [item.split('\n')[0] for item in gp_list.readlines()]
    return {'entity':gp_list}

@app.post('/api/submit/')
def post_gp_dropdown(item: Item):
    entity = item.raceName
    print(f"{entity}")
    return {"status": "success", "entity": entity}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000)