import json

def verify_plan(plan_str, task_dictionary):
    try:
        # if the plan is invalid because tasks have duplicate keys, doing this silently eats that problems. But, not sure how to fix...
        task_list = json.loads(plan_str)
    except json.JSONDecodeError:
        print("Error: Invalid JSON output")
        return False

    task_ids = set()

    for task in task_list:
        task_dictionary_entry = task_dictionary[task["task"]]

        # check task exists:
        if not task_dictionary_entry:
            print("Error: Invalid task name (task doesnt exist)", task)
            return False

        # Check if required keys are present in the task
        if not all(key in task for key in ("task", "id", "dep", "args")):
            print("Error: Missing required keys in task for task", task)
            return False

        # check if task id is numeric:
        try:
            int(task["id"])
        except ValueError:
            print("Error: Task id is not an int", task)
            return False

        # Check if task id is unique
        if task["id"] in task_ids:
            print("Error: Duplicate task id", task)
            return False
        task_ids.add(task["id"])

        # Check if all dependencies are valid
        for dep_id in task["dep"]:
            if dep_id not in task_ids:
                print("Error: Invalid dependency id", task)
                return False

        # Check args are 1:1 with parameters
        parameter_names = set(p["name"] for p in task_dictionary_entry["parameters"])
        if set(task["args"].keys()) != parameter_names:
            print("Error: Arguments dont match parameters", task)
            return False

        # Check if all args are valid
        for arg_key, arg_value in task["args"].items():
            parameter_definition = next(p for p in task_dictionary_entry["parameters"] if p["name"] == arg_key)
            if parameter_definition["type"] == "json string":
                if not isinstance(arg_value, dict):
                    print("Error: Invalid JSON string (not a dict)", task)
                    return False
                
                if not all(isinstance(key, str) for key in arg_value.keys()):
                    print("Error: Invalid JSON string (keys not strings)", task)
                    return False
                
                # Check <OUTPUT_OF>-dep_id references in json payload
                for v in arg_value.values():
                    if isinstance(v, str) and v.startswith("<OUTPUT_OF>-"):
                        dep_id = v.split("-")[-1]
                        try:
                            dep_id_int = int(dep_id)
                        except ValueError:
                            print("Error: Invalid <OUTPUT_OF> reference in json (dep_id not an int)", task)
                            return False
                        if dep_id_int not in task["dep"]:
                            print("Error: Invalid <OUTPUT_OF> reference in json (dep_id not in dep list)", task)
                            return False

            # Check if all args are using the correct <OUTPUT_OF>-dep_id format
            if isinstance(arg_value, str) and arg_value.startswith("<OUTPUT_OF>-"):
                dep_id = arg_value.split("-")[-1]
                try:
                    dep_id_int = int(dep_id)
                except ValueError:
                    print("Error: Invalid <OUTPUT_OF> reference (dep_id not an int)", task)
                    return False
                if dep_id_int not in task["dep"]:
                    print("Error: Invalid <OUTPUT_OF> reference (dep_id not in dep list)", task)
                    return False

    return True