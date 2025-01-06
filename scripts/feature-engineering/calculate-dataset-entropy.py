import pandas as pd
import math
from collections import Counter
import logging
import sys

# Configure logging
logging.basicConfig(
    filename='/root/project-mitnick/logs/clean_entropy_calculation.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def compute_entropy(s):
    """
    Compute the Shannon entropy of a string.

    Parameters:
        s (str): The input string.

    Returns:
        float: The entropy value.
    """
    if not isinstance(s, str):
        if pd.isna(s):
            # This case should not occur if NaNs are already removed
            return 0.0
        else:
            s = str(s)  # Convert non-string to string if possible

    if not s:
        return 0.0

    counts = Counter(s)
    total = len(s)
    entropy = -sum((count / total) * math.log2(count / total) for count in counts.values())
    return entropy

def main():
    # File paths
    input_file = '/root/project-mitnick/datasets/dga_data.csv'  # Replace with your actual input file path
    output_file = '/root/project-mitnick/datasets/dga_data.csv'  # Desired output file path

    try:
        # Read the CSV file, ensuring 'domain' is treated as string
        df = pd.read_csv(input_file, dtype={'domain': 'str'})
        logging.info(f"Successfully read the input file: {input_file}")
    except FileNotFoundError:
        logging.error(f"The file {input_file} was not found.")
        print(f"Error: The file {input_file} was not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        logging.error("The input file is empty.")
        print("Error: The input file is empty.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading the file: {e}")
        print(f"An unexpected error occurred while reading the file: {e}")
        sys.exit(1)

    # Display initial dataset size
    initial_count = len(df)
    logging.info(f"Initial number of entries: {initial_count}")
    print(f"Initial number of entries: {initial_count}")

    # Remove rows where 'domain' is NaN
    df_cleaned = df.dropna(subset=['domain'])
    cleaned_count = len(df_cleaned)
    removed_count = initial_count - cleaned_count
    logging.info(f"Removed {removed_count} entries with missing 'domain' values.")
    print(f"Removed {removed_count} entries with missing 'domain' values.")

    # Optionally, reset the index
    df_cleaned.reset_index(drop=True, inplace=True)

    # Compute entropy for each domain
    df_cleaned['entropy'] = df_cleaned['domain'].apply(compute_entropy)
    logging.info("Computed entropy for all cleaned domains.")

    # Optional: Round entropy to 4 decimal places for readability
    df_cleaned['entropy'] = df_cleaned['entropy'].round(4)

    # Log entropy statistics
    entropy_stats = df_cleaned['entropy'].describe()
    logging.info(f"Entropy statistics:\n{entropy_stats}")
    print("\nEntropy statistics:")
    print(entropy_stats)

    try:
        # Save the cleaned DataFrame with entropy to a new CSV file
        df_cleaned.to_csv(output_file, index=False)
        logging.info(f"Cleaned data with entropy saved to {output_file}")
        print(f"\nCleaned data with entropy saved to {output_file}")
    except Exception as e:
        logging.error(f"An error occurred while writing to the file: {e}")
        print(f"An error occurred while writing to the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
