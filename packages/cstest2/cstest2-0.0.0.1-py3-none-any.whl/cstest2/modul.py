def bmi(a, b):
    a = int(a) / 100
    b = int(b)
    c = b/(a**2)
    d = []

    if c <= 18.5:
        d.append('저체중')
    elif c <= 24.9:
        d.append('정상')
    else:
        d.append('과체중')
    print(f'MY BMI : {c:.1f}')
    print(f'나의 BMI(신체질량지수)는 {c:.1f}이고, {d[0]}입니다.')



