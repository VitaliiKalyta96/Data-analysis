import pandas as pd


survey_file = "survey_results_public.csv"
schema_file = "survey_results_schema.csv"
data_df = pd.read_csv(survey_file)
schema_df = pd.read_csv(schema_file)

"""Скільки респондентів пройшли опитування?"""
print("Кількість респондентів пройшли опитування:", data_df.shape[0])


"""Скільки респондентів відповіли на всі запитання?"""
# Отримуємо список питань із колонки "qname"
question_columns = set(schema_df["qname"].dropna())

# Перетинаємо зі стовпцями таблиці опитування (залишаємо тільки ті, що є у питанні)
valid_columns = list(question_columns.intersection(data_df.columns))

# Фільтруємо таблицю лише за цими стовпцями
filtered_data = data_df[valid_columns]

# Рахуємо кількість респондентів, які відповіли на всі ці питання
full_responses = filtered_data.dropna().shape[0]
print("Кількість респондентів, які відповіли на всі запитання:", full_responses)


"""Які значення мір центральної тенденції для досвіду (WorkExp) респондентів?"""
# Переконаємось, що WorkExp є числовим типом
data_df['WorkExp'] = pd.to_numeric(data_df['WorkExp'], errors='coerce')

# Обчислюємо міри центральної тенденції
mean_value = round(data_df['WorkExp'].mean(), 2) # Середнє значення
median_value = data_df['WorkExp'].median()  # Медіана
mode_value = data_df['WorkExp'].mode()   # Мода (може бути кілька значень)

print(f"Середнє значення (Mean): {mean_value}")
print(f"Медіана (Median): {median_value}")
print(f"Мода (Mode): {mode_value.tolist()}")


"""Скільки респондентів працює віддалено?"""
# Фільтруємо респондентів, які працюють віддалено (зі значенням "Remote")
remote_workers_ = data_df[data_df['RemoteWork'].notna()]
remote_workers = data_df[data_df['RemoteWork'] == 'Remote']

# Кількість респондентів, які працюють віддалено
remote_count = remote_workers.shape[0]
print(f"Кількість респондентів, які працюють віддалено: {remote_count}")


"""Який відсоток респондентів програмує на Python?"""
# # Перевіримо як називається стовпець з мовами
# print(list(data_df.columns))

# Стовпець з мовами називається 'LanguageHaveWorkedWith'
# Перевіряємо, чи містить кожен рядок 'Python'
python_users = data_df['LanguageHaveWorkedWith'].dropna().str.contains('Python', na=False)

# Обчислюємо відсоток
percentage_python = round((python_users.sum() / len(data_df)) * 100, 2)
print(f"Відсоток респондентів, які програмують на Python: {percentage_python}%")


"""Скільки респондентів навчалося програмувати за допомогою онлайн курсів?"""
data_df['learned_with_online_courses'] = data_df.LearnCode.str.contains('online courses', case=False, na=False)
online_count = data_df.learned_with_online_courses.sum()
print("Кількість респондентів навчалося програмувати за допомогою онлайн курсів -", online_count)


"""Серед респондентів що програмують на Python в групуванні по країнам, яка середня та медіанна сума компенсації (ConvertedCompYearly) в кожній країні?"""
# Фільтруємо респондентів, які вказали, що програмують на Python
python_devs = data_df[data_df['LanguageHaveWorkedWith'].notna() & data_df['LanguageHaveWorkedWith'].str.contains('Python', na=False)]

# Групуємо за країнами та обчислюємо середнє та медіану зарплати
compensation_stats = python_devs.groupby('Country')['ConvertedCompYearly'].agg(['mean', 'median']).round(1)

# # Встановлюємо максимальну кількість рядків для виведення
# pd.set_option('display.max_rows', None)  # Показуємо всі рядки

# Виводимо результат
print(compensation_stats)


"""Які рівні освіти мають 5 респондентів з найбільшою компенсацією?"""
level_educ = data_df[['ResponseId', 'EdLevel', 'ConvertedCompYearly']].sort_values(by='ConvertedCompYearly', ascending=False).reset_index(drop=True).head(5)
print(level_educ)

"""Бонусні запитання:"""
"""В кожній віковій категорії, який відсоток респондентів програмує на Python?"""
# Глянемо, які відповіді зазначені у стовпцю 'Age'.
unique_responses_ = data_df['Age'].unique()
print("Унікальні відповіді:", unique_responses_)

# Унікальні вікові категорії
age_categories = ['Prefer not to say', 'Under 18 years old', '18-24 years old', '25-34 years old',
                  '35-44 years old', '45-54 years old', '55-64 years old', '65 years or older']

# Перевірка чи респонденти програмують на Python
python_devs = data_df[data_df['LanguageHaveWorkedWith'].str.contains('Python', na=False)]

# Створення порожнього словника для результатів
age_python_percent = {}

# Для кожної вікової категорії
for category in age_categories:
    # Відбираємо респондентів з цієї вікової категорії
    age_group = data_df[data_df['Age'] == category]

    # Респонденти в Python
    python_in_group = python_devs[python_devs['Age'] == category]

    # Обчислюємо відсоток
    percent = (len(python_in_group) / len(age_group)) * 100 if len(age_group) > 0 else 0
    age_python_percent[category] = percent

# Виводимо відсотки для кожної вікової категорії
for category, percent in age_python_percent.items():
    print(f"Вікова категорія: {category} - Відсоток програмістів на Python: {percent:.2f}%")


"""Серед респондентів що знаходяться в 75 перцентилі за компенсацією середнього і працюють віддалено, які індустрії є найрозповсюдженішими?"""

# Перевіримо як називаються потрібні колонки до цього запитання.
print(list(data_df.columns))

# Перевіримо наявних значень у стовпці RemoteWork
print(data_df['RemoteWork'].unique())

print(data_df[(data_df.ConvertedCompYearly > data_df.ConvertedCompYearly.quantile(0.75)) & \
              (data_df.RemoteWork == 'Remote')].Industry.value_counts().reset_index())