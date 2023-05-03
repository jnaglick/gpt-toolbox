from .tasks import routes as tasks_routes
from .search import search

routes = [
    *tasks_routes,
    search
]
