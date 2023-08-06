class Bmi:
    def __init__(self, weight, height):
        self.weight = weight
        self.height = height

    def calculate_bmi(self):
        CONVERSION = 30.48
        return round(self.weight / ((self.height*CONVERSION)/100)**2, 2)
