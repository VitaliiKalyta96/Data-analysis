import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("ab_test_data.csv")
print(df)

print(df['test_group'].value_counts())
print("Кількість користувачів групи 'a':", (df['test_group'] == 'a').sum())
print("Кількість користувачів групи 'b':", (df['test_group'] == 'b').sum())
print(df['conversion'].value_counts())
print("Конверсія в групі A:", round(df[df['test_group'] == 'a']['conversion'].mean() * 100, 2), "%")
print("Конверсія в групі B:", round(df[df['test_group'] == 'b']['conversion'].mean() * 100, 2), "%")

df['timestamp'] = pd.to_datetime(df['timestamp'])
start_date = df['timestamp'].min()
end_date = df['timestamp'].max()
diff_date = (end_date - start_date).days

print("Дата початку тесту:", start_date.date())
print("Дата кінця тесту:", end_date.date())
print("Тривалість тесту (в днях):", diff_date)

"""Тестування гіпотез за допомогою SciPy. Критерій Стʼюдента"""

alpha = 0.05
statistic, pvalue = stats.ttest_ind(df[df['test_group'] == 'a']['conversion'],
                                    df[df['test_group'] == 'b']['conversion'],
                                    alternative='less')

print(f't-statistic: {round(statistic, 2)}, p-value: {round(pvalue, 2)}')

if pvalue < alpha:
    print('The difference is statistically significant, Null Hypothesis is rejected.')
else:
    print('The difference is insignificant, Null Hypothesis cannot rejected.')


"""Візуалізація для порівняння середніх значень у групах з 95% довірчими інтервалами"""

plt.figure(figsize=(8, 6))
sns.barplot(x=df['test_group'],
            y=df['conversion'],
            errorbar=('ci', 95),
            hue=df['test_group'],
            palette=['blue', 'orange'])

plt.title('A/B Test Results')
plt.xlabel('Group')
plt.ylabel('Mean Conversion Rate')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()