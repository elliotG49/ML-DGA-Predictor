def frequency_of_numbers(domain: str) -> float:
    """
    Return the ratio (frequency) of digits to total length of domain.
    E.g., for 'abc123', ratio = 3/6 = 0.5
    """
    if not domain:
        return 0.0
    digit_count = sum(ch.isdigit() for ch in domain)
    return digit_count / len(domain)
