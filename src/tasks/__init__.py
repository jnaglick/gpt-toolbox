from .dictionary import task_dictionary 

def task_to_prompt(task):
    name = task["name"]
    description = task["description"]
    parameters = task["parameters"]
    output = task["output"]

    return "\n".join([
        f"Name: \"{name}\"",
        f"Description: {description}",
        "Parameters:",
        "\n".join([f"- {param['name']}: {param['description']}" for param in parameters]),
        f"Outputs: {output['description']}"
    ]).strip()

task_prompt_segment = "\n\n".join([task_to_prompt(task) for _, task in task_dictionary.items()])
