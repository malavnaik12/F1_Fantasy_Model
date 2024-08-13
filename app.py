from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.post('/')
def post_gp_dropdown():
    with open("./input_files/local_gp_list.txt","r+") as gp_list:
        gp_locs = [item.split('\n')[0] for item in gp_list.readlines()]
    return jsonify({"gp_locs": gp_locs})

# @app.get('/')
# def get_gp_name():
#     pass
if __name__ == '__main__':
    app.run(debug=True)