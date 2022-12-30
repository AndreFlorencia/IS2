import signal, sys
import psycopg2
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.importarFicheiro import importarFicheiro
from functions.converterXML import converterXML
from functions.query1 import query1
from functions.query2 import query2
from functions.query3 import query3
from functions.query4 import query4
from functions.apagarFicherio import apagar
from functions.validarXML import validarXML
from functions.listarXML import listarXML


class RequestHandler(SimpleXMLRPCRequestHandler):
   rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 9000), requestHandler=RequestHandler,allow_none=True) as server:
   server.register_introspection_functions()


   def signal_handler(signum, frame):
      print("received signal")
      server.server_close()

      # perform clean up, etc. here...

      print("exiting, gracefully")
      sys.exit(0)

   # signals
   signal.signal(signal.SIGTERM, signal_handler)
   signal.signal(signal.SIGHUP, signal_handler)
   signal.signal(signal.SIGINT, signal_handler)

   # register both functions
   server.register_function(converterXML)
   server.register_function(importarFicheiro)
   server.register_function(listarXML)
   server.register_function(validarXML)
   server.register_function(query1)
   server.register_function(query2)
   server.register_function(query3)
   server.register_function(query4)
   server.register_function(apagar)

   # start the server
   print("Starting the RPC Server...")

   server.serve_forever()
