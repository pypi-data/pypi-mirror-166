class BMI:
    def __init__(self, height, weight):
        self.height = height/100
        self.weight = weight
        self.bmi = self.weight / self.height**2

    def calc(self):
        return f"{self.bmi:.2f}"

    def grade(self):
        if self.bmi <= 18.5:
            return "저체중"
        elif 18.5 < self.bmi <= 22.9:
            return "정상"
        elif 22.9 < self.bmi <= 24.9:
            return "과체중"
        else:
            return "비만"
