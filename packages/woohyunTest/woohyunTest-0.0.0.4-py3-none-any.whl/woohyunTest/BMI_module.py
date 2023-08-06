def BMI_evaluate():
    weight = input("체중: ")
    height = input("신장: ")

    weight = float(weight)
    height = float(height)

    height = height/100
    bmi = weight / (height*height)

    print(f'My BMI: {bmi}')
    if bmi <18.5:
        print("저체중")
    elif bmi>18.5 and bmi<23:
        print("정상")
    elif bmi>23 and bmi<25:
        print("과체중")
    elif bmi>25 and bmi<30:
        print("경도비만")
    else:
        print("중등도비만")