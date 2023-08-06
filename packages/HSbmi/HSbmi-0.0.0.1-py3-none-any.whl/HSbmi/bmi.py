def bmi_cal(height, weight):
    '''BMI를 계산하고 비만도를 측정합니다.
    height : 키 (cm)
    weight : 몸무게 (kg)
    '''

    bmi = weight / ((height/100)**2)
    bmi = round(bmi,1)
    msg = ''
    if bmi <= 18.5:
        msg = '저체중'
    elif bmi < 23:
        msg = '정상'
    elif bmi < 25:
        msg = '과체중'
    else:
        msg = '비만'

    print('MY BMI:{}'.format(bmi))
    print('나의BMI(신체질량지수)는 {}이고, {}입니다.'.format(bmi, msg))

