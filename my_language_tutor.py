import random
import pandas as pd
import os

# source path

source_path = input("Path of your dictionary file: ")
assert os.path.exists(source_path), f"The path: {source_path} doesn't exist :((("

file_name = input("Name of the file: ")
source_path_file_name = (f"{source_path}/{file_name}")
assert os.path.isfile(source_path_file_name), f"The file: {source_path_file_name} doesn't exist :((("

# loading dictionary file from Excel
df = pd.read_excel(source_path_file_name, sheet_name=0) # note: "r" sign is needed

dictionary_english = list(df['english'])
dictionary_native = list(df['hungarian'])

# eng
question_en = random.choice(dictionary_english)
question_pos_en = dictionary_english.index(question_en)

# native
question_native = random.choice(dictionary_native)
question_pos_hu = dictionary_native.index(question_native)

print("*"*38," My English Tutor ","*"*38)
print(" ")
result = input("Which version do you want to play? English to native press: 'a' or native to English press:' 'b'\n ")

# ENG ---> NATIVE
if result == "a":

    while True:
            answer_native = input(f"Please translate the floowing word:\n {question_en}  --->  ").lower()
            if answer_native not in dictionary_native:
                    print("Sorry. Wrong aswer! Press enter and try again. :(")
                    input()
                    continue
            if question_pos_en == dictionary_native.index(answer_native):
                    print("Your answer is correct!:)")
                    result = input("Do you want to continue? (y/n)").lower()
                    if result == "y":
                            question_en = random.choice(dictionary_english)
                            question_pos_en= dictionary_english.index(question_en)
                    else:
                            exit()
            else:
                    print("Sorry. Wrong aswer! Press enter and try again. :(")
                    input()
# NATIVE ---> ENG

if result == "b":

    while True:
            answer_eng = input(f"Please translate the floowing word:\n {question_native}  --->  ").lower()
            if answer_eng not in dictionary_english:
                    print("Sorry. Wrong aswer! Press enter and try again. :(")
                    input()
                    continue
            if question_pos_hu == dictionary_english.index(answer_eng):
                    print("Your answer is correct!:)")
                    result = input("Do you want to continue? (y/n)").lower()
                    if result == "y":
                            question_native = random.choice(dictionary_native)
                            question_pos_hu= dictionary_native.index(question_native)
                    else:
                            exit()
            else:
                    print("Sorry. Wrong aswer! Press enter and try again. :(")
                    input()
