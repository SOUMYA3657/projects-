import tkinter as tk
from tkinter import messagebox, filedialog
import string
import random

def get_strength(pw):
    length = len(pw)
    has_upper = any(c.isupper() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_special = any(c in string.punctuation for c in pw)
    score = sum([has_upper, has_digit, has_special]) + (length >= 12)
    return ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"][min(score, 4)]

def generate_password(length, use_upper, use_digits, use_special):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_upper else ''
    digits = string.digits if use_digits else ''
    special = string.punctuation if use_special else ''
    all_chars = lower + upper + digits + special

    if not all_chars:
        return "Error: No characters selected"

    password = [
        random.choice(lower),
        random.choice(upper) if use_upper else '',
        random.choice(digits) if use_digits else '',
        random.choice(special) if use_special else ''
    ]
    password += random.choices(all_chars, k=length - len(password))
    random.shuffle(password)
    return ''.join(password)

def generate():
    try:
        length = int(length_entry.get())
        count = int(count_entry.get())
        use_upper = upper_var.get()
        use_digits = digit_var.get()
        use_special = special_var.get()

        results.delete(1.0, tk.END)
        for _ in range(count):
            pw = generate_password(length, use_upper, use_digits, use_special)
            results.insert(tk.END, f"{pw} | Strength: {get_strength(pw)}\n")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

def save_passwords():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as f:
            f.write(results.get(1.0, tk.END))
        messagebox.showinfo("Saved", f"Passwords saved to {file_path}")
        
def copy_password():
    selected = results.get(tk.SEL_FIRST, tk.SEL_LAST)
    root.clipboard_clear()
    root.clipboard_append(selected)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

root = tk.Tk()
root.title("Advanced Password Generator")

tk.Label(root, text="Password Length:").grid(row=0, column=0, sticky='e')
length_entry = tk.Entry(root)
length_entry.insert(0, "12")
length_entry.grid(row=0, column=1)

tk.Label(root, text="Number of Passwords:").grid(row=1, column=0, sticky='e')
count_entry = tk.Entry(root)
count_entry.insert(0, "5")
count_entry.grid(row=1, column=1)

upper_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Uppercase", variable=upper_var).grid(row=2, column=0, sticky='w')
tk.Checkbutton(root, text="Include Digits", variable=digit_var).grid(row=2, column=1, sticky='w')
tk.Checkbutton(root, text="Include Special Chars", variable=special_var).grid(row=3, column=0, sticky='w')

tk.Button(root, text="Generate Passwords", command=generate).grid(row=4, column=0, pady=10)
tk.Button(root, text="Save to File", command=save_passwords).grid(row=4, column=1)
tk.Button(root, text="Copy Selected", command=copy_password).grid(row=5, column=0, columnspan=2)

results = tk.Text(root, height=10, width=50)
results.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
