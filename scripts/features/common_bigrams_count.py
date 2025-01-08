def count_common_bigrams(domain: str, common_bigrams: set) -> int:
    """
    Count how many bigrams (pairs of consecutive chars) in 'domain'
    appear in the set 'common_bigrams'.
    """
    domain_lower = domain.lower()
    count = 0
    for i in range(len(domain_lower) - 1):
        bigram = domain_lower[i : i + 2]
        if bigram in common_bigrams:
            count += 1
    return count
