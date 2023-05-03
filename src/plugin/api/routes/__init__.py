from .datetime import datetime
from .tasks import tasks
from .search import search
from .url import url

routes = [
    datetime,
    *tasks,
    search,
    url,
]
