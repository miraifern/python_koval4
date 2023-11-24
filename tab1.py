import pandas as pd
from faker import Faker
import random

fake = Faker('uk_UA')

def MiddleNameMale(fake):
    male_middle_names = [
        "Олексійович", "Михайлович", "Дмитрович", "Едуардович", "Богданович",
        "Сергійович", "Андрійович", "Петрович", "Єгорович", "Володимирович"
    ]
    return fake.random_element(male_middle_names)

def MiddleNameFemale(fake):
    female_middle_names = [
        "Олексіївна", "Михайлівна", "Дмитрівна", "Едуардівна", "Богданівна",
        "Сергіївна", "Андріївна", "Петрівна", "Єгорівна", "Володимирівна"
    ]
    return fake.random_element(female_middle_names)

num_records = 2000

records = []

for i in range(num_records):
    if i < num_records * 0.4:
        gender = "Ж"
        first_name = fake.first_name_female()
        middle_name = MiddleNameFemale(fake)

    else:
        gender = "Ч"
        first_name = fake.first_name_male()
        middle_name = MiddleNameMale(fake)

    birthdate = fake.date_of_birth(minimum_age=15, maximum_age=85)
    record = {
        "Прізвище": fake.last_name(),
        "Ім’я": first_name,
        "По батькові": middle_name,
        "Стать": gender,
        "Дата народження": birthdate.strftime('%d.%m.%Y'),
        "Посада": fake.job(),
        "Місто проживання": fake.city(),
        "Адреса проживання": fake.address(),
        "Моб. ном. телефону": fake.phone_number(),
        "Email": fake.email()
    }
    records.append(record)

random.shuffle(records)

df = pd.DataFrame(records)

df.to_csv('filetab.csv', index=False, encoding='utf-8')

print("filetab.csv створено.")
