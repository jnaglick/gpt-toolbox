from flask import jsonify, request, abort

from utils import web_search

def search_action(search_term, relevance_summary_agent):
    search_results = web_search(search_term, num_results=8, relevance_summary_fn=relevance_summary_agent.prediction)

    return [
        {
            'title': title,
            'url': url,
            'body': body
        } for title, url, body in search_results
    ]

def search(server):
    relevance_summary_agent = server.context.agents['relevance_summary']

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

        return jsonify(search_action(request.json['query'], relevance_summary_agent)), 200
  
    return _search
