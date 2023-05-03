from .datetime import datetime
from .tasks import tasks
from .search import search
from .shell import shell
from .url import url

routes = [
    datetime,
    *tasks,
    search,
    shell,
    url,
]
