import os
import matplotlib.pyplot as plt
import seaborn as sns


os.makedirs("model_results",exist_ok=True)


# ========================================
# LOGISTIC REGRESSION TEST RESULTS
# ========================================

logistic_accuracy=0.80
logistic_precision=0.6842
logistic_recall=0.6842
logistic_f1=0.6842

logistic_cm=[
    [35,6],
    [6,13]
]


# ========================================
# RANDOM FOREST TEST RESULTS
# ========================================

random_forest_accuracy=0.8333
random_forest_precision=0.7368
random_forest_recall=0.7368
random_forest_f1=0.7368

random_forest_cm=[
    [36,5],
    [5,14]
]


# ========================================
# RANDOM FOREST CROSS-VALIDATION RESULTS
# ========================================

cv_accuracy=0.836
cv_precision=0.7374
cv_recall=0.76
cv_f1=0.7475


# ========================================
# METRIC VALUES
# ========================================

metrics=[
    "Accuracy",
    "Precision",
    "Recall",
    "F1 Score"
]

logistic_values=[
    logistic_accuracy,
    logistic_precision,
    logistic_recall,
    logistic_f1
]

random_forest_values=[
    random_forest_accuracy,
    random_forest_precision,
    random_forest_recall,
    random_forest_f1
]


# ========================================
# 1. ACCURACY COMPARISON
# ========================================

plt.figure(figsize=(7,5))

plt.bar(
    ["Logistic Regression","Random Forest"],
    [logistic_accuracy*100,random_forest_accuracy*100]
)

plt.ylabel("Accuracy (%)")
plt.title("Accuracy Comparison")
plt.ylim(0,100)
plt.tight_layout()

plt.savefig("model_results/accuracy_comparison.png")
plt.close()


# ========================================
# 2. PRECISION COMPARISON
# ========================================

plt.figure(figsize=(7,5))

plt.bar(
    ["Logistic Regression","Random Forest"],
    [logistic_precision*100,random_forest_precision*100]
)

plt.ylabel("Precision (%)")
plt.title("Precision Comparison")
plt.ylim(0,100)
plt.tight_layout()

plt.savefig("model_results/precision_comparison.png")
plt.close()


# ========================================
# 3. RECALL COMPARISON
# ========================================

plt.figure(figsize=(7,5))

plt.bar(
    ["Logistic Regression","Random Forest"],
    [logistic_recall*100,random_forest_recall*100]
)

plt.ylabel("Recall (%)")
plt.title("Recall Comparison")
plt.ylim(0,100)
plt.tight_layout()

plt.savefig("model_results/recall_comparison.png")
plt.close()


# ========================================
# 4. F1 SCORE COMPARISON
# ========================================

plt.figure(figsize=(7,5))

plt.bar(
    ["Logistic Regression","Random Forest"],
    [logistic_f1*100,random_forest_f1*100]
)

plt.ylabel("F1 Score (%)")
plt.title("F1 Score Comparison")
plt.ylim(0,100)
plt.tight_layout()

plt.savefig("model_results/f1_comparison.png")
plt.close()


# ========================================
# 5. OVERALL MODEL PERFORMANCE
# ========================================

x=range(len(metrics))

plt.figure(figsize=(10,6))

plt.bar(
    [i-0.2 for i in x],
    [value*100 for value in logistic_values],
    width=0.4,
    label="Logistic Regression"
)

plt.bar(
    [i+0.2 for i in x],
    [value*100 for value in random_forest_values],
    width=0.4,
    label="Random Forest"
)

plt.xticks(list(x),metrics)
plt.ylabel("Percentage")
plt.title("Overall Model Performance")
plt.ylim(0,100)
plt.legend()
plt.tight_layout()

plt.savefig("model_results/overall_model_performance.png")
plt.close()


# ========================================
# 6. RANDOM FOREST
# CROSS-VALIDATION VS TEST
# ========================================

cv_values=[
    cv_accuracy,
    cv_precision,
    cv_recall,
    cv_f1
]

test_values=[
    random_forest_accuracy,
    random_forest_precision,
    random_forest_recall,
    random_forest_f1
]

x=range(len(metrics))

plt.figure(figsize=(10,6))

plt.bar(
    [i-0.2 for i in x],
    [value*100 for value in cv_values],
    width=0.4,
    label="5-Fold Cross-Validation"
)

plt.bar(
    [i+0.2 for i in x],
    [value*100 for value in test_values],
    width=0.4,
    label="Test Set"
)

plt.xticks(list(x),metrics)
plt.ylabel("Percentage")
plt.title("Random Forest: Cross-Validation vs Test Performance")
plt.ylim(0,100)
plt.legend()
plt.tight_layout()

plt.savefig("model_results/random_forest_cv_vs_test.png")
plt.close()


# ========================================
# 7. LOGISTIC REGRESSION CONFUSION MATRIX
# ========================================

plt.figure(figsize=(6,5))

sns.heatmap(
    logistic_cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Predicted Survived","Predicted Death"],
    yticklabels=["Actual Survived","Actual Death"]
)

plt.title("Confusion Matrix - Logistic Regression")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()

plt.savefig("model_results/logistic_regression_confusion_matrix.png")
plt.close()


# ========================================
# 8. RANDOM FOREST CONFUSION MATRIX
# ========================================

plt.figure(figsize=(6,5))

sns.heatmap(
    random_forest_cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Predicted Survived","Predicted Death"],
    yticklabels=["Actual Survived","Actual Death"]
)

plt.title("Confusion Matrix - Random Forest")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()

plt.savefig("model_results/random_forest_confusion_matrix.png")
plt.close()


print("========================================")
print("MODEL RESULT GRAPHS")
print("========================================")
print("All model result graphs generated successfully.")
print("Graphs saved in the 'model_results' folder.")