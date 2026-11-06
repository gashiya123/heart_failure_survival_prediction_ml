import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv(
    "dataset/heart_failure_clinical_records_dataset.csv"
)

X = data.drop("DEATH_EVENT", axis=1)
y = data["DEATH_EVENT"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

test_samples = X_test.head(5).copy()
test_samples["DEATH_EVENT"] = y_test.loc[test_samples.index]

print(test_samples.to_string())