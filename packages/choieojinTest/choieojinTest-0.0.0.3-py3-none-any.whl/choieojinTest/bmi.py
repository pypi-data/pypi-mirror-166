def calculate(height, weight):
    weight = weight
    height = float(height / 100)
    bmi = round(weight / (height * height), 1)

    if bmi <= 18.5:
        print("MY BMI: ", bmi, "\n나의BMI(신체질량지수)는", bmi, "이고, 저체중입니다.")
    elif bmi <= 22.9:
        print("MY BMI: ", bmi, "\n나의BMI(신체질량지수)는", bmi, "이고, 정상입니다.")
    elif bmi <= 24.9:
        print("MY BMI: ", bmi, "\n나의BMI(신체질량지수)는", bmi, "이고, 과체중입니다.")
    else:
        print("MY BMI: ", bmi, "\n나의BMI(신체질량지수)는", bmi, "이고, 비만입니다.")