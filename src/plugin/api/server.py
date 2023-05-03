from flask import Flask, send_from_directory
from flask_cors import CORS

from .routes import routes

def add_routes(server, routes):
    @server.route('/openapi.yaml')
    def serve_openapi_spec():
        return send_from_directory('./.well-known/', 'openapi.yaml')
    
    @server.route('/.well-known/ai-plugin.json')
    def serve_ai_plugin():
        return send_from_directory('./.well-known/', 'ai-plugin.json')

    resources = []

    for route in routes:
        resources.append(route(server))
    
    return resources

def server():
    server = Flask(__name__)

    CORS(server)

    resources = add_routes(server, routes)

    return server, resources