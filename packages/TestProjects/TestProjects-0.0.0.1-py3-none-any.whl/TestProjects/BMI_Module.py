def calc_bmi(height = 173, weight=62.9):
    height = height * 0.01
    weight = weight
    bmi = weight / height ** 2
    print("BMI:", bmi)

calc_bmi(height = 173, weight = 62.9)