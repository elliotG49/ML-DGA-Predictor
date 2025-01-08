import csv

from string_entropy import calculate_string_entropy
from huffman_compression_ratio import huffman_compression_ratio
from string_length import domain_length
from longest_dict_word import longest_dictionary_word
from dict_substring_count import count_dictionary_substrings
from consecutive_vc_distribution import has_strict_vowel_consonant_pattern
from uncommon_bigrams_count import count_uncommon_bigrams
from common_bigrams_count import count_common_bigrams
from number_frequency import frequency_of_numbers


def load_dictionary(dictionary_csv_path: str) -> set:
    """
    Load English words from a CSV into a set.
    Assumes one word per line or a column containing words.
    Adjust parsing as needed.
    """
    dictionary_set = set()
    with open(dictionary_csv_path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word:
                dictionary_set.add(word.lower())
    return dictionary_set

def load_bigrams(bigrams_csv_path: str) -> set:
    """
    Load bigrams from a CSV into a set.
    Assumes one bigram per line or a column containing bigrams.
    Adjust parsing as needed.
    """
    bigrams_set = set()
    with open(bigrams_csv_path, 'r', encoding='utf-8') as f:
        for line in f:
            bigram = line.strip()
            if bigram:
                bigrams_set.add(bigram.lower())
    return bigrams_set


def main():
    # Example file paths (adjust to your actual paths)
    dict_file_path = "/root/project-mitnick/dictionaries/"
    dataset_file_path = "/root/project-mitnick/datasets/"
    domain_csv_path = f"{dataset_file_path}dga_data.csv"                     # Input CSV with a column "domain"
    output_csv_path = f"{dataset_file_path}domains_with_features_v01.csv"       # Output CSV
    english_dict_path = f"{dict_file_path}english_wordlist.csv"        # CSV with English words
    common_bigrams_path = f"{dict_file_path}common_bigrams.csv"          # CSV with frequent bigrams
    uncommon_bigrams_path = f"{dict_file_path}uncommon_bigrams.csv"      # CSV with rare bigrams

    # Load the supporting data
    dictionary_set = load_dictionary(english_dict_path)
    common_bigrams_set = load_bigrams(common_bigrams_path)
    uncommon_bigrams_set = load_bigrams(uncommon_bigrams_path)

    # Read domains and compute features
    with open(domain_csv_path, 'r', encoding='utf-8', newline='') as infile, \
         open(output_csv_path, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        # Define new fieldnames
        fieldnames = reader.fieldnames + [
            "string_entropy",
            "huffman_compression_ratio",
            "domain_length",
            "longest_dict_word_length",
            "num_substrings_in_dict",
            "vowel_consonant_binary",
            "num_uncommon_bigrams",
            "num_common_bigrams",
            "number_frequency"
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            raw_domain = row["domain"]  # Adjust if your CSV column is named differently
            domain = raw_domain.replace("-", "")

            # 1) String Entropy
            row["string_entropy"] = calculate_string_entropy(domain)

            # 2) Huffman Compression Ratio
            row["huffman_compression_ratio"] = huffman_compression_ratio(domain)

            # 3) Length of domain
            row["domain_length"] = domain_length(domain)

            # 4) Longest dictionary word
            row["longest_dict_word_length"] = longest_dictionary_word(domain, dictionary_set)

            # 5) Number of substrings in dictionary (≥3 letters)
            row["num_substrings_in_dict"] = count_dictionary_substrings(domain, dictionary_set, 3)

            # 6) Vowel/Consonant distribution (binary)
            row["vowel_consonant_binary"] = has_strict_vowel_consonant_pattern(domain)

            # 7) Number of uncommon bigrams
            row["num_uncommon_bigrams"] = count_uncommon_bigrams(domain, uncommon_bigrams_set)

            # 8) Number of common bigrams
            row["num_common_bigrams"] = count_common_bigrams(domain, common_bigrams_set)

            # 9) Frequency of numbers
            row["number_frequency"] = frequency_of_numbers(domain)

            writer.writerow(row)

    print(f"Features computed. Results saved to: {output_csv_path}")


if __name__ == "__main__":
    main()
