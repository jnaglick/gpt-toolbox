from .api import server, schema_components
from .create_openapi_spec import create_openapi_spec

def start_server():
    server_instance, resources = server()

    create_openapi_spec(server_instance, resources, schema_components)
    
    server_instance.run(port=3333, use_reloader=False)
