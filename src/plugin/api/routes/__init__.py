from .datetime import datetime
from .tasks import task_routes
from .search import search
from .shell import shell
from .url import url
from .random_number import random_number
from .memory import memory 
from .vim_ex import vim_ex

routes = [
    datetime,
    *task_routes,
    search,
    shell,
    url,
    random_number,
    memory,
    vim_ex,
]
