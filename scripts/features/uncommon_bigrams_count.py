def count_uncommon_bigrams(domain: str, uncommon_bigrams: set) -> int:
    """
    Count how many bigrams (pairs of consecutive chars) in 'domain'
    appear in the set 'uncommon_bigrams'.
    """
    domain_lower = domain.lower()
    count = 0
    for i in range(len(domain_lower) - 1):
        bigram = domain_lower[i : i + 2]
        if bigram in uncommon_bigrams:
            count += 1
    return count
