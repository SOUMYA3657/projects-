def calculate_bmi(weight, height_cm):
    """Calculate the Body Mass Index (BMI)."""
    height_m = height_cm / 100  # Convert cm to meters
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def classify_bmi(bmi):
    """Classify the BMI based on WHO standards."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def get_positive_float(prompt):
    """Prompt the user until a valid positive float is entered."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_age():
    """Prompt the user to enter a valid age."""
    while True:
        try:
            age = int(input("Age: "))
            if age <= 0:
                print("Please enter a valid positive age.")
            else:
                return age
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def get_gender():
    """Prompt the user to select a gender."""
    while True:
        gender = input("Gender (M/F/Other): ").strip().lower()
        if gender in ['m', 'f', 'other']:
            return gender.capitalize()
        else:
            print("Invalid input. Please enter M, F, or Other.")

def main():
    print("           ==== BMI Calculator ====")
    print("\nEnter your personal details and body measurements:\n")

    age = get_age()
    gender = get_gender()
    height_cm = get_positive_float("Height (cm): ")
    weight = get_positive_float("Weight (kg): ")

    bmi = calculate_bmi(weight, height_cm)
    category = classify_bmi(bmi)

    print("\n--- Your BMI Report ---")
    print(f"Age: {age} years")
    print(f"Gender: {gender}")
    print(f"Height: {height_cm} cm")
    print(f"Weight: {weight} kg")
    print(f"BMI: {bmi}")
    print(f"BMI Category: {category}")

    print("\n--- BMI Classification (WHO) ---")
    print("Underweight: < 18.5")
    print("Normal weight: 18.5 – 24.9")
    print("Overweight: 25 – 29.9")
    print("Obesity: 30 or more")

if __name__ == "__main__":
    main()
