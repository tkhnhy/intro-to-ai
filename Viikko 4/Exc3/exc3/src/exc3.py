from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

# MNIST download is required on the first run. Use a fixed subset for speed.
X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False, parser="liac-arff")
X = X.astype("float32") / 255.0
X_small, _, y_small, _ = train_test_split(
    X, y, train_size=10000, stratify=y, random_state=1
)
X_dev, X_test, y_dev, y_test = train_test_split(
    X_small, y_small, test_size=0.2, stratify=y_small, random_state=1
)
X_train, X_val, y_train, y_val = train_test_split(
    X_dev, y_dev, test_size=0.2, stratify=y_dev, random_state=1
)

clf = MLPClassifier(
    hidden_layer_sizes=(40,),   # one hidden layer, 40 neurons
    max_iter=50,
    solver="sgd",
    learning_rate_init=0.2,
    random_state=1,
)
clf.fit(X_train, y_train)
#print("Validation accuracy:", clf.score(X_val, y_val))
# After choosing a configuration using validation results only:
print("Final test accuracy:", clf.score(X_test, y_test))