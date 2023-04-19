assistant = {
    "name": "assistant",
    "description": "Give another assistant a task to do, using some information you got from another task. The other assistant is not as smart or capable as you are. This should be kept as granular and simple as possible.",
    "parameters": [
        {
            "name": "task_description",
            "type": "string",
            "description": "The task to do."
        },
        {
            "name": "context",
            "type": "json string",
            "description": "Additional information the assistant will need to do the task. This must be a json string that can be parsed into a dictionary. Values in this dictionary may be \"<OUTPUT_OF>-dep_id\" references or static values."
        },
    ],
    "output": {
        "type": "string",
        "description": "Answer"
    }
}

google = {
    "name": "google",
    "description": "Search google",
    "parameters": [
        {
            "name": "query",
            "type": "string",
            "description": "The query to search for"
        }
    ],
    "output": {
        "type": "string",
        "description": "The URL of the top search result"
    }
}

web_request = {
    "name": "web_request",
    "description": "Make a web request",
    "parameters": [
        {
            "name": "url",
            "type": "string",
            "description": "The url to request"
        }
    ],
    "output": {
        "type": "string",
        "description": "The response body"
    }
}

write_to_file = {
    "name": "write_to_file",
    "description": "Write something to a file",
    "parameters": [
        {
            "name": "file_name",
            "type": "string",
            "description": "The name of the file to create and write to. If the file already exists, it will be overwritten."
        },
        {
            "name": "value",
            "type": "string",
            "description": "The value to write to the file."
        }
    ],
    "output": {
        "type": "string",
        "description": "The contents of the file"
    }
}

append_to_file = {
    "name": "append_to_file",
    "description": "Append something to a file",
    "parameters": [
        {
            "name": "file_name",
            "type": "string",
            "description": "The name of the file to append to. If the file doesn't exist, it will be created."
        },
        {
            "name": "value",
            "type": "string",
            "description": "The value to append to the file."
        }
    ],
    "output": {
        "type": "string",
        "description": "The contents of the file"
    }
}

read_from_file = {
    "name": "read_from_file",
    "description": "Read from a file",
    "parameters": [
        {
            "name": "file_name",
            "type": "string",
            "description": "The name to read from."
        },
    ],
    "output": {
        "type": "string",
        "description": "The contents of the file"
    }
}

evaluate_python = {
    "name": "evaluate_python",
    "description": "Execute a python function and get the result.",
    "parameters": [
        {
            "name": "code",
            "type": "string",
            "description": "A block of python code defining a single function to execute. The code must be a function that takes in a single argument, which will be the dictionary you pass to the `args` parameter. The function must return a string. You will get the result of the function return value."
        },
        {
            "name": "args",
            "type": "json string",
            "description": "The arguments that will be passed to the function. This must be a json string that can be parsed into a dictionary. Values in this dictionary may be \"<OUTPUT_OF>-dep_id\" references or static values."
        }
    ],
    "output": {
        "type": "string",
        "description": "The result of the python function"
    }
}


task_dictionary = {
    "assistant": assistant,
    "google": google,
    "web_request": web_request,
    "write_to_file": write_to_file,
    "append_to_file": append_to_file,
    "read_from_file": read_from_file,
    # "evaluate_python": evaluate_python
}