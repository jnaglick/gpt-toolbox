import openai

def generate_embedding(text, model="text-embedding-ada-002"):
    """
    Generate an embedding for the given text using the specified model.

    Args:
        text (str): The input text for which to generate the embedding.
        model (str): The model to use for generating the embedding. Default is "text-embedding-ada-002".

    Returns:
        list: The generated embedding as a list of floating-point numbers.
    """
    response = openai.Embedding.create(input=text, model=model)
    embedding = response["data"][0]["embedding"]
    return embedding
