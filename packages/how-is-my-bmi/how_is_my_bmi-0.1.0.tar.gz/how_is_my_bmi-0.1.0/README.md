how_is_my_bmi

A small library to be able to generate your BMI Index - Body Mass Index.

Installation

pip install bmi

Get Started

How to get the BMI Index:

from bmi import Bmi

### Instantiate the BMI Object
user_2 = Bmi(105, 6)

### Call the BMI Calculator method
print(user_2.calc_bmi())