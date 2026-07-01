import numpy as np
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox


file_path = 'insurance.csv'#Place this file in the same folder as the code.
df = pd.read_csv(file_path)

sex_map = {'female': 1, 'male': 0}
smoker_map = {'yes': 1, 'no': 0}
region_map = {
    'southwest': 0,
    'southeast': 1,
    'northwest': 2,
    'northeast': 3
}

df_encoded = df.copy()
df_encoded['sex'] = df_encoded['sex'].map(sex_map)
df_encoded['smoker'] = df_encoded['smoker'].map(smoker_map)
df_encoded['region'] = df_encoded['region'].map(region_map)

x = df_encoded.iloc[:, 0:6].values
y = df_encoded.iloc[:, 6].values


def run_cbr():
    global x, y, df, df_encoded
    try:
        sex_val = 1 if sex_var.get() == "Female" else 0
        smoker_val = 1 if smoker_var.get() == "Yes" else 0

        xnew = np.array([
            float(age_entry.get()),
            sex_val,
            float(bmi_entry.get()),
            float(children_entry.get()),
            smoker_val,
            region_map[region_var.get().lower()]
        ])


        existing_index = None
        for i in range(len(x)):
            if np.array_equal(x[i], xnew):
                existing_index = i
                break
        if existing_index is not None:
            result_label.configure(
                text=
                f"The case already exists\n"
                f"Case number in Dataset: {existing_index + 2}\n\n"
                f"Age: {int(x[existing_index][0])}\n"
                f"Sex: {'Female' if x[existing_index][1] == 1 else 'Male'}\n"
                f"BMI: {x[existing_index][2]:.2f}\n"
                f"Children: {int(x[existing_index][3])}\n"
                f"Smoker: {'Yes' if x[existing_index][4] == 1 else 'No'}\n"
                f"Region: {['Southwest','Southeast','Northwest','Northeast'][int(x[existing_index][5])]}"
            )
            price_label.configure(text=f"${y[existing_index]:,.2f}")
            return

        distances = []
        for i in range(len(x)):
            d = 0
            for j in range(len(x[0])):
                d += abs(x[i][j] - xnew[j])
            distances.append(d)

        min_index = distances.index(min(distances))
        predicted_price = float(y[min_index])
        nearest = x[min_index]

        new_case = {
            'age': xnew[0],
            'sex': 'female' if sex_val == 1 else 'male',
            'bmi': xnew[2],
            'children': int(xnew[3]),
            'smoker': 'yes' if smoker_val == 1 else 'no',
            'region': region_var.get().lower(),
            'charges': predicted_price
        }

        df = pd.concat([df, pd.DataFrame([new_case])], ignore_index=True)
        df.to_csv(file_path, index=False)


        df_encoded = df.copy()
        df_encoded['sex'] = df_encoded['sex'].map(sex_map)
        df_encoded['smoker'] = df_encoded['smoker'].map(smoker_map)
        df_encoded['region'] = df_encoded['region'].map(region_map)

        x = df_encoded.iloc[:, 0:6].values
        y = df_encoded.iloc[:, 6].values

        result_label.configure(
            text=
            f"New case (added to the dataset)\n"
            f"nearest case:\n"
            f"Age: {int(nearest[0])}\n"
            f"Sex: {'Female' if nearest[1] == 1 else 'Male'}\n"
            f"BMI: {nearest[2]:.2f}\n"
            f"Children: {int(nearest[3])}\n"
            f"Smoker: {'Yes' if nearest[4] == 1 else 'No'}\n"
            f"Region: {['Southwest','Southeast','Northwest','Northeast'][int(nearest[5])]}"
        )
        price_label.configure(text=f"${predicted_price:,.2f}")

    except Exception as e:
        messagebox.showerror("خطأ", f"تحقق من القيم المدخلة\n{e}")


NAVY = "#132A43"
NAVY_DEEP = "#0B1D31"
GOLD = "#D9A441"
GOLD_SOFT = "#F1D9A6"
CREAM = "#FAF6EE"
CARD = "#FFFFFF"
LINE = "#E4DCC9"
MUTED = "#5C6A76"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("CBR Insurance Pricing System")
root.geometry("860x700")
root.configure(fg_color=CREAM)

header = ctk.CTkFrame(root, fg_color=NAVY_DEEP, corner_radius=0, height=60)
header.pack(fill="x", side="top")
ctk.CTkLabel(
    header, text="●  ●  ●   cbr_insurance_pricing.py",
    font=ctk.CTkFont(family="Consolas", size=12),
    text_color="#B9C6D3"
).pack(side="left", padx=20, pady=16)

title_frame = ctk.CTkFrame(root, fg_color=CREAM)
title_frame.pack(fill="x", padx=36, pady=(24, 4))
ctk.CTkLabel(
    title_frame, text="CASE-BASED REASONING · INSURANCE PRICING",
    font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
    text_color="#4E8388"
).pack(anchor="w")
ctk.CTkLabel(
    title_frame, text="Estimate a New Case",
    font=ctk.CTkFont(family="Georgia", size=30, weight="bold"),
    text_color=NAVY
).pack(anchor="w", pady=(2, 0))
ctk.CTkLabel(
    title_frame,
    text="Enter a person's details. The system retrieves the closest matching case on record.",
    font=ctk.CTkFont(family="Segoe UI", size=14),
    text_color=MUTED
).pack(anchor="w", pady=(4, 0))

body = ctk.CTkFrame(root, fg_color=CREAM)
body.pack(fill="both", expand=True, padx=36, pady=16)
body.grid_columnconfigure(0, weight=1)
body.grid_columnconfigure(1, weight=1)

left_frame = ctk.CTkFrame(body, fg_color=CARD, corner_radius=12, border_width=1, border_color=LINE)
left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

ctk.CTkLabel(
    left_frame, text="●  NUMERICAL INPUTS",
    font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
    text_color=NAVY
).pack(anchor="w", padx=18, pady=(16, 10))

def add_field(parent, label_text):
    ctk.CTkLabel(
        parent, text=label_text,
        font=ctk.CTkFont(family="Segoe UI", size=14), text_color=MUTED
    ).pack(anchor="w", padx=18, pady=(6, 2))
    entry = ctk.CTkEntry(
        parent, font=ctk.CTkFont(family="Consolas", size=15),
        fg_color="#FCFAF4", border_color=LINE, text_color=NAVY_DEEP,
        corner_radius=8, height=38
    )
    entry.pack(fill="x", padx=18, pady=(0, 6))
    return entry

age_entry = add_field(left_frame, "Age")
bmi_entry = add_field(left_frame, "BMI")
children_entry = add_field(left_frame, "Children")
ctk.CTkLabel(left_frame, text="", height=6).pack()

right_frame = ctk.CTkFrame(body, fg_color=CARD, corner_radius=12, border_width=1, border_color=LINE)
right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

ctk.CTkLabel(
    right_frame, text="●  CATEGORICAL INPUTS",
    font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
    text_color=NAVY
).pack(anchor="w", padx=18, pady=(16, 10))

def add_dropdown(parent, label_text, options):
    ctk.CTkLabel(
        parent, text=label_text,
        font=ctk.CTkFont(family="Segoe UI", size=14), text_color=MUTED
    ).pack(anchor="w", padx=18, pady=(6, 2))
    var = ctk.StringVar(value="choose")
    menu = ctk.CTkOptionMenu(
        parent, variable=var, values=options,
        fg_color="#FCFAF4", text_color=NAVY_DEEP, button_color=GOLD,
        button_hover_color="#C6913A", dropdown_fg_color=CARD,
        font=ctk.CTkFont(family="Segoe UI", size=14), corner_radius=8, height=38
    )
    menu.pack(fill="x", padx=18, pady=(0, 6))
    return var

sex_var = add_dropdown(right_frame, "Sex", ["Female", "Male"])
smoker_var = add_dropdown(right_frame, "Smoker", ["Yes", "No"])
region_var = add_dropdown(right_frame, "Region", ["Southwest", "Southeast", "Northwest", "Northeast"])

btn_frame = ctk.CTkFrame(root, fg_color=CREAM)
btn_frame.pack(fill="x", padx=36, pady=(6, 4))
ctk.CTkButton(
    btn_frame, text="Calculate the Price  →",
    font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
    fg_color=NAVY, hover_color=NAVY_DEEP, text_color=GOLD_SOFT,
    corner_radius=10, height=46, command=run_cbr
).pack(pady=6)

results_frame = ctk.CTkFrame(root, fg_color=CREAM)
results_frame.pack(fill="both", expand=False, padx=36, pady=(6, 24))
results_frame.grid_columnconfigure(0, weight=2)
results_frame.grid_columnconfigure(1, weight=1)

result_card = ctk.CTkFrame(results_frame, fg_color=NAVY, corner_radius=12)
result_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

result_label = ctk.CTkLabel(
    result_card, text="Results will appear here after calculation.",
    font=ctk.CTkFont(family="Consolas", size=14),
    text_color="#EAF0F4", justify="left", anchor="w"
)
result_label.pack(fill="both", padx=20, pady=18)

price_card = ctk.CTkFrame(results_frame, fg_color=GOLD, corner_radius=12)
price_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

ctk.CTkLabel(
    price_card, text="PREDICTED PRICE",
    font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
    text_color=NAVY_DEEP
).pack(anchor="w", padx=20, pady=(18, 4))

price_label = ctk.CTkLabel(
    price_card, text="—",
    font=ctk.CTkFont(family="Georgia", size=28, weight="bold"),
    text_color=NAVY_DEEP
)
price_label.pack(anchor="w", padx=20, pady=(0, 18))

root.mainloop()