import numpy as np
import pandas as pd


applications_path = pd.read_csv("applications(2.0).csv")
industries_path = pd.read_csv("industries(2.0).csv")

industries_data = pd.DataFrame(industries_path)
applications_data = pd.DataFrame(applications_path)

# # Встановлюємо максимальну кількість рядків для виведення
pd.set_option('display.max_columns', None)  # Показуємо всі стовпці
print(applications_data.head(5))


"""Приберемо дублікати applicant_id."""
# До видалення дублікатів з колонки 'applicant_id'
print("До видалення дублікатів -", applications_data['applicant_id'].shape[0])

# Після видалення дублікатів з колонки 'applicant_id'
applications_data.drop_duplicates(subset="applicant_id", keep="last", inplace=True)
print("Після видалення дублікатів -", applications_data['applicant_id'].shape[0])


"""В полі 'External Rating' заповнимо відсутні значення нулями."""
applications_data['External Rating'].fillna(0, inplace=True)
print(applications_data.head(5))


"""В полі 'Education level' заповнимо відсутні значення текстом “Середня”."""
# Для початку перевіримо, які відповіді записані у дану таблицю.
unique_responses = applications_data['Education level'].unique()
print("Унікальні відповіді у стовпці Education level:", unique_responses, )

# Далі порахуємо кількість там пустих значень до
education_na = applications_data['Education level'].isna()
count_na = education_na.sum()
print("Кількість пустих значень у стовпці Education level до:",count_na)

applications_data['Education level'].fillna('Середня', inplace=True)

# Далі порахуємо кількість там пустих значень після
education_na = applications_data['Education level'].isna()
count_na = education_na.sum()
print("Кількість пустих значень у стовпці Education level після:",count_na)
print(applications_data.head(5))

# Додамо до цього DataFrame дані з файлу industries.csv, а саме, рейтинги індустрій.
merged_data = pd.merge(applications_data, industries_data)
merged_data.head(5)


"""Переводимо стовпець 'Applied at' в формат datetime"""
merged_data['Applied at'] = pd.to_datetime(merged_data['Applied at'], format='mixed', dayfirst=True, errors='coerce')
merged_data.head(5)


"""Розраховано рейтинг заявки за наступними умовами:

Рейтинг має бути числом від 0 до 100.

Рейтинг - сума оцінок заявки по 6 критеріям.

Рейтинг дорівнює нулю, якщо відсутнє значення 'Amount' або якщо 'External Rating' дорівнює нулю.

Якщо вік заявника між 35 та 55, до рейтингу додається 20 балів.

Якщо заявка була подана не у вихідні, до рейтингу додається 20 балів.

Якщо заявника одружений, до рейтингу додається 20 балів.

Якщо заявника знаходиться в Києві чи області, до рейтингу додається 10 балів Значення 'Score' з таблиці industries.csv також додається до заявки (і складає від 0 до 20 балів).

Якщо 'External Rating' більше чи дорівнює 7, до рейтингу додається 20 балів.

Якщо 'External Rating' менше чи дорівнює 2, з рейтингу віднімається 20 балів."""

# Функція для розрахунку рейтингу заявки
def calculate_rating(row):

    rating = 0

    # Перевірка на відсутність 'Amount' або 'External Rating'
    if pd.isna(row['Amount']) or row['External Rating'] == 0:
        return 0  # Рейтинг 0, якщо немає 'Amount' або 'External Rating' дорівнює 0

    # Вік заявника (між 35 і 55)
    if 35 <= row['Age'] <= 55:
        rating += 20

    # Час подачі заявки (не у вихідні)
    if pd.to_datetime(row['Applied at']).weekday() < 5:  # weekday() < 5 означає не вихідний
        rating += 20

    # Сімейний стан (якщо одружений)
    if row['Marital status'] == 'Married':
        rating += 20

    # Місцезнаходження (Київ або область)
    if row['Location'] in ['Київ чи область']:  # Перевіряємо, чи знаходиться в Києві чи області
        rating += 10

    # Рейтинг індустрії (значення 'Score' з industries.csv)
    if pd.notna(row['Score']):
        rating += row['Score']

    # Зовнішній рейтинг
    if row['External Rating'] >= 7:
        rating += 20
    elif row['External Rating'] <= 2:
        rating -= 20

    # Обмежуємо рейтинг до діапазону від 0 до 100
    rating = min(max(rating, 0), 100)

    # Повертаємо розрахований рейтинг
    return rating

# Додаємо новий стовпчик 'Rating' з обчисленим рейтингом
merged_data['Rating'] = merged_data.apply(calculate_rating, axis=1)

# Перевіряємо перші кілька рядків об'єднаної таблиці з рейтингами
print(merged_data.head(5))


"""В результуючій таблиці залишемо лише заявки з рейтингом більше нуля, ці заявки вважатимуться прийнятими."""
updated_data = merged_data[merged_data['Rating'] > 0]
print(updated_data.head(10))


"""Дані з результуючої таблиці згрупуємо за тижнем подачі заявки та виведемо середній рейтинг прийнятих заявок у кожен тиждень."""
# 1. Перетворюємо 'Applied at' у datetime
# updated_data['Applied at'] = pd.to_datetime(updated_data['Applied at'], errors='coerce')

# 2. Встановлюємо 'Applied at' як індекс
updated_data = updated_data.set_index('Applied at')

# 3. Групуємо за тижнями і рахуємо середнє
weekly_avg_rating = updated_data['Rating'].resample('W').mean().round(1).dropna().reset_index()

# 4. Перейменовуємо стовпці
weekly_avg_rating.rename(columns={'Applied at': 'Week Start', 'Rating': 'Average Rating'}, inplace=True)
print(weekly_avg_rating)