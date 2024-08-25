import sys
from os.path import dirname, abspath

project_home = u'/home/mnaik/F1_Fantasy_Model'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from uvicorn import Config, Server
import app  # Replace with your app's import path

config = Config(app=app, host="0.0.0.0", port=8000, log_level="info")
server = Server(config)

if __name__ == "__main__":
    server.run()
