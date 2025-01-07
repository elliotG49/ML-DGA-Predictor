def longest_dictionary_word(domain: str, dictionary_set: set) -> int:
    """
    Find the length of the longest word within 'domain' that appears in 'dictionary_set'.
    Returns 0 if no dictionary word is found.

    Assumes dictionary_set is a Python set of valid words.
    """
    domain_lower = domain.lower()
    max_length = 0

    # Optional: Remove TLDs or punctuation, if desired. For now, use domain as-is.

    # Check all substrings
    for start_idx in range(len(domain_lower)):
        for end_idx in range(start_idx + 1, len(domain_lower) + 1):
            substring = domain_lower[start_idx:end_idx]
            if substring in dictionary_set and len(substring) > max_length:
                max_length = len(substring)

    return max_length
