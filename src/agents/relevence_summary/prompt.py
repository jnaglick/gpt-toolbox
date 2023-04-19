def relevence_summary(query, text_to_summarize): return f"""
Given this query:
{query}
Give a very brief summary of the relevant information from this result:
{text_to_summarize}
""".strip()

def relevence_summary_with_thoughts(query, thoughts, text_to_summarize): return f"""
Given this query:
{query}
I 
Give a very brief summary of the relevant information from this result:
{text_to_summarize}
""".strip()
