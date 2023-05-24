from .datetime import datetime
from .tasks import tasks
from .search import search
from .shell import shell
from .url import url
from .random_number import random_number
from .memory import create_memory

routes = [
    datetime,
    *tasks,
    search,
    shell,
    url,
    random_number,
    create_memory,
]
