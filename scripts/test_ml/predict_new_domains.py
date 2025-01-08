import joblib
import pandas as pd
import sys

sys.path.append("/root/project-mitnick/scripts/features")
# Import your feature functions
from scripts.features.string_entropy import calculate_string_entropy
from scripts.features.huffman_compression_ratio import huffman_compression_ratio
from scripts.features.domain_length import domain_length
from scripts.features.longest_dict_word import longest_dictionary_word
from scripts.features.dict_substring_count import count_dictionary_substrings
from scripts.features.consecutive_vc_distribution import has_strict_vowel_consonant_pattern
from scripts.features.uncommon_bigrams_count import count_uncommon_bigrams
from scripts.features.common_bigrams_count import count_common_bigrams
from scripts.features.number_frequency import frequency_of_numbers

def load_dictionary(dictionary_csv_path: str) -> set:
    """Load dictionary words into a set (same as before)."""
    dictionary_set = set()
    with open(dictionary_csv_path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word:
                dictionary_set.add(word.lower())
    return dictionary_set

def load_bigrams(bigrams_csv_path: str) -> set:
    """Load bigrams into a set (same as before)."""
    bigrams_set = set()
    with open(bigrams_csv_path, 'r', encoding='utf-8') as f:
        for line in f:
            bigram = line.strip()
            if bigram:
                bigrams_set.add(bigram.lower())
    return bigrams_set

def compute_features_for_domain(
    domain: str, 
    dictionary_set: set,
    common_bigrams_set: set,
    uncommon_bigrams_set: set
) -> dict:
    """
    Compute the nine features for a single domain.
    Return a dictionary where keys are feature names and values are the computed feature.
    """
    # Preprocess domain (e.g., remove hyphens if you decided to do that)
    # domain = domain.replace("-", "")

    features = {}
    features["string_entropy"] = calculate_string_entropy(domain)
    features["huffman_compression_ratio"] = huffman_compression_ratio(domain)
    features["domain_length"] = domain_length(domain)
    features["longest_dict_word_length"] = longest_dictionary_word(domain, dictionary_set)
    features["num_substrings_in_dict"] = count_dictionary_substrings(domain, dictionary_set, 3)
    features["vowel_consonant_binary"] = has_strict_vowel_consonant_pattern(domain)
    features["num_uncommon_bigrams"] = count_uncommon_bigrams(domain, uncommon_bigrams_set)
    features["num_common_bigrams"] = count_common_bigrams(domain, common_bigrams_set)
    features["number_frequency"] = frequency_of_numbers(domain)
    return features

def main():
    # 1. Paths to your pre-trained model, scaler, dictionary, and bigrams
    model_path = "/root/project-mitnick/models/DGA-feature-based-v0.1.joblib"
    scaler_path = "/root/project-mitnick/models/DGA-feature-based-scaler-v0.1.joblib"
    dictionary_csv_path = "/root/project-mitnick/dictionaries/english_wordlist.csv"
    common_bigrams_path = "/root/project-mitnick/dictionaries/common_bigrams.csv"
    uncommon_bigrams_path = "/root/project-mitnick/dictionaries/uncommon_bigrams.csv"

    # 2. Load the trained model and scaler
    rf_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    # 3. Load dictionary sets (if required by your features)
    dictionary_set = load_dictionary(dictionary_csv_path)
    common_bigrams_set = load_bigrams(common_bigrams_path)
    uncommon_bigrams_set = load_bigrams(uncommon_bigrams_path)

    # 4. Read the text file containing new domains (one per line)
    test_domains_file = "/root/project-mitnick/datasets/new-dga-domains.txt"
    with open(test_domains_file, "r", encoding="utf-8") as f:
        new_domains = [line.strip() for line in f if line.strip()]

    # 5. Compute features for each domain
    feature_rows = []
    for domain in new_domains:
        feats = compute_features_for_domain(
            domain,
            dictionary_set,
            common_bigrams_set,
            uncommon_bigrams_set
        )
        feature_rows.append(feats)

    # Convert to a DataFrame
    df_features = pd.DataFrame(feature_rows)

    # 6. Scale the features using the same scaler
    #    Make sure the columns match the exact order your model expects
    feature_order = [
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
    X = df_features[feature_order].values
    X_scaled = scaler.transform(X)

    # 7. Get predictions from the model
    #    rf_model predicts 1 for 'dga' and 0 for 'legit' (assuming your training mapped that way)
    predictions = rf_model.predict(X_scaled)

    # 8. Interpret predictions and display results
    #    Example: map 1 -> 'dga' and 0 -> 'legit'
    label_map = {1: "dga", 0: "legit"}
    results = []
    for domain, pred in zip(new_domains, predictions):
        result_label = label_map[pred]
        results.append((domain, result_label))

    # 9. Print or save the results
    print("\nClassification Results for New Domains:")
    for domain, label in results:
        print(f"{domain} -> {label}")

    # (Optional) Save results to a CSV
    # df_results = pd.DataFrame(results, columns=["domain", "prediction"])
    # df_results.to_csv("/root/project-mitnick/datasets/test_domains_predictions.csv", index=False)

if __name__ == "__main__":
    main()
