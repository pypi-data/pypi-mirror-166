print('체질량 지수 BMI를 계산합니다~\n')

name = input('당신의 이름을 입력하세요: ')
weight = input('몸무게를 입력하세요: ') # 결과는 항상 문자열이다
height = input('키를 입력하세요: ')
print(type(weight), type(height)) # 둘 다 str 타입이다

weight = float(weight)
height = float(height)
print(type(weight), type(height)) # float로 바뀌었다

height = height / 100 # bmi 계산을 위한 단위 조정
bmi = weight / (height*height) # 또는 weight / (height**2)

comment = '\n%s님의 bmi는 %d/(%.2f*%.2f)이므로 %.3f입니다.'
print(comment % (name, weight, height, height, bmi))