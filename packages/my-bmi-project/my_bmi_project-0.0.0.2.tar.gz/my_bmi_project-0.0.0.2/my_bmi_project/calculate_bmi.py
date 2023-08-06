def calculate_bmi(centimeter, kilogram) :
    height = centimeter * 0.01
    weight = kilogram
    return weight / (height * height)

def calcuate_bmi_with_grade(centimeter, kilogram) :
    bmi = calculate_bmi(centimeter, kilogram)

    result = ''
    if bmi < 18.5 :
        result = "저체중"
    elif bmi < 23 :
        result = "정상"
    elif bmi < 25 :
        result = "과체중"
    elif bmi < 30 :
        result = "경도비만"
    else :
        result = "중등도비만"

    return result