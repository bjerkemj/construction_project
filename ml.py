import random
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Generate the data
data = []
categories = []

for i in range(5):
    data.append([random.random() for _ in range(5)])
    categories.append(random.choice(['A', 'B']))

encoded_categories = [0 if category == 'A' else 1 for category in categories]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, encoded_categories, test_size=0.2, random_state=42)

# Create a logistic regression model and fit it to the training data
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the test data
predictions = model.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")

# Test with a new example
test_example = [[random.random() for _ in range(5)]]
prediction = model.predict(test_example)
predicted_category = 'A' if prediction[0] == 0 else 'B'
print(f"Test example: {test_example}")
print(f"Predicted category: {predicted_category}")

### SVM

import random
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Generate the data
data = []
categories = []

for i in range(5):
    data.append([random.random() for _ in range(5)])
    categories.append(random.choice(['A', 'B']))

# Encode categories as 0 and 1
encoded_categories = [0 if category == 'A' else 1 for category in categories]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, encoded_categories, test_size=0.2, random_state=42)

# Create an SVM model and fit it to the training data
model = svm.SVC()
model.fit(X_train, y_train)

# Make predictions on the test data
predictions = model.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")

# Test with a new example
test_example = [[random.random() for _ in range(5)]]
prediction = model.predict(test_example)
predicted_category = 'A' if prediction[0] == 0 else 'B'
print(f"Test example: {test_example}")
print(f"Predicted category: {predicted_category}")

### Decision tree

import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Generate the data
data = []
categories = []

for i in range(5):
    data.append([random.random() for _ in range(5)])
    categories.append(random.choice(['A', 'B']))

# Encode categories as 0 and 1
encoded_categories = [0 if category == 'A' else 1 for category in categories]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, encoded_categories, test_size=0.2, random_state=42)

# Create a Decision Tree model and fit it to the training data
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Make predictions on the test data
predictions = model.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")

# Test with a new example
test_example = [[random.random() for _ in range(5)]]
prediction = model.predict(test_example)
predicted_category = 'A' if prediction[0] == 0 else 'B'
print(f"Test example: {test_example}")
print(f"Predicted category: {predicted_category}")


### Regression