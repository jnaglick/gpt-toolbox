from server import server, resources, components
from create_openapi_spec import create_openapi_spec

def start_plugin_server():
    create_openapi_spec(server, resources, components)
    server.run(debug=True, port=3333)
