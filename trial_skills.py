from encodings import utf_8
from numpy import unicode_
import requests
import json

url = "https://emsiservices.com/skills/versions/latest/extract"

payload = "{ \"text\": \"... Jay Madhavi Navi Mumbai, Maharashtra - Email me on Indeed: indeed.com/r/Jay- Madhavi/1e7d0305af766bf6  I look forward to being associated with a growth - oriented, learning firm and contribute my skills for its success. This will allow me to grow both professionally as well as an individually.  WORK EXPERIENCE  NIIT -  2016 to 2016  B+ Average Advanced  SQL Oracle -  2016 to 2016  B+ Average  MSCIT -  2011 to 2011  A Completed Technical Institution  Projects undertaken (BE):  S.N. Project Title Name of company/college Nature of the Remarks project  1 Android Based Saraswati College Of Android Completed Employee Tracker Engineering Application System  2 An innovative Saraswati College Of Compilation Completed approach for Engineering code optimization  3 Simple Website Saraswati College Of Website related to Completed Related to Engineering information of Classical Italian cars Cars  About Myself:   I am Capable and Hardworking, and can adapt to New Surroundings.  https://www.indeed.com/r/Jay-Madhavi/1e7d0305af766bf6?isid=rex-download&ikw=download-top&co=IN https://www.indeed.com/r/Jay-Madhavi/1e7d0305af766bf6?isid=rex-download&ikw=download-top&co=IN     I Can Face Challenges with confidence and would give my best shot under Stressful situations.  .. 03 : 03:  EDUCATION  BE (Computer Science) in Computer Science  Saraswati College Of Engineering, Kharghar -  Mumbai, Maharashtra  2014 to 2017  HSC in Computer science  Acharya College Chembur -  Mumbai, Maharashtra  2011 to 2013  SSC  State Board  2011  ADDITIONAL INFORMATION    Ability to accept responsibilities and give best performance to complete the given work efficiently.   To take up challenging jobs & work as a team.   To positively accept my Mistake. ...\", \"confidenceThreshold\": 0.6 }"
headers = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjNDNjZCRjIzMjBGNkY4RDQ2QzJERDhCMjI0MEVGMTFENTZEQkY3MUYiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJQR2FfSXlEMi1OUnNMZGl5SkE3eEhWYmI5eDgifQ.eyJuYmYiOjE2NDYzMjcyNjYsImV4cCI6MTY0NjMzMDg2NiwiaXNzIjoiaHR0cHM6Ly9hdXRoLmVtc2ljbG91ZC5jb20iLCJhdWQiOlsiZW1zaV9vcGVuIiwiaHR0cHM6Ly9hdXRoLmVtc2ljbG91ZC5jb20vcmVzb3VyY2VzIl0sImNsaWVudF9pZCI6IjN2anIzNDhla2RreXU2czciLCJlbWFpbCI6ImRpdmlqYS5raW5nZXJAc29tYWl5YS5lZHUiLCJjb21wYW55IjoiU29tYWl5YSBUcnVzdCIsIm5hbWUiOiJEaXZpamEgS2luZ2VyIiwiaWF0IjoxNjQ2MzI3MjY2LCJzY29wZSI6WyJlbXNpX29wZW4iXX0.CjhGJeRGOg-w7C4rtOpUhSAUprhS5WyIGwy-aBfm_pIT8x0rjBQN5oaEyVFz931aauwQRWaD7D0gEgZ4_FjKhdGkBbsHXW2qrf5Ai7jMZeiXguXzSvwC3uze-D_sebI4OqX0Q-2HwuxjHYdjCD_uTWneKc9bBhGMHZhpgvkHYVs3-_aWQ5N-YCgCSrkjzLeuli2JjphidHoeg-1aCh8QtqF2ClIUUsaNkEbKZF2XCScNaQFEn4VBMtl90jI_zMWztl78aylClX3K9eQGaycqaInVEaCruyLCQAZey-Boi6zi08ygny_cpdmGBzxVAfRqh9__b5A-fdWmBgDgw7P-4Q",
    'Content-Type': "application/json"
    }

response = requests.request("POST", url, data=payload.encode("utf-8"), headers=headers)

print(type(response.json()))

# json_data = json.loads(response.text)

# print(json_data)

d = dict(response.json())

temp= d['data']
skills=[]

for t in temp:
    skills.append(t['skill']['name'])

print(skills)