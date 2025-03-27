import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("facebook_ads_data (2.0).csv")
print(df.head(5))


# Перетворюємо 'ad_date' у datetime
df['ad_date'] = pd.to_datetime(df['ad_date'], errors='coerce')

# Фільтруємо лише 2021 рік
df_2021 = df[df['ad_date'].dt.year == 2021]

# Групуємо дані за днями та сумуємо значення
daily_stat = df_2021.groupby('ad_date')[['total_spend', 'total_impressions', 'total_clicks', 'total_value']].sum()
daily_stat = daily_stat.reset_index()

# Створення сітки для перших 6 графіків
fig, axes = plt.subplots(3, 2, figsize=(15, 15))

# 1. Графік Щоденні витрати на рекламу у 2021 році
axes[0, 0].plot(daily_stat['ad_date'], daily_stat['total_spend'], label='Total spend')
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Total spend ($)")
axes[0, 0].set_title("Щоденні витрати на рекламу у 2021 році")
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].legend(loc='upper right')

# 2. Графік Щоденні витрати на рекламу у 2021 році та 7 денне середнє
axes[0, 1].plot(daily_stat['ad_date'], daily_stat['total_spend'].rolling(7).mean(), label='Total spend')
axes[0, 1].set_xlabel("Date")
axes[0, 1].set_ylabel("Total spend ($)")
axes[0, 1].set_title("Щоденні витрати на рекламу у 2021 році та 7 денне середнє")
axes[0, 1].tick_params(axis='x', rotation=45)
axes[0, 1].legend(loc='upper right')

# 3. Графік Щоденний ROMI у 2021 році
daily_stat['romi'] = daily_stat['total_value'] / daily_stat['total_spend']
axes[1, 0].plot(daily_stat['ad_date'], daily_stat['romi'], label='ROMI')
axes[1, 0].set_xlabel("Date")
axes[1, 0].set_ylabel("ROMI")
axes[1, 0].set_title("Щоденний ROMI у 2021 році")
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].legend(loc='upper right')

# 4. Графік Щоденний ROMI у 2021 році та 7 денне середнє
axes[1, 1].plot(daily_stat['ad_date'], daily_stat['romi'].rolling(7).mean(), label='ROMI')
axes[1, 1].set_xlabel("Date")
axes[1, 1].set_ylabel("ROMI")
axes[1, 1].set_title("Щоденний ROMI у 2021 році та 7 денне середнє")
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].legend(loc='upper right')

# 5. Графік Загальна сума витрат на рекламу в кожній з кампаній
daily_stat_campaign = df.groupby('campaign_name')[['total_spend', 'total_impressions', 'total_clicks', 'total_value']].sum().reset_index()
axes[2, 0].barh(daily_stat_campaign['campaign_name'], daily_stat_campaign.sort_values('total_spend')['total_spend'])
axes[2, 0].set_xlabel("Total spend")
axes[2, 0].set_ylabel("Campaign Name")
axes[2, 0].set_title("Загальна сума витрат на рекламу в кожній з кампаній")

# 6. Графік Загальний ROMI в кожній з кампаній"
daily_stat_campaign['romi'] = daily_stat_campaign['total_value'] / daily_stat_campaign['total_spend']
axes[2, 1].barh(daily_stat_campaign['campaign_name'], daily_stat_campaign.sort_values('romi')['romi'])
axes[2, 1].set_xlabel("ROMI")
axes[2, 1].set_ylabel("Campaign Name")
axes[2, 1].set_title("Загальний ROMI в кожній з кампаній")

# Відображення перших 6 графіків
plt.tight_layout(pad=3.0)  # Відступи між графіками
plt.subplots_adjust(top=0.95, bottom=0.05)  # Відступи з верхньої та нижньої частини
plt.show()

# Створення сітки для останніх 4 графіків
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 7. Boxplot Розподіл ROMI по кампаніях
sns.boxplot(x='campaign_name', y='romi', data=df, ax=axes[0, 0])
axes[0, 0].set_xlabel("Campaign Name")
axes[0, 0].set_ylabel("ROMI")
axes[0, 0].set_title("Розподіл ROMI по кампаніях")
axes[0, 0].tick_params(axis='x', rotation=90)

# 8. Гістограма розподілу ROMI
sns.histplot(df['romi'], ax=axes[0, 1])
axes[0, 1].set_title("Гістограма розподілу ROMI")

# 9. матриця Кореляція між числовими показниками
all_indicators_corr = df.loc[:, 'total_spend':].corr()
sns.heatmap(all_indicators_corr, annot=True, fmt='.0%', cmap='crest_r', ax=axes[1, 0])
axes[1, 0].set_title("Кореляція між числовими показниками")

# 10. Лінійна регресія між витратами та цінністю
sns.regplot(data=df, x='total_spend', y='total_value', scatter_kws={'alpha':0.5}, line_kws={'color':'blue'}, ax=axes[1, 1])
axes[1, 1].set_title("Зв’язок між витратами на рекламу та цінністю")

# Відображення останніх 4 графіків
plt.tight_layout(pad=3.0)  # Відступи між графіками
plt.subplots_adjust(top=0.95, bottom=0.05)  # Відступи з верхньої та нижньої частини
plt.show()