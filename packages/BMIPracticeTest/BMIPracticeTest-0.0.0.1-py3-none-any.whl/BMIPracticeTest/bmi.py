def calculate_bmi():
    name = input('이름을 입력하세요: ')
    height = input('키를 입력하세요: ')
    weight = input('몸무게를 입력하세요: ')

    height = float(height)
    weight = float(weight)

    height = height/100
    bmi = weight/(height*height)

    if bmi <= 18.5:
        print('{0}님의 BMI는 {1:.2f}(저체중)입니다.'.format(name, bmi))
    elif (bmi >= 18.5) and (bmi <= 22.9):
        print('{0}님의 BMI는 {1:.2f}(정상)입니다.'.format(name, bmi))
    elif (bmi >= 23.0) and (bmi <= 24.9):
        print('{0}님의 BMI는 {1:.2f}(과체중)입니다.'.format(name, bmi))
    elif bmi >= 25.0:
        print('{0}님의 BMI는 {1:.2f}(비만)입니다.'.format(name, bmi))
    else:
        print('다시 입력해 주세요')