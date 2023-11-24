import pandas as pd
from datetime import datetime

def calculate_employer_age(DateBirth):
    today = datetime.today()
    employer_age = today.year - DateBirth.year - ((today.month, today.day) < (DateBirth.month, DateBirth.day))
    return employer_age

try:
    df = pd.read_csv('filetab.csv', encoding='utf-8')

    with pd.ExcelWriter('filetab1.xlsx', engine='xlsxwriter') as writer:
        df_all = pd.DataFrame(columns=["Прізвище", "Ім’я", "По батькові", "Дата народження", "Стать", "Посада", "Місто проживання", "Адреса проживання", "Моб. ном. телефону", "Email"])
        df_younger_18 = pd.DataFrame(columns=["№", "Прізвище", "Ім’я", "По батькові", "Дата народження", "Вік"])
        df_18_45 = pd.DataFrame(columns=["№", "Прізвище", "Ім’я", "По батькові", "Дата народження", "Вік"])
        df_45_70 = pd.DataFrame(columns=["№", "Прізвище", "Ім’я", "По батькові", "Дата народження", "Вік"])
        df_older_70 = pd.DataFrame(columns=["№", "Прізвище", "Ім’я", "По батькові", "Дата народження", "Вік"])

        count_all = 0
        count_younger_18 = 0
        count_18_45 = 0
        count_45_70 = 0
        count_older_70 = 0

        for index, row in df.iterrows():
            birthdate = datetime.strptime(row["Дата народження"], '%d.%m.%Y')
            age = calculate_employer_age(birthdate)

            if age < 18:
                category_df = df_younger_18
                count_younger_18 += 1
                row_number = count_younger_18
            elif 18 <= age <= 45:
                category_df = df_18_45
                count_18_45 += 1
                row_number = count_18_45
            elif 45 < age <= 70:
                category_df = df_45_70
                count_45_70 += 1
                row_number = count_45_70
            else:
                category_df = df_older_70
                count_older_70 += 1
                row_number = count_older_70

            count_all += 1
            df_all = df_all.append(row)

            category_df = category_df.append({"№": row_number, "Прізвище": row["Прізвище"], "Ім’я": row["Ім’я"], "По батькові": row["По батькові"], "Дата народження": row["Дата народження"], "Вік": age}, ignore_index=True)

        df_all.to_excel(writer, sheet_name="all", index=False)
        df_younger_18.to_excel(writer, sheet_name="younger_18", index=False)
        df_18_45.to_excel(writer, sheet_name="18-45", index=False)
        df_45_70.to_excel(writer, sheet_name="45-70", index=False)
        df_older_70.to_excel(writer, sheet_name="older_70", index=False)

    print("Файл filetab1.xlsx створено ")

except FileNotFoundError:
    print("Повідомлення про відсутність, або проблеми при відкритті файлу CSV.")
except Exception as e:
    print("Повідомлення про неможливість створення XLSX файлу:", str(e))
