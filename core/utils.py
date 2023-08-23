import tiktoken


def num_tokens(text: str, model_name: str) -> int:
    """Return the number of tokens in the given string."""
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(text))

def get_n_tokens(text: str, model_name: str, n: int = -1) -> str:
    """ Return the first n tokens of a string"""
    if n == -1:
        return text

    encoding = tiktoken.encoding_for_model(model_name)
    encoded = encoding.encode(text)
    encoded = encoded[:n]
    return encoding.decode(encoded)
