name= input('당신의 이름을 입력해주세요 : ')
height = float(input('당신의 키를 입력해주세요 : '))
weight = float(input('당신의 몸무게를 입력해주세요 : '))

height = height * 0.01
bmi = weight/(height*height)

print("MY BMI : {:.2f} ".format(bmi))

if bmi < 18.5:
    print("{} 님의 BMI(신체질량지수)는 {:.2f}이고 저체중 입니다".format(name,bmi))
elif 18.5 <= bmi <23:
    print("{} 님의 BMI(신체질량지수)는 {:.2f}이고 정상 입니다".format(name,bmi))
elif 23<= bmi <25:
    print("{} 님의 BMI(신체질량지수)는 {:.2f}이고 과체중 입니다".format(name,bmi))
elif 25<= bmi <30:
    print("{} 님의 BMI(신체질량지수)는 {:.2f}이고 경도비만 입니다".format(name,bmi))
else:
    print("{} 님의 BMI(신체질량지수)는 {:.2f}이고 중증도비만 입니다".format(name,bmi))