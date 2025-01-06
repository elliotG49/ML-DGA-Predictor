import pandas as pd

input_file = '/root/project-mitnick/datasets/domains_cleaned_with_entropy.csv'
df = pd.read_csv(input_file, dtype={'entropy': 'float', 'isDGA': 'str'})
average_entropy = df.groupby('isDGA')['entropy'].mean()
print(average_entropy)
