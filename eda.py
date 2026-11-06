import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data=pd.read_csv("dataset/heart_failure_clinical_records_dataset.csv")

# Basic information
print("Dataset shape:",data.shape)
print("\nDataset information:")
print(data.info())

# Display first ten records
print("\nFirst ten records of the dataset:")
print(data.head(10).to_string(index=False))

# Summary statistics
print("\nSummary statistics of the dataset:")
print(data.describe().to_string())

print("\nMissing values:")
print(data.isnull().sum())

print("\nDuplicate rows:",data.duplicated().sum())

print("\nClass distribution:")
print(data["DEATH_EVENT"].value_counts())

# Create EDA plots folder
import os
os.makedirs("eda_plots",exist_ok=True)

# 1. Death event distribution
plt.figure(figsize=(6,4))
sns.countplot(x="DEATH_EVENT",data=data)
plt.title("Death Event Distribution")
plt.xlabel("Death Event")
plt.ylabel("Number of Patients")
plt.tight_layout()
plt.savefig("eda_plots/death_event_distribution.png")
plt.close()

# 2. Age distribution
plt.figure(figsize=(7,4))
sns.histplot(data["age"],kde=True)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Patients")
plt.tight_layout()
plt.savefig("eda_plots/age_distribution.png")
plt.close()

# 3. Ejection fraction distribution
plt.figure(figsize=(7,4))
sns.histplot(data["ejection_fraction"],kde=True)
plt.title("Ejection Fraction Distribution")
plt.xlabel("Ejection Fraction")
plt.ylabel("Number of Patients")
plt.tight_layout()
plt.savefig("eda_plots/ejection_fraction_distribution.png")
plt.close()

# 4. Serum creatinine distribution
plt.figure(figsize=(7,4))
sns.histplot(data["serum_creatinine"],kde=True)
plt.title("Serum Creatinine Distribution")
plt.xlabel("Serum Creatinine")
plt.ylabel("Number of Patients")
plt.tight_layout()
plt.savefig("eda_plots/serum_creatinine_distribution.png")
plt.close()

# 5. Age vs Death Event
plt.figure(figsize=(7,4))
sns.boxplot(x="DEATH_EVENT",y="age",data=data)
plt.title("Age vs Death Event")
plt.xlabel("Death Event")
plt.ylabel("Age")
plt.tight_layout()
plt.savefig("eda_plots/age_vs_death_event.png")
plt.close()

# 6. Ejection Fraction vs Death Event
plt.figure(figsize=(7,4))
sns.boxplot(x="DEATH_EVENT",y="ejection_fraction",data=data)
plt.title("Ejection Fraction vs Death Event")
plt.xlabel("Death Event")
plt.ylabel("Ejection Fraction")
plt.tight_layout()
plt.savefig("eda_plots/ejection_fraction_vs_death_event.png")
plt.close()

# 7. Serum Creatinine vs Death Event
plt.figure(figsize=(7,4))
sns.boxplot(x="DEATH_EVENT",y="serum_creatinine",data=data)
plt.title("Serum Creatinine vs Death Event")
plt.xlabel("Death Event")
plt.ylabel("Serum Creatinine")
plt.tight_layout()
plt.savefig("eda_plots/serum_creatinine_vs_death_event.png")
plt.close()

# 8. Binary clinical variables distribution
binary_columns=["anaemia","diabetes","high_blood_pressure","sex","smoking"]

binary_data=data[binary_columns].sum()

plt.figure(figsize=(8,5))
binary_data.plot(kind="bar")
plt.title("Distribution of Binary Clinical Variables")
plt.xlabel("Clinical Variable")
plt.ylabel("Number of Patients with Value 1")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("eda_plots/binary_clinical_variables.png")
plt.close()

# 9. Correlation heatmap
plt.figure(figsize=(12,9))
correlation=data.corr()
sns.heatmap(correlation,annot=True,fmt=".2f",cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("eda_plots/correlation_heatmap.png")
plt.close()

print("\nEDA completed successfully.")
print("Plots saved in the 'eda_plots' folder.")