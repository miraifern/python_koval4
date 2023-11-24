import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def calculate_employee_age(date_of_birth):
    today = datetime.today()
    employee_age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return employee_age

def generate_employee_statistics():
    try:
        df = pd.read_csv('filetab.csv', encoding='utf-8', parse_dates=['Дата народження'])

        age_categories = {
            "younger_18": {"male": 0, "female": 0},
            "18-45": {"male": 0, "female": 0},
            "45-70": {"male": 0, "female": 0},
            "older_70": {"male": 0, "female": 0}
        }
        gender_count = {"male": 0, "female": 0}

        for index, row in df.iterrows():
            age = calculate_employee_age(row["Дата народження"])
            if age < 18:
                age_category = "younger_18"
            elif 18 <= age <= 45:
                age_category = "18-45"
            elif 45 < age <= 70:
                age_category = "45-70"
            else:
                age_category = "older_70"

            if row["Стать"] == "Ч":
                gender_category = "male"
                gender_count["male"] += 1
            elif row["Стать"] == "Ж":
                gender_category = "female"
                gender_count["female"] += 1
            else:
                continue

            age_categories[age_category][gender_category] += 1

        print("\nРозподіл за статтю:")
        print(f"Ч: {gender_count['male']}")
        print(f"Ж: {gender_count['female']}")

        show_gender_chart(gender_count)
        show_age_distribution_chart(age_categories)
        show_gender_age_stacked_bar_chart(age_categories)

        print("\nРозподіл за віком:")
        for category, counts in age_categories.items():
            print(f"{category}: {counts['male'] + counts['female']}")

        print("\nРозподіл за статтю та віком:")
        for category, counts in age_categories.items():
            print(f"{category}: Ч - {counts['male']}, Ж - {counts['female']}")

        print("Ok")
    except FileNotFoundError:
        print("Повідомлення про відсутність, або проблеми при відкритті файлу CSV.")
    except Exception as e:
        print("Помилка:", str(e))

def show_age_distribution_chart(age_categories):
    categories = list(age_categories.keys())
    total_counts = [counts["male"] + counts["female"] for counts in age_categories.values()]
    plt.figure()
    plt.bar(categories, total_counts, color='grey')
    plt.xlabel('Вікова категорія')
    plt.ylabel('Кількість співробітників')
    plt.title('Розподіл за віком')
    plt.xticks(rotation=45)

def show_gender_age_stacked_bar_chart(age_categories):
    categories = list(age_categories.keys())
    male_counts = [counts["male"] for counts in age_categories.values()]
    female_counts = [counts["female"] for counts in age_categories.values()]
    bar_width = 0.35
    index = range(len(categories))
    plt.figure()
    plt.bar(index, male_counts, bar_width, label='Ч', color='green')
    plt.bar(index, female_counts, bar_width, label='Ж', color='yellow', bottom=male_counts)
    plt.xlabel('Вікова категорія')
    plt.ylabel('Кількість співробітників')
    plt.title('Розподіл за віком та статтю')
    plt.xticks(index, categories, rotation=45)
    plt.legend()

def show_gender_chart(gender_counts):
    labels = 'Чоловіча стать', 'Жіноча стать'
    sizes = [gender_counts["male"], gender_counts["female"]]
    colors = ['green', 'yellow']
    plt.figure()
    plt.pie(sizes, labels=labels, colors=colors, autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '', startangle=140)
    plt.axis('equal')
    plt.title('Розподіл за статтю')

generate_employee_statistics()
plt.show()
