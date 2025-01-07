import math

def calculate_string_entropy(s: str) -> float:
    """
    Calculate the Shannon entropy of a string s.
    Entropy measures the unpredictability of characters in the string.
    """
    if not s:
        return 0.0

    # Count frequency of each character
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1

    # Compute entropy
    entropy = 0.0
    length = len(s)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)

    return entropy
