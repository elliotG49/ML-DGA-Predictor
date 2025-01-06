import zlib

def calculate_huffman_compression_ratio(input_string):
    """
    Calculate the Huffman compression ratio of a given string.
    
    Parameters:
        input_string (str): The input string to analyze.
        
    Returns:
        float: The compression ratio (compressed size / original size).
    """
    if not input_string:
        raise ValueError("Input string cannot be empty.")

    # Convert the string to bytes
    input_bytes = input_string.encode('utf-8')

    # Original size in bytes
    original_size = len(input_bytes)

    # Compress the string
    compressed_data = zlib.compress(input_bytes)

    # Compressed size in bytes
    compressed_size = len(compressed_data)

    # Calculate compression ratio
    compression_ratio = compressed_size / original_size

    return compression_ratio

# Example usage
input_string = input("Enter: ")
compression_ratio = calculate_huffman_compression_ratio(input_string)
print(f"Compression Ratio: {compression_ratio:.4f}")
