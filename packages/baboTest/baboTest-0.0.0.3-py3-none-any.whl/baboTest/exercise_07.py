def calcul(weight,height):
    height = float(height/100)
    value = round(float(weight/(height *height)),1)
    return value

def cpwndrngkrl(value):
    if value <= 18.5:
        print('MY BMI {}'.format(value))
        print('나의 BMI(신체질량지수)는 {}이고 저체중입니다.'.format(value))
    elif value <= 22.9:
        print('MY BMI {}'.format(value))
        print('나의 BMI(신체질량지수)는 {}이고 정상입니다.'.format(value))
    elif value <= 24.9:
        print('MY BMI {}'.format(value))
        print('나의 BMI(신체질량지수)는 {}이고 과체중입니다.'.format(value))
    else:
        print('MY BMI {}'.format(value))
        print('나의 BMI(신체질량지수)는 {}이고 비만입니다.'.format(value))
