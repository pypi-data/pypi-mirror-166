import BMI_cal

bmi = BMI_cal.BMIC(int(input('키 (cm): ')), int(input('몸무계 (kg): ')))

print(f'MY BMI: {bmi:.2f}')

if bmi <= 18.5:
    print('저체중입니다.')
elif bmi <= 22.9:
    print('정상입니다.')
elif bmi <= 24.9:
    print('과체중입니다.')
else:
    print('비만입니다.')