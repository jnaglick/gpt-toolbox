import json

def task(task_name, task_id, dependencies, arguments):
    return {
        "task": task_name,
        "id": task_id,
        "dep": dependencies,
        "args": arguments
    }

mets_plan = [
    task(
        "google",
        0,
        [],
        {
            "query": "Mets schedule"
        }
    ),
    task(
        "web_request",
        1,
        [0],
        {
            "url": "<OUTPUT_OF>-0"
        }
    ),
    task(
        "assistant",
        2,
        [1],
        {
            "task_description": "Read this mets schedule and figure out who the Mets are playing today",
            "context": {
                "schedule": "<OUTPUT_OF>-1"
            }
        }
    )
]

def examples():
    return [
        [
            "Who are the mets playing today",
            json.dumps(mets_plan, indent=4)
        ]
    ]
