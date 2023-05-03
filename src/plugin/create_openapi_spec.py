from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
import yaml

def create_openapi_spec(app, resources, components):
    spec = APISpec(
        title="GPT Toolbox API",
        version="v1",
        info=dict(
            description="A ChatGPT plugin API for the GPT Toolbox",
        ),
        servers=[{
            "url": "http://localhost:3333"
        }],
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    with app.test_request_context():
        for resource in resources:
            spec.path(view=resource)

    for component in components:
        spec.components.schema(component.__name__, schema=component)

    # TODO compute route to yaml
    with open("./src/plugin/.well-known/openapi.yaml", "w") as f:
        yaml.dump(spec.to_dict(), f)
