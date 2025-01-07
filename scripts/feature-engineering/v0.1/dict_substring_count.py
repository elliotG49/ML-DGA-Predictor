def count_dictionary_substrings(domain: str, dictionary_set: set, min_length: int = 3) -> int:
    """
    Count how many distinct substrings (length >= min_length) of 'domain'
    appear in 'dictionary_set'.
    """
    domain_lower = domain.lower()
    found_substrings = set()

    for start_idx in range(len(domain_lower)):
        for end_idx in range(start_idx + min_length, len(domain_lower) + 1):
            substring = domain_lower[start_idx:end_idx]
            if substring in dictionary_set:
                found_substrings.add(substring)

    return len(found_substrings)
