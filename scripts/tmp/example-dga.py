import random

def dga(seed):
    domains = []
    for i in range(100):  # Generate 100 domains
        random.seed(seed + i)
        domain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8)) + ".com"
        domains.append(domain)
    return domains

print(dga(203423))
