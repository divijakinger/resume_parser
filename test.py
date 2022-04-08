import pymongo

conn = pymongo.MongoClient("mongodb+srv://root:root@deepblue.mcahp.mongodb.net/test")

db = conn.test
resume = db.Testing1

for data in resume.find():
    temp=data.copy()
    data['inserted_skills']=['This','is','testing']
    resume.replace_one(temp,data)