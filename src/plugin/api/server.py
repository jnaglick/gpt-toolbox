from dataclasses import dataclass

from flask import Flask, send_from_directory
from flask_cors import CORS

from agents.few_shot import RelevanceSummaryAgent
from db import Chroma, AbstractDocumentDatabase
from .routes import routes

@dataclass
class ServerContext:
    agents: dict
    db: AbstractDocumentDatabase
    db_long_term: AbstractDocumentDatabase

def add_routes(server, routes):
    @server.route('/openapi.yaml')
    def serve_openapi_spec():
        return send_from_directory('../.well-known/', 'openapi.yaml')
    
    @server.route('/.well-known/ai-plugin.json')
    def serve_ai_plugin():
        return send_from_directory('../.well-known/', 'ai-plugin.json')

    @server.route('/logo.png')
    def serve_ico():
        return send_from_directory('../.well-known/', 'logo.png')

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

    agents = {
        'relevance_summary': RelevanceSummaryAgent("🧰 plugin: RelevanceSummaryAgent")
    }

    # TODO get db locations from env    
    db = Chroma('toolbox-memory-general', "/Users/jmn/chroma/toolbox-memory-general")
    db_long_term = Chroma('toolbox-memory-long-term', "/Users/jmn/chroma/toolbox-memory-long-term")

    #print(f"Plugin memory initialized. short_term: {db.collection.count()}, long_term: {db_long_term.collection.count()}")
    # print(db.query("route"))

    server.context = ServerContext(
       agents=agents,
       db=db,
       db_long_term=db_long_term
    )

    CORS(server)

    resources = add_routes(server, routes)

    return server, resources