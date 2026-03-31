import pandas as pd

file = "TR UPDATED 2025-26 N.xlsm"

all_data = []
roll_counter = 1

sheets = pd.read_excel(file, sheet_name=None)

for sheet_name, df in sheets.items():

    # 🔥 SKIP FIRST FEW ROWS (IMPORTANT)
    df = df.iloc[2:]  # skip top 2 rows (adjust if needed)

    # Reset header row
    df.columns = [str(col).strip().lower() for col in df.iloc[0]]
    df = df[1:]

    name_col = "name of student"
    phone_col = "contact no."

    if name_col not in df.columns:
        continue

    # Class logic
    if str(sheet_name).lower() == "ukg":
        class_num = 1
    else:
        try:
            class_num = int(sheet_name) + 1
        except:
            continue

    for _, row in df.iterrows():

        name = str(row.get(name_col, "")).strip()

        if name == "" or name.lower() == "nan":
            continue

        phone = str(row.get(phone_col, "")).strip()

        all_data.append([roll_counter, name, phone, class_num])

        roll_counter += 1


final_df = pd.DataFrame(all_data, columns=["roll", "name", "parent_phone", "class"])

final_df.to_csv("students.csv", index=False)

print("✅ students.csv created with", len(final_df), "students")
