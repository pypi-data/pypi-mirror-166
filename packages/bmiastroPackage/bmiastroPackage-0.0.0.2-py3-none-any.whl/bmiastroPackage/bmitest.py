def cal_bmi(tall, weight):
	bmi = round(weight / (tall*tall), 1)
	if bmi <= 18.5:
		metric = '저체중'
	elif bmi > 18.5 and bmi <= 22.9:
		metric = '정상'
	elif bmi > 22.9 and bmi <= 24.9:
		metric = '과체중'
	elif bmi > 24.9:
		metric = '비만'
	else:
		metric = '키의 단위는 m, 몸무게의 단위는 kg 입니다.'
	
	print(f'My BMI: {bmi}')
	print(f"나의 BMI(신체질량지수)는 {bmi}이고, {metric}입니다.")

def celeb_versionup():
	print('good feeling. succeed versionup!!')
