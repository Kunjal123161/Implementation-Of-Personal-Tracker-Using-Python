import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the datasets
exercise_df = pd.read_csv('exercise.csv')
calories_df = pd.read_csv('calories.csv')

# Step 2: Merge the datasets on 'User_ID'
merged_df = pd.merge(exercise_df, calories_df, on='User_ID', how='inner')

# Step 3: Data Inspection
# Check the first few rows of the merged dataset
print(merged_df.head())

# Step 4: Basic Data Cleaning
# 4.1 Check for missing values
print("\nMissing values in each column:")
print(merged_df.isnull().sum())

# 4.2 Handle missing values (if any)
# For simplicity, we can drop rows with missing values
merged_df = merged_df.dropna()

# Step 5: Simple Visualizations

# 5.1 Distribution of Age (Histogram)
plt.figure(figsize=(8, 6))
sns.histplot(merged_df['Age'], kde=True)
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

# 5.2 Distribution of Calories Burned (Histogram)
plt.figure(figsize=(8, 6))
sns.histplot(merged_df['Calories'], kde=True)
plt.title('Distribution of Calories Burned')
plt.xlabel('Calories')
plt.ylabel('Frequency')
plt.show()

# 5.3 Distribution of Exercise Duration (Histogram)
plt.figure(figsize=(8, 6))
sns.histplot(merged_df['Duration'], kde=True)
plt.title('Distribution of Exercise Duration')
plt.xlabel('Exercise Duration (minutes)')
plt.ylabel('Frequency')
plt.show()

# 5.4 Distribution of Weight (Histogram)
plt.figure(figsize=(8, 6))
sns.histplot(merged_df['Weight'], kde=True)
plt.title('Distribution of Weight')
plt.xlabel('Weight (kg)')
plt.ylabel('Frequency')
plt.show()

# 5.5 Boxplot: Calories Burned by Gender
plt.figure(figsize=(8, 6))
sns.boxplot(x='Gender', y='Calories', data=merged_df)
plt.title('Calories Burned by Gender')
plt.show()

# 5.6 Boxplot: Exercise Duration by Gender
plt.figure(figsize=(8, 6))
sns.boxplot(x='Gender', y='Duration', data=merged_df)
plt.title('Exercise Duration by Gender')
plt.show()

# 5.7 Scatter Plot: Duration vs Calories Burned
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Duration', y='Calories', data=merged_df, hue='Gender')
plt.title('Exercise Duration vs Calories Burned')
plt.xlabel('Exercise Duration (minutes)')
plt.ylabel('Calories Burned')
plt.show()

# 5.8 Pairplot to see the relationships between multiple variables
plt.figure(figsize=(10, 8))
sns.pairplot(merged_df[['Age', 'Weight', 'Duration', 'Calories', 'Heart_Rate']])
plt.suptitle('Pairplot of Age, Weight, Duration, Calories, and Heart Rate', y=1.02)
plt.show()

# 5.9 Heatmap of Correlation between Numerical Variables
plt.figure(figsize=(10, 8))
correlation_matrix = merged_df[['Age', 'Weight', 'Duration', 'Calories', 'Heart_Rate']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()

# Step 6: Basic Analysis - Average Calories by Gender
print("\nAverage Calories Burned by Gender:")
print(merged_df.groupby('Gender')['Calories'].mean())

# Step 7: Average Calories Burned by Age Group (Optional)
# Creating age groups for analysis
age_bins = [0, 18, 30, 40, 50, 60, 100]
age_labels = ['<18', '18-30', '30-40', '40-50', '50-60', '60+']
merged_df['Age_Group'] = pd.cut(merged_df['Age'], bins=age_bins, labels=age_labels)

# Boxplot of Calories Burned by Age Group
plt.figure(figsize=(10, 6))
sns.boxplot(x='Age_Group', y='Calories', data=merged_df)
plt.title('Calories Burned by Age Group')
plt.show()


