# from .datetime import datetime
from .edit import edit_routes
from .tasks import task_routes
from .search import search
from .shell import shell
from .url import url
# from .random_number import random_number
from .memory import memory 
from .vim import vim

routes = [
    # datetime,
    *edit_routes,
    *task_routes,
    search,
    shell,
    url,
    # random_number,
    memory,
    vim,
]
