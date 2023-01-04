import sys
import xmlrpc.client

from flask import Flask

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 5000

app = Flask(__name__)
app.config["DEBUG"] = True

RPC_SERVER_URL = "http://localhost:9000/RPC2"

@app.route('/string_reverse', methods=['GET'])
def string_reverse():
    
    return "hello"

@app.route('/')
def hello():
    # Create an XML-RPC client
   

    # Return the server's response
    return 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
