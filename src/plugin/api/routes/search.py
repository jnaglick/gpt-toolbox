from utils import duckduckgo, web_request

from flask import jsonify, request, abort

def search_action(search_term, num_results=3):
    search_results = duckduckgo(search_term, num_results)
    page_results = [web_request(url) for _, url in search_results]

    return [
        {
            'title': title,
            'url': url,
            'body': body
        } for (title, url), body in zip(search_results, page_results)
    ]

def search(server):
    @server.route('/search', methods=['POST'])
    def _search():
        """
        ---
        post:
            operationId: search
            summary: Search the web for something. This will execute a web search and return the results.
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/SearchRequest'
            responses:
                200:
                    description: Search result
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                    $ref: '#/components/schemas/SearchResult'
                400:
                    description: Invalid input, a required field is missing
        """
        if not request.json or 'query' not in request.json:
            abort(400)

        return jsonify(search_action(request.json['query'], num_results=3)), 200
  
    return _search
