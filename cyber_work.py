# -*- coding: utf-8 -*-
"""CYBER_WORK.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15mB_ON9nrd5_awXlrnfeQxXfgOeSSK63
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
from google.colab import drive
# %matplotlib inline

from google.colab import drive
drive.mount('/content/drive')

import glob
all_dfs=[pd.read_csv(one)
        for one in glob.glob('/content/drive/MyDrive/MINI/TCP_IP-DDoS-TCP*.pcap.csv')
        ]
all_sr=[pd.read_csv(one) for one in glob.glob('/content/drive/MyDrive/CSV/*.csv')]
#Adding column for identificatino of attacks
for f in all_dfs:
  f['Attack']=1
for df in all_sr:
  f['Attack']=0

dfs= all_sr.append(all_dfs)
df=pd.concat(all_dfs)

from imblearn.over_sampling import SMOTE
X = df.drop(columns=['Attack'])
y = df['Attack']
# Split data into train and test sets
# Apply SMOTE to balance the dataset
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Convert the resampled data back to DataFrame
resampled_df = pd.DataFrame(X_resampled, columns=X.columns)
resampled_df['Attack'] = y_resampled

# Save the resampled dataset to a new CSV file
resampled_df.to_csv("balanced_IDS.csv", index=False)

df=pd.read_csv("balanced_IDS.csv")

X = df.drop(columns=['Attack'])
y = df['Attack']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



"""# Scaling"""

from sklearn.linear_model import LinearRegression
lg=LinearRegression()
lg.fit(X_train,y_train)



"""# Model evaluation"""

y_pred = lg.predict(X_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Assuming y_test and y_pred are your true labels and predicted labels, respectively
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)  # Root Mean Squared Error
r2 = r2_score(y_test, y_pred)  # R-squared
print("Key Metrics of Linear Regression")
print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("R-squared (R2):", r2)

np.random.seed(0)
y_test = 10 * np.random.rand(100)
y_pred = y_test + np.random.normal(0, 1, 100)  # Adding some noise for prediction

# Define bin edges for 5 bins
bin_edges = np.linspace(np.min(y_test), np.max(y_test), 6)  # 5 bins = 6 edges

# Bin the test and predicted values
y_binned = np.digitize(y_test, bin_edges) - 1
pred_binned = np.digitize(y_pred, bin_edges) - 1

# Compute the confusion matrix
conf_matrix = confusion_matrix(y_binned, pred_binned)

# Display the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=bin_edges, yticklabels=bin_edges)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix for Binned Linear Regression')
plt.show()

X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Initialize and train a Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

y_pred_proba = rf_classifier.predict_proba(X_test)
y_pred=rf_classifier.predict(X_test)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Calculate precision
precision = precision_score(y_test, y_pred)

# Calculate recall
recall = recall_score(y_test, y_pred)

# Calculate F1-score
f1 = f1_score(y_test, y_pred)
print("Key Metrics of Random Forest")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

accuracy

precision

from sklearn.metrics import confusion_matrix

# Assuming y_test contains the true class labels and y_pred contains the predicted class labels
conf_matrix = confusion_matrix(y_test, y_pred)

print("Confusion Matrix for Random Forest:")
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='g')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

from sklearn.naive_bayes import GaussianNB



nb_classifier = GaussianNB()
nb_classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = nb_classifier.predict(X_test)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Assuming y_test contains the true class labels and y_pred contains the predicted class labels
# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Calculate precision
precision = precision_score(y_test, y_pred)

# Calculate recall
recall = recall_score(y_test, y_pred)

# Calculate F1-score
f1 = f1_score(y_test, y_pred)
print("Key Metrics of GaussianNB")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

precision

accuracy

from sklearn.metrics import confusion_matrix

# Create the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

print("Confusion Matrix for GaussianNB:")
# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='g')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

from sklearn.ensemble import AdaBoostClassifier

# Initialize the AdaBoost classifier with a decision tree as the base estimator
adaboost_classifier = AdaBoostClassifier(n_estimators=50, random_state=42)

# Train the AdaBoost classifier using the training data
adaboost_classifier.fit(X_train, y_train)

# Make predictions on the new data
y_pred = adaboost_classifier.predict(X_test)

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score

# Make predictions on the testing data
y_pred = adaboost_classifier.predict(X_test)

# Calculate precision
precision = precision_score(y_test, y_pred)

# Calculate recall
recall = recall_score(y_test, y_pred)

# Calculate F1-score
f1 = f1_score(y_test, y_pred)
print("Key Metrics of Adaboost")
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

from sklearn.metrics import confusion_matrix

# Calculate the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

print("Confusion Matrix for Adaboost:")
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='g')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

