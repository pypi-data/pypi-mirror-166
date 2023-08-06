def cal_bmi():
    h = int(input('키: '))
    w = int(input('몸무게: '))
    bmi = round(w/(h**2)*10000,1)

    print(f"MY BMI: {bmi}")
    if bmi<=18.5:
        print(f"나의 BMI(신체질량지수)는 {bmi}이고, 저체중입니다.")
    elif 18.5<bmi<=22.9:
        print(f"나의 BMI(신체질량지수)는 {bmi}이고, 정상입니다.")
    elif 23<bmi<24.9:
        print(f"나의 BMI(신체질량지수)는 {bmi}이고, 과체중입니다.")
    else:
        print(f"나의 BMI(신체질량지수)는 {bmi}이고, 비만입니다.")
# print(bmi)
#cal_bmi()