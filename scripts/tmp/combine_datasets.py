import pandas as pd

# ----------------------------------------------------------------------
# 1. Read your CSV file
# ----------------------------------------------------------------------
df = pd.read_csv("/root/project-mitnick/datasets/raw/dga_domains_full.csv")  
# The columns are: [isDGA, subset, host]

# ----------------------------------------------------------------------
# 2. Create a 'domain' column by splitting at the first '.'
# ----------------------------------------------------------------------
def get_domain_before_first_dot(full_str):
    if '.' in full_str:
        return full_str.split('.', 1)[0]  # split only on the first dot
    else:
        return full_str  # if no dot found, keep the entire string

df["domain"] = df["host"].apply(get_domain_before_first_dot)

# ----------------------------------------------------------------------
# 3. Rename 'subset' -> 'subclass' (optional, depending on your needs)
# ----------------------------------------------------------------------
df.rename(columns={"subset": "subclass"}, inplace=True)

# ----------------------------------------------------------------------
# 4. Reorder columns to: [isDGA, domain, host, subclass]
# ----------------------------------------------------------------------
df = df[["isDGA", "domain", "host", "subclass"]]

# ----------------------------------------------------------------------
# 5. Save the updated CSV
# ----------------------------------------------------------------------
output_path = "/root/project-mitnick/datasets/raw/dga_data_corrected.csv"
df.to_csv(output_path, index=False)

print(f"Corrected dataset saved to: {output_path}")
