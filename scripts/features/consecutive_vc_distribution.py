def has_strict_vowel_consonant_pattern(domain: str) -> int:
    """
    Check if the domain has a strict alternating vowel-consonant pattern.
    Return 1 if yes, 0 otherwise.

    Example:
        "aBaCaDa" -> 1 (strictly alternates vowel/consonant)
        "google" -> 0 (because 'oo' are consecutive vowels)
    """
    vowels = set("aeiou")
    domain_lower = domain.lower()

    if not domain_lower:
        return 0

    # We'll ignore non-alphabetic chars for the pattern check, or treat them as breaks
    filtered = [ch for ch in domain_lower if ch.isalpha()]
    if not filtered:
        return 0

    # Check adjacency
    for i in range(len(filtered) - 1):
        current_is_vowel = filtered[i] in vowels
        next_is_vowel = filtered[i + 1] in vowels
        # If they are both vowels or both consonants, pattern breaks
        if current_is_vowel == next_is_vowel:
            return 0

    return 1
