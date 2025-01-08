import heapq
from collections import Counter

def huffman_compression_ratio(s: str) -> float:
    """
    Calculate the Huffman compression ratio of string s.
    The ratio = (uncompressed size in bits) / (compressed size in bits).
    If the string is empty or has only one unique character, returns 1.0.
    """

    if len(s) <= 1:
        # If string is empty or only 1 char, Huffman won't compress meaningfully
        # Return ratio = 1.0
        return 1.0

    # Frequency of each character
    freq = Counter(s)

    # Create a node structure for the Huffman tree
    class Node:
        def __init__(self, freq, char=None, left=None, right=None):
            self.freq = freq
            self.char = char
            self.left = left
            self.right = right

        # For priority queue comparisons
        def __lt__(self, other):
            return self.freq < other.freq

    # Build a forest of single-character nodes
    forest = []
    for char, f in freq.items():
        forest.append(Node(f, char))
    heapq.heapify(forest)

    # Build Huffman tree by merging the two smallest subtrees repeatedly
    while len(forest) > 1:
        n1 = heapq.heappop(forest)
        n2 = heapq.heappop(forest)
        merged = Node(n1.freq + n2.freq, None, n1, n2)
        heapq.heappush(forest, merged)

    # The remaining element is the root of the Huffman tree
    root = forest[0]

    # Traverse the Huffman tree to determine code lengths
    code_lengths = {}

    def traverse(node, depth):
        # If it's a leaf node, store the depth
        if node.char is not None:
            code_lengths[node.char] = depth
            return
        # Otherwise traverse children
        if node.left:
            traverse(node.left, depth + 1)
        if node.right:
            traverse(node.right, depth + 1)

    traverse(root, 0)

    # Calculate the weighted average code length
    total_code_length = 0
    total_chars = len(s)
    for char, f in freq.items():
        total_code_length += f * code_lengths[char]

    # Average code length in bits
    avg_code_length = total_code_length / total_chars

    # Uncompressed size (8 bits per character)
    uncompressed_bits = total_chars * 8
    # Compressed size (avg_code_length bits per character)
    compressed_bits = total_chars * avg_code_length

    if compressed_bits == 0:
        return 1.0

    # Huffman compression ratio
    return uncompressed_bits / compressed_bits
