from utils import run_shell_command

from flask import jsonify, request, abort

def shell(server):
    @server.route('/shell', methods=['POST'])
    def _shell():
        """
        ---
        post:
            operationId: shell
            summary: Run a shell command on the user's machine and see the results. This can be used for many different things - get creative! ATTENTION NEVER Use This To Edit Files - Always Try Using edit_* Instead!
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/ShellRequest'
            responses:
                200:
                    description: Shell result
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/ShellResult'
                400:
                    description: Invalid input, a required field is missing
        """
        if not request.json or 'command' not in request.json:
            abort(400)

        return jsonify(run_shell_command(request.json['command'])), 200
  
    return _shell
