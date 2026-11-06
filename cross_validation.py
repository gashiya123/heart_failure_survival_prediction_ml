import pandas as pd

from sklearn.model_selection import StratifiedKFold,cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import make_scorer,accuracy_score,precision_score,recall_score,f1_score
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE


# 1. LOAD DATASET

data=pd.read_csv("dataset/heart_failure_clinical_records_dataset.csv")

X=data.drop("DEATH_EVENT",axis=1)
y=data["DEATH_EVENT"]


# 2. RANDOM FOREST PIPELINE

random_forest_pipeline=Pipeline([
    ("smote",SMOTE(random_state=42)),
    ("model",RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ))
])


# 3. 5-FOLD STRATIFIED CROSS-VALIDATION

cv=StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# 4. METRICS

scoring={
    "accuracy":make_scorer(accuracy_score),
    "precision":make_scorer(precision_score,zero_division=0),
    "recall":make_scorer(recall_score,zero_division=0),
    "f1":make_scorer(f1_score,zero_division=0)
}


# 5. CROSS-VALIDATION

results=cross_validate(
    random_forest_pipeline,
    X,
    y,
    cv=cv,
    scoring=scoring
)


# 6. DISPLAY RESULTS

print("========================================")
print("5-FOLD CROSS-VALIDATION RESULTS")
print("========================================")

print("\nAccuracy for each fold:")
print(results["test_accuracy"])

print("\nPrecision for each fold:")
print(results["test_precision"])

print("\nRecall for each fold:")
print(results["test_recall"])

print("\nF1 Score for each fold:")
print(results["test_f1"])


# 7. AVERAGE RESULTS

accuracy_mean=results["test_accuracy"].mean()
precision_mean=results["test_precision"].mean()
recall_mean=results["test_recall"].mean()
f1_mean=results["test_f1"].mean()


print("\n========================================")
print("AVERAGE CROSS-VALIDATION RESULTS")
print("========================================")

print("Accuracy:",round(accuracy_mean,4))
print("Precision:",round(precision_mean,4))
print("Recall:",round(recall_mean,4))
print("F1 Score:",round(f1_mean,4))


# 8. STANDARD DEVIATION

print("\n========================================")
print("STANDARD DEVIATION")
print("========================================")

print("Accuracy:",round(results["test_accuracy"].std(),4))
print("Precision:",round(results["test_precision"].std(),4))
print("Recall:",round(results["test_recall"].std(),4))
print("F1 Score:",round(results["test_f1"].std(),4))