def cal_BMI(kg,height):
    BMI = kg/((height*0.01)**2)
    return BMI

def classify_BMI(kg,height):
    BMI=cal_BMI(kg,height)
    state_fat = ''
    if BMI <=18.5:
        state_fat = "저체중"
    elif 18.5<=BMI<=22.9:
        state_fat = "정상"
    elif 23 <=BMI <=24.9:
        state_fat = "과체중"
    else :
        state_fat = "비만"
    return BMI, state_fat

def input_BMI():
    height = float(input("키(cm) 입력 : "))
    kg = float(input("몸무게(kg) 입력 : "))
    BMI_tuple = classify_BMI(kg, height)
    print("MY BMI : {0:.2f}\n나의 BMI(신체질량지수)는 {0:.2f}이고, {1}입니다.".format(
        BMI_tuple[0], BMI_tuple[1]
    ))