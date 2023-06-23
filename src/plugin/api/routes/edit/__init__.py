from .edit_replace_line import replace_line
from .edit_insert_line import insert_line
from .edit_file_view import file_view

edit_routes = [
    replace_line,
    insert_line,
    file_view,
]