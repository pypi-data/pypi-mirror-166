def test_bmi(length, weight):
    bmi = weight / ((length/100)**2)
    if bmi <18.5:
        print('MY BMI: %.1f'% (bmi))
        print('나의BMI(신체질량지수)는 %.1f이고, 저체중입니다'%(bmi))

    elif (bmi >= 18.5) & (bmi <23):
        print('MY BMI: %.1f'% (bmi))
        print('나의BMI(신체질량지수)는 %.1f이고, 정상입니다'%(bmi))

    elif (bmi >= 23) & (bmi < 25):
        print('MY BMI: %.1f'% (bmi))
        print('나의BMI(신체질량지수)는 %.1f이고, 과체중입니다'%(bmi))

    else:
        print('MY BMI: %.1f'% (bmi))
        print('나의BMI(신체질량지수)는 %.1f이고, 비만입니다'%(bmi))