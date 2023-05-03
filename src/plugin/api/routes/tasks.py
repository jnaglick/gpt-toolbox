import uuid

from flask import jsonify, request, abort

class TaskService:
    def __init__(self):
        self.tasks = {}

    def get_all_tasks(self):
        return list(self.tasks.values())

    def get_task(self, task_uuid):
        return self.tasks.get(task_uuid)

    def create_task(self, task_data):
        task_uuid = str(uuid.uuid4())
        item = {
            'uuid': task_uuid,
            'task': task_data['task'],
            'status': task_data['status'],
            'notes': task_data['notes']
        }
        self.tasks[task_uuid] = item
        return item

    def update_task(self, task_uuid, task_data):
        item = self.tasks.get(task_uuid)
        if item is None:
            return None

        item['task'] = task_data.get('task', item['task'])
        item['status'] = task_data.get('status', item['status'])
        item['notes'] = task_data.get('notes', item['notes'])

        self.tasks[task_uuid] = item
        return item

    def delete_task(self, task_uuid):
        if task_uuid in self.tasks:
            del self.tasks[task_uuid]
            return True
        return False

task_service = TaskService()

def index(server):
    @server.route('/tasks', methods=['GET'])
    def _index():
        """List all Task items
        ---
        get:
            operationId: listTasks
            summary: List all Task items
            responses:
                200:
                    description: List of Task items
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                    $ref: '#/components/schemas/Task'
        """
        return jsonify(task_service.get_all_tasks())

    return _index

def get(server):
    @server.route('/tasks/<string:task_uuid>', methods=['GET'])
    def _get(task_uuid):
        """Get a specific Task item by UUID
        ---
        get:
            operationId: getTask
            summary: Get a specific Task item by UUID
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
        """Create a Task item
        ---
        post:
            operationId: createTask
            summary: Create a new Task item
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
                                $ref: '#/components/schemas/Task'

                400:
                    description: Invalid input, a required field is missing
        """
        if not request.json or 'task' not in request.json or 'status' not in request.json or 'notes' not in request.json:
            abort(400)

        task = task_service.create_task(request.json)
        return jsonify(task), 201

    return _post

def put(server):
    @server.route('/tasks/<string:task_uuid>', methods=['PUT'])
    def _put(task_uuid):
        """Update a Task item by UUID
        ---
        put:
            operationId: updateTask
            summary: Update a Task item by UUID. At least one field must be provided, but you can also update multiple fields at once.
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
                                $ref: '#/components/schemas/Task'

                400:
                    description: Invalid input, at least one field must be provided
        """
        if not request.json or not any(field in request.json for field in ('task', 'status', 'notes')):
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
            summary: Delete a Task item by UUIDS. Prefer to update the status to 'cancelled' instead of deleting. Only use this when you are sure you want to delete the item.
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

tasks = [index, get, post, put, delete]
