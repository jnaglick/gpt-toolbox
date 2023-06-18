import uuid

from flask import jsonify, request, abort

from utils import console, run_shell_command

def create_task_script(code, task_uuid):
    script_filename = f"{task_uuid}.py"

    with open(script_filename, "w") as script_file:
        script_file.write(code)

    console.verbose(f"Created/Updated task: {task_uuid}")

class TaskService:
    def __init__(self):
        self.tasks = {}

    def get_all_tasks(self):
        return [{k: v for k, v in task.items() if k != 'code'} for task in self.tasks.values()]

    def get_task(self, task_uuid):
        return self.tasks.get(task_uuid)

    def create_task(self, task_data):
        task_uuid = str(uuid.uuid4())

        create_task_script(task_data['code'], task_uuid)

        item = {
            'uuid': task_uuid,
            'task': task_data['task'],
            'desc': task_data['desc'],
            'notes': task_data['notes'],
            'code': task_data['code'],
        }
        self.tasks[task_uuid] = item
        
        return {k: v for k, v in item.items() if k != 'code'}

    def update_task(self, task_uuid, task_data):
        item = self.tasks.get(task_uuid)
        if item is None:
            return None

        if item['code'] != task_data['code']:
            create_task_script(task_data['code'], task_uuid)

        item['task'] = task_data.get('task', item['task'])
        item['desc'] = task_data.get('desc', item['desc'])
        item['notes'] = task_data.get('notes', item['notes'])
        item['code'] = task_data.get('code', item['code'])
        self.tasks[task_uuid] = item

        return {k: v for k, v in item.items() if k != 'code'}

    def delete_task(self, task_uuid):
        if task_uuid in self.tasks:
            del self.tasks[task_uuid]
            return True
        return False
    
    def run_task(self, task_uuid, args=''):
        script_filename = f"{task_uuid}.py"
        console.verbose(f"Running task: {task_uuid}")
        return run_shell_command(f"python3 {script_filename} {args}")

task_service = TaskService()

def index(server):
    @server.route('/tasks', methods=['GET'])
    def _index():
        """Lists existing tasks. Its very important to know what you can do. A task is a special function you can run to augment your power for the user! This doesnt tell you the tasks code
        ---
        get:
            operationId: listTasks
            summary: Lists existing tasks. Its very important to know what you can do. A task is a special function you can run to augment your power for the user! This doesnt tell you the tasks code
            responses:
                200:
                    description: List of Tasks without code.
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                    $ref: '#/components/schemas/TaskWithoutCode'
        """
        return jsonify(task_service.get_all_tasks())

    return _index

def get(server):
    @server.route('/tasks/<string:task_uuid>', methods=['GET'])
    def _get(task_uuid):
        """Get a specific Task by UUID. This is the way to see the code behind a task. Useful if you need to fix it. This just tells you about the task, it does not let you run it.
        ---
        get:
            operationId: getTask
            summary: Get a specific Task by UUID. This is the way to see the code behind a task. Useful if you need to fix it. This just tells you about the task, it does not let you run it.
            parameters:
              - in: path
                name: task_uuid
                schema:
                    type: string
                required: true
                description: Unique identifier of the Task item
            responses:
                200:
                    description: Task item found
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/Task'
                404:
                    description: Task item not found
        """
        task = task_service.get_task(task_uuid)
        if task:
            return jsonify(task)
        abort(404)

    return _get

def post(server):
    @server.route('/tasks', methods=['POST'])
    def _post():
        """Create a Task item. A task is a special function you can run to augment your power for the user! ATTENTION Its very important to make sure the code is a complete standalone executable python script.
        ---
        post:
            operationId: createTask
            summary: Create a Task item. A task is a special function you can run to augment your power for the user! ATTENTION Its very important to make sure the code is a complete standalone executable python script.
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/CreateTaskRequest'
            responses:
                201:
                    description: Task item created
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/TaskWithoutCode'
                400:
                    description: Invalid input, a required field is missing
        """
        if not request.json or \
        'task' not in request.json or\
        'desc' not in request.json or\
        'notes' not in request.json or\
        'code' not in request.json:
            abort(400)

        task = task_service.create_task(request.json)
        return jsonify(task), 201

    return _post

def put(server):
    @server.route('/tasks/<string:task_uuid>', methods=['PUT'])
    def _put(task_uuid):
        """Update a Task. Use this to fix a broken task. Only specify the fields that need to be updating. ATTENTION its very important to make sure the code is a complete standalone executable python script.
        ---
        put:
            operationId: updateTask
            summary: Update a Task. Use this to fix a broken task. Only specify the fields that need to be updating. ATTENTION its very important to make sure the code is a complete standalone executable python script.
            parameters:
              - in: path
                name: task_uuid
                schema:
                    type: string
                required: true
                description: UUID of the Task
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/UpdateTaskRequest'
            responses:
                200:
                    description: Task item updated
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/TaskWithoutCode'
                400:
                    description: Invalid input, at least one field must be provided
        """
        if not request.json:
            abort(400)

        updated_task = task_service.update_task(task_uuid, request.json)
        if updated_task:
            return jsonify(updated_task)

        abort(404)

    return _put

def delete(server):
    @server.route('/tasks/<string:task_uuid>', methods=['DELETE'])
    def _delete(task_uuid):
        """Delete a Task item by UUID
        ---
        delete:
            operationId: deleteTask
            summary: Delete a Task item by UUIDS. Only use this when you are sure you want to delete a task.
            parameters:
              - in: path
                name: task_uuid
                schema:
                    type: string
                required: true
                description: Unique identifier of the Task
            responses:
                200:
                    description: Task item deleted
                404:
                    description: Task item not found
        """
        if task_service.delete_task(task_uuid):
            return jsonify({"result": "Task deleted"})

        abort(404)

    return _delete

def run(server):
    @server.route('/tasks/<string:task_uuid>/run', methods=['POST'])
    def _run(task_uuid):
        """Runs a specific Task and gets the results. Before you run tasks, look at the task list to find the best one for the job.
        ---
        post:
            operationId: runTask
            summary: Runs a specific Task and gets the results. Before you run tasks, look at the task list to find the best one for the job.
            parameters:
              - in: path
                name: task_uuid
                schema:
                    type: string
                required: true
                description: Unique identifier of the Task item
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/RunTaskRequest'
            responses:
                200:
                    description: Task item was ran
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/ShellResult'
                404:
                    description: Task item not found
        """
        task = task_service.get_task(task_uuid)
        if task:
            return jsonify(task_service.run_task(task['uuid'], ' '.join(request.json['args'])))
        abort(404)

    return _run

task_routes = [index, get, post, put, delete, run]
