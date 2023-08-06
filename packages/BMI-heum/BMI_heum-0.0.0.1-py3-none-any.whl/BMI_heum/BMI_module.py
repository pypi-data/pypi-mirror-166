def printBMI(weight, height):
    '''BMI지수 측정해준다.
    18.5이하이면 저체중 / 18.5~22.9 사이면 정상 / 23.0~24.9 사이면 과체중 / 25.0이상부터는 비만으로 판정'''
    height_m = height/100
    BMI = weight / (height_m**2)
    if BMI < 18.5:
        measure = '저체중'
    elif 18.5<= BMI <=22.9:
        measure = '정상'
    elif 23.0<= BMI <=24.9:
        measure = '과체중'
    else:
        measure = '비만'
    print('''MY BMI: {}
    나의 BMI(신체질량지수)는 {}이고, {}입니다.'''.format(BMI,BMI,measure))
