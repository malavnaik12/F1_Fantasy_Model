from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
origins = [
    "http://localhost:8080",  # Vue.js dev server
    "http://localhost:8000"   # FastAPI server
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

@app.post('/api/submit/')
def post_gp_dropdown(item: Item):
    entity = item.raceName
    print(f"{entity}")
    return {"status": "success", "entity": entity}
    # with open("./input_files/local_gp_list.txt","r+") as gp_list:
    #     gp_locs = [item.split('\n')[0] for item in gp_list.readlines()]
    # return jsonify({"gp_locs": gp_locs})

# @app.get('/')
# def get_gp_name():
#     pass
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)