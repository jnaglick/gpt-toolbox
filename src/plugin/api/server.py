from flask import Flask, send_from_directory
from flask_cors import CORS

from db import Chroma, AbstractDocumentDatabase
from .routes import routes

from dataclasses import dataclass

@dataclass
class ServerContext:
    db: AbstractDocumentDatabase

def add_routes(server, routes):
    @server.route('/openapi.yaml')
    def serve_openapi_spec():
        return send_from_directory('../.well-known/', 'openapi.yaml')
    
    @server.route('/.well-known/ai-plugin.json')
    def serve_ai_plugin():
        return send_from_directory('../.well-known/', 'ai-plugin.json')

    resources = []

    for route in routes:
        resource = route(server)

        # TODO not exactly elegant, fix later
        if not isinstance(resource, list):
            resource = [resource]

        resources.extend(resource)
    
    return resources

def server():
    server = Flask(__name__)

    chroma = Chroma('memory')

    # TODO why isnt @server.before_first_request working?
    server.context = ServerContext(
        db=chroma
    )

    CORS(server)

    resources = add_routes(server, routes)

    return server, resources