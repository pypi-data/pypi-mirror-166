def check_bmi(weight, height):
    height = height / 100
    bmi = weight / (height * height)
    my_bmi = " "
    if bmi < 18.5:
        my_bmi = '저체중'
    elif bmi < 23.0:
        my_bmi = '정상'
    elif bmi < 24.9:
        my_bmi = '과체중'
    else:
        my_bmi = '비만'
    print("MY BMI: ", round(bmi, 1))

    print('나의 BMI(신체질량지수)는 {:.1f} 이고, {} 입니다.'.format(bmi, my_bmi))