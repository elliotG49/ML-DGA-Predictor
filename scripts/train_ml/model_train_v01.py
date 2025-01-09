import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Load the dataset with your computed numeric features
data_path = "/root/project-mitnick/datasets/cleaned_featured/domains_with_features_v01.csv"
data = pd.read_csv(data_path)

# Drop rows with NaNs if necessary
data.dropna(subset=["domain"], inplace=True)

# 2. Define your label (binary) from the 'isDGA' column
#    Map 'dga' -> 1, 'legit' -> 0
y = data["isDGA"].map({"dga": 1, "legit": 0})

# 3. Select your numeric feature columns
feature_columns = [
    "string_entropy",
    "huffman_compression_ratio",
    "domain_length",
    "longest_dict_word_length",
    "num_substrings_in_dict",
    "num_uncommon_bigrams",
    "num_common_bigrams",
]
X = data[feature_columns].values

# 4. Set up Stratified K-Fold
n_splits = 10
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# Lists to store per-fold metrics
fold_accuracies = []
fold_confusion_matrices = []
fold_class_reports = []

fold_index = 1

# 5. Perform cross-validation
for train_index, test_index in skf.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    # Scale (normalize) features using MinMaxScaler
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize and train the Random Forest model
    rf_model = RandomForestClassifier(n_estimators=165, random_state=42, n_jobs=-1)
    rf_model.fit(X_train_scaled, y_train)

    # Predict on this fold's test set
    y_pred = rf_model.predict(X_test_scaled)

    # Evaluate metrics
    accuracy = accuracy_score(y_test, y_pred)
    conf_mat = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, output_dict=True)

    fold_accuracies.append(accuracy)
    fold_confusion_matrices.append(conf_mat)
    fold_class_reports.append(class_report)

    print(f"--- Fold {fold_index} ---")
    print(f"Accuracy: {accuracy:.4f}")
    print("Confusion Matrix:")
    print(conf_mat)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("-----------------------------------\n")
    fold_index += 1

# 6. Aggregate results across folds
mean_accuracy = np.mean(fold_accuracies)
print(f"Mean Accuracy across {n_splits} folds: {mean_accuracy:.4f}")

# Compute average confusion matrix (assuming binary classification 2x2)
avg_conf_mat = sum(fold_confusion_matrices) / n_splits

# 7. Visualize the averaged confusion matrix
plt.figure(figsize=(6,4))
sns.heatmap(avg_conf_mat, annot=True, fmt=".2f", cmap="Blues")
plt.title(f"Average Confusion Matrix (n_splits={n_splits})")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()

# 8. (Optional) Retrain a final model on the entire dataset
final_scaler = MinMaxScaler()
X_scaled = final_scaler.fit_transform(X)
final_model = RandomForestClassifier(n_estimators=165, random_state=42, n_jobs=-1)
final_model.fit(X_scaled, y)

# 9. Save the final model & scaler as Joblib files
model_path = "/root/project-mitnick/models/DGA-feature-based-v0.1.joblib"
scaler_path = "/root/project-mitnick/models/DGA-feature-based-scaler-v0.1.joblib"
joblib.dump(final_model, model_path)
joblib.dump(final_scaler, scaler_path)

print(f"Final Random Forest model saved to {model_path}")
print(f"Final scaler saved to {scaler_path}")

# 10. Show Feature Importances (after final training)
importances = final_model.feature_importances_

# Create a DataFrame with feature names and their importances
importance_df = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': importances
})

# Sort by importance (descending)
importance_df.sort_values('Importance', ascending=False, inplace=True)

print("\n--- Feature Importances (Final Model) ---")
print(importance_df)

# Optional: Visualize feature importances as a bar chart
plt.figure(figsize=(8, 5))
sns.barplot(data=importance_df, x='Importance', y='Feature', palette='viridis')
plt.title("Random Forest Feature Importances")
plt.tight_layout()
plt.show()
