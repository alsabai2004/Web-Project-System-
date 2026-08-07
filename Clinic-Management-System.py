# ------------------- استيراد المكتبات ------------------- #
import json
import os

# ------------------- تعريف الملف ------------------- #
FILENAME = "clinic_data.txt"

# ------------------- تحميل البيانات ------------------- #
def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

# ------------------- حفظ البيانات ------------------- #
def save_data(data):
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)

# ------------------- الصفحة الرئيسية ------------------- #
def main_menu():
    while True:
        print("""
================= MAIN PAGE =================
Press[1]: Go to the secretary
Press[2]: Go to the doctor
Press[3]: Go to the pharmacy
Press[4]: Set in the waiting room
=============================================""")
        choice = input("Enter your choice: ")

        if choice == "1":
            secretary_interface()
        elif choice == "2":
            doctor_interface()
        elif choice == "3":
            pharmacist_interface()
        elif choice == "4":
            print("You're now in the waiting room...")
        else:
            print("Invalid choice, try again.")

# ------------------- سكرتير ------------------- #
def secretary_interface():
    data = load_data()
    while True:
        print("""
=========== SECRETARY PAGE ===========
Press [1]: Add patient
Press [2]: View one patient informations
Press [3]: View all patients informations
Press [4]: Delete patient
Press [5]: Change the patient's informations
Press [6]: Go to the waiting room
Press [7]: Save the informations in a document
Press [8]: Delete the document
=======================================""")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_patient(data)
        elif choice == "2":
            view_one_patient(data)
        elif choice == "3":
            show_all_patients()
        elif choice == "4":
            delete_patient(data)
        elif choice == "5":
            edit_patient(data)
        elif choice == "6":
            break
        elif choice == "7":
            save_data(data)
            print("Data saved successfully.")
        elif choice == "8":
            if os.path.exists(FILENAME):
                os.remove(FILENAME)
                print("Document deleted.")
            else:
                print("No document found to delete.")
        else:
            print("Invalid choice, try again.")

# ------------------- إضافة مريض ------------------- #
def add_patient(data):
    n = int(input("Enter the number of patients you want to add: "))
    for i in range(n):
        print(f"Adding patient {i+1}")
        name = input("Full name: ")
        age = input("Age: ")
        sex = input("Sex (male/female): ")
        phone = input("Phone number: ")
        whatsapp = input("WhatsApp number: ")
        fees = input("Register fees (type 'ok' if paid): ")
        if fees.lower() != "ok":
            print("Registration not complete.")
            return
        visit_day = input("Visit day: ")
        visit_month = input("Visit month: ")
        visit_year = input("Visit year: ")

        patient_id = str(len(data) + 1)
        data[patient_id] = {
            "Id": int(patient_id),
            "Name": name,
            "Age": age,
            "Sex": sex,
            "Register fees": fees,
            "Sick condition": "None",
            "Medicines": {},
            "Visit date": f"{visit_day}/{visit_month}/{visit_year}",
            "Return date": "None",
            "Contact": {
                "WhatsApp": whatsapp,
                "Phone": phone
            }
        }
    save_data(data)

# ------------------- عرض مريض واحد ------------------- #
def view_one_patient(data):
    name = input("Enter the patient's full name: ")
    found = False
    for patient in data.values():
        if patient["Name"].lower() == name.lower():
            for k, v in patient.items():
                print(f"{k} : {v}")
            found = True
            break
    if not found:
        print("Patient not found.")

# ------------------- عرض كل المرضى ------------------- #
def show_all_patients():
    data = load_data()
    if not data:
        print("No records found.")
    else:
        for patient in data.values():
            print("-" * 50)
            for k, v in patient.items():
                print(f"{k} : {v}")

# ------------------- حذف مريض ------------------- #
def delete_patient(data):
    name = input("Enter the patient's full name to delete: ")
    for pid in list(data):
        if data[pid]["Name"].lower() == name.lower():
            del data[pid]
            print("Patient deleted.")
            save_data(data)
            return
    print("Patient not found.")

# ------------------- تعديل بيانات مريض ------------------- #
def edit_patient(data):
    name = input("Enter the patient's full name to edit: ")
    for patient in data.values():
        if patient["Name"].lower() == name.lower():
            while True:
                print("""
What do you want to change?
1: Name
2: Age
3: Sex
4: Sick condition
5: Medicines
6: Visit date
7: Return date
8: Contact
9: Stop
""")
                option = input("Enter option number: ")
                if option == "1":
                    patient["Name"] = input("New name: ")
                elif option == "2":
                    patient["Age"] = input("New age: ")
                elif option == "3":
                    patient["Sex"] = input("New sex: ")
                elif option == "4":
                    patient["Sick condition"] = input("New condition: ")
                elif option == "5":
                    key = input("Disease name: ")
                    val = input("Medicine: ")
                    patient["Medicines"][key] = val
                elif option == "6":
                    day = input("Day: ")
                    month = input("Month: ")
                    year = input("Year: ")
                    patient["Visit date"] = f"{day}/{month}/{year}"
                elif option == "7":
                    day = input("Day: ")
                    month = input("Month: ")
                    year = input("Year: ")
                    patient["Return date"] = f"{day}/{month}/{year}"
                elif option == "8":
                    phone = input("Phone: ")
                    whatsapp = input("WhatsApp: ")
                    patient["Contact"] = {"Phone": phone, "WhatsApp": whatsapp}
                elif option == "9":
                    break
                else:
                    print("Invalid option")
            save_data(data)
            return
    print("Patient not found.")

# ------------------- واجهة الطبيب ------------------- #
def doctor_interface():
    data = load_data()
    name = input("Doctor, enter patient's full name: ")
    for patient in data.values():
        if patient["Name"].lower() == name.lower():
            condition = input("Enter condition status (good, so so, bad): ")
            patient["Sick condition"] = condition
            while True:
                disease = input("Enter disease (or 'done'): ")
                if disease.lower() == 'done':
                    break
                med = input(f"Medicine for {disease}: ")
                patient["Medicines"][disease] = med
            ret = input("Is there a return date? (yes/no): ")
            if ret.lower() == "yes":
                day = input("Day: ")
                month = input("Month: ")
                year = input("Year: ")
                patient["Return date"] = f"{day}/{month}/{year}"
            save_data(data)
            return
    print("Patient not found.")

# ------------------- واجهة الصيدلي ------------------- #
def pharmacist_interface():
    while True:
        print("\n========== Pharmacist Interface ==========")
        print("Press[1]: Show all patient data")
        print("Press[2]: Back to main page")
        choice = input("Enter your choice: ")

        if choice == "1":
            show_all_patients()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Try again.")

# ------------------- تشغيل البرنامج ------------------- #
if __name__ == "__main__":
    main_menu()
    
