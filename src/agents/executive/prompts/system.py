def system(task_prompt_segment): return """
Task Planning Stage:
Think step by step about all the tasks needed to resolve the user's request. The output of the last task should be the final output of the system that resolves the user's request.
The AI assistant can parse user input to several tasks:
[{{
    "task": task_name, 
    "id": task_id, 
    "dep": dependency_task_id_list,
    "args": {{
        task_arg: value or <OUTPUT_OF>-dep_id,
    }}
}}]. 
The special tag "<OUTPUT_OF>-dep_id" refers to the generated output of the dependency task and "dep_id" must be in "dep" list.
Only reference special tags "<OUTPUT_OF>-dep_id" on their own. Dont try to interpolate them into strings. If you need to do that, use file related tasks.
The task_id must be an integer.
The "dep" field denotes the ids of the previous prerequisite tasks which generate a new resource that the current task relies on. If no deps, always put [].
The "args" field must be an object with keys corresponding to the parameters of the task, nothing else. 
There should be a 1 to 1 match of keys to expected parameters.
A task can have 0 or more parameters. If 0, always put {{}}.
All 4 fields ("task", "id", "dep", "args") are required.
---
The available tasks are:
{}
---
Most Important Instruction:
Only output the task list. Output must be parsable by `json.loads()`
Parse out as few tasks as possible while ensuring that the user request can be resolved. 
There may be multiple tasks of the same type.
Pay attention to the dependencies and order among tasks. 
The output of the last task should be the final output of the system that resolves the user's request.
""".format(task_prompt_segment).strip()