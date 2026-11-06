import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix

from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE


# 1. LOAD DATASET

data=pd.read_csv("dataset/heart_failure_clinical_records_dataset.csv")

X=data.drop("DEATH_EVENT",axis=1)
y=data["DEATH_EVENT"]


# 2. DATASET CLASS DISTRIBUTION

print("========================================")
print("ORIGINAL DATASET")
print("========================================")

print("Total records:",len(data))

print("\nClass distribution:")
print(y.value_counts())

print("\nClass percentage:")
print((y.value_counts(normalize=True)*100).round(2))


# 3. STRATIFIED TRAIN-TEST SPLIT

X_train,X_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("\n========================================")
print("TRAIN-TEST SPLIT")
print("========================================")

print("Training data:",X_train.shape)
print("Testing data:",X_test.shape)

print("\nTraining class distribution:")
print(y_train.value_counts())

print("\nTesting class distribution:")
print(y_test.value_counts())


# 4. SMOTE + RANDOM FOREST

random_forest_pipeline=Pipeline([
    ("smote",SMOTE(random_state=42)),
    ("model",RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ))
])


# 5. CHECK TRAINING DATA AFTER SMOTE

smote=SMOTE(random_state=42)

X_train_smote,y_train_smote=smote.fit_resample(
    X_train,
    y_train
)

print("\n========================================")
print("TRAINING DATA AFTER SMOTE")
print("========================================")

print("Training data before SMOTE:",X_train.shape)
print("Training data after SMOTE:",X_train_smote.shape)

print("\nClass distribution after SMOTE:")
print(y_train_smote.value_counts())


# 6. TRAIN RANDOM FOREST

print("\n========================================")
print("MODEL TRAINING")
print("========================================")

random_forest_pipeline.fit(X_train,y_train)

print("Random Forest training completed.")


# 7. TRAINING PREDICTION

train_probability=random_forest_pipeline.predict_proba(X_train)[:,1]

threshold=0.40

y_train_pred=(train_probability>=threshold).astype(int)


# 8. TRAINING METRICS

train_accuracy=accuracy_score(y_train,y_train_pred)

train_precision=precision_score(
    y_train,
    y_train_pred,
    zero_division=0
)

train_recall=recall_score(
    y_train,
    y_train_pred,
    zero_division=0
)

train_f1=f1_score(
    y_train,
    y_train_pred,
    zero_division=0
)


print("\n========================================")
print("TRAINING RESULTS")
print("========================================")

print("Threshold:",threshold)
print("Accuracy:",round(train_accuracy,4))
print("Precision:",round(train_precision,4))
print("Recall:",round(train_recall,4))
print("F1 Score:",round(train_f1,4))


# 9. TEST PREDICTION

test_probability=random_forest_pipeline.predict_proba(X_test)[:,1]

y_test_pred=(test_probability>=threshold).astype(int)


# 10. TEST METRICS

test_accuracy=accuracy_score(y_test,y_test_pred)

test_precision=precision_score(
    y_test,
    y_test_pred,
    zero_division=0
)

test_recall=recall_score(
    y_test,
    y_test_pred,
    zero_division=0
)

test_f1=f1_score(
    y_test,
    y_test_pred,
    zero_division=0
)

test_cm=confusion_matrix(y_test,y_test_pred)


print("\n========================================")
print("TESTING RESULTS")
print("========================================")

print("Threshold:",threshold)
print("Accuracy:",round(test_accuracy,4))
print("Precision:",round(test_precision,4))
print("Recall:",round(test_recall,4))
print("F1 Score:",round(test_f1,4))

print("\nConfusion Matrix:")
print(test_cm)


# 11. SAVE MODEL

joblib.dump(
    random_forest_pipeline,
    "random_forest_model.pkl"
)

joblib.dump(
    threshold,
    "random_forest_threshold.pkl"
)


print("\n========================================")
print("MODEL SAVED")
print("========================================")

print("Model saved as: random_forest_model.pkl")
print("Threshold saved as: random_forest_threshold.pkl")