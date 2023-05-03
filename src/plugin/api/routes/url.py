from utils import web_request

from flask import jsonify, request, abort

def url_action(url):
    if url.startswith("https://"):
        url = url.replace("https://", "http://")
    return web_request(url)

def url(server):
    @server.route('/url', methods=['POST'])
    def _url():
        """
        ---
        post:
            operationId: url
            summary: Look up something on the web. This will access the url and return the results.
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/UrlRequest'
            responses:
                200:
                    description: Result
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/UrlResult'
                400:
                    description: Invalid input, a required field is missing

        """
        if not request.json or 'url' not in request.json:
            abort(400)

        body = url_action(request.json['url'])

        return jsonify({
            'body': body
        }), 200
  
    return _url
