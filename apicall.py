import requests
import time


edamam_response = requests.get("https://api.edamam.com/search?app_id=6e3a1c55&app_key=979f4ea3d3c1014ffa5de338accf640b")
print(edamam_response)      # 200 – OK. The request was successful.
url = 'https://api.edamam.com/search?'
edamam_id = 'app_id=6e3a1c55'
edamam_key = 'app_key=979f4ea3d3c1014ffa5de338accf640b'
q = 'q='
health = 'health='

allergy_dict = {'peanut': 'peanut-free', 'peanuts': 'peanut-free', 'tree nut': 'tree-nut-free',
                'dairy': 'dairy-free', 'milk' : 'dairy-free', 'alcohol': 'alcohol-free',
                'celery' : 'celery-free', 'eggs' : 'egg-free', 'fish' : 'fish-free',
                'gluten' : 'gluten-free', 'mustard' : 'mustard-free', 'pork' : 'pork-free',
                'sesame' : 'sesame-free', 'shellfish' : 'shellfish-free', 'soy' : 'soy-free',
                'tree nuts' : 'tree-nut-free', 'wheat' : 'wheat-free'}

print("Welcome to the Allergy App!")

print("What would you like to cook?")
q_input = input()
print("What is your food allergy?")
health_input = input()

health_arg = ""
allergen_found = False
for key,val in allergy_dict.items():
    if(health_input == key):
        health_arg = val
        allergen_found = True

link = ""
if allergen_found:
    link = url + q + q_input + "&" + edamam_id + "&" + edamam_key + "&" + q + q_input + "&" + health + health_arg
else:
    link = url + q + q_input + "&" + edamam_id + "&" + edamam_key + "&" + q + q_input + "&" + "excluded" + "=" + health_input

print(link)
print(requests.get(link).json())