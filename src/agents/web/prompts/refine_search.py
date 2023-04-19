def refine_search(query, results): return f"""
Given this query:
{query}
Give a very brief summary of the relevant information from this result:
{results}
""".strip()
