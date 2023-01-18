import sys
import xmlrpc.client
from flask_cors import CORS

from flask import Flask

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 5000

app = Flask(__name__)
app.config["DEBUG"] = True

server = xmlrpc.client.ServerProxy("http://rpc-server:9000")

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route("/api/regions", methods=['GET'])
def find_region():
    data = server.query1()
    return data, 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
