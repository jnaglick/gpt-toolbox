from .tasks import routes as tasks_routes
from .search import search
from .url import url

routes = [
    *tasks_routes,
    search,
    url,
]
