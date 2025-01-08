import random
import string

def dga_dircrypt(num_domains=10, wordlist=None):
    """
    Generate domains by mixing dictionary words + random strings.
    """
    if wordlist is None:
        # Example default wordlist
        wordlist = ["apple", "banana", "cat", "dog", "error", "zebra"]

    domains = []
    for _ in range(num_domains):
        # Random dictionary word
        word = random.choice(wordlist)
        
        # Insert random letters
        random_part = ''.join(random.choices(string.ascii_lowercase, k=5))
        
        # Combine them
        domain = f"{random_part}{word}{random_part}"
        domains.append(domain)
    return domains

if __name__ == "__main__":
    file_path = "/root/project-mitnick/datasets/new-dga-domains.txt"
    dga_domains = dga_dircrypt(num_domains=500)
    print("\nDirCrypt-like DGA domains:")
    f = open(file_path, "w")
    for d in dga_domains:
        f.write(d + "\n")
    f.close()
        
        
