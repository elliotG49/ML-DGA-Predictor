import pandas as pd

def diagnose_csv(input_file):
    df = pd.read_csv(input_file)
    
    # Check the data types
    print("Data Types:\n", df.dtypes)
    
    # Identify non-string entries in 'domain'
    non_string_domains = df[~df['domain'].apply(lambda x: isinstance(x, str))]
    print(f"\nNumber of non-string entries in 'domain': {len(non_string_domains)}")
    print(non_string_domains)

if __name__ == "__main__":
    input_file = '/root/project-mitnick/datasets/dga_data.csv'  # Replace with your actual file path
    diagnose_csv(input_file)
