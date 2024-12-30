import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Load the dataset
data = pd.read_csv('/root/project-mitnick/datasets/dga_data.csv')

# 2. Drop NaN rows from the "domain" column
data = data.dropna(subset=['domain'])

# 3. Extract features (domain) and labels (isDGA)
X = data['domain']
y = data['isDGA'].map({'dga': 1, 'legit': 0})  # Map labels to binary values

# 4. Convert domains to features using CountVectorizer (e.g., n-grams)
vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 4))
X_features = vectorizer.fit_transform(X)

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_features,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 6. Initialize and train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=165, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# 7. Evaluate on the test set
y_pred = rf_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)

print(f"Test Accuracy: {test_accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 8. Confusion Matrix (numeric)
conf_mat = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", conf_mat)

# 9. Visualize Confusion Matrix
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()

model_name = "/root/project-mitnick/models/DGA-v0.1.joblib"
# 10. Save the trained model to a Joblib file
joblib.dump(rf_model, model_name)
print(f"Random Forest model saved to {model_name}.")
