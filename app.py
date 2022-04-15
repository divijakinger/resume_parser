import pickle
from pydoc import synopsis
from resume_parser_final import *
from flask import Flask, render_template, request, url_for, redirect
import pymongo
from flask_ngrok import run_with_ngrok
from flask_cors import CORS
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

conn = pymongo.MongoClient("mongodb+srv://root:root@deepblue.mcahp.mongodb.net/test")


app = Flask(__name__)
CORS(app)
run_with_ngrok(app)


db = conn.test
resume = db.Testing1


@app.route("/")
def index():
    return "Welcome to API homepage"


resume_id = 0

@app.route("/add", methods=["GET", "POST"])
def add_todo():
    try:
        resume.drop()
    except:
        pass
    data = request.json
    urls = data["urls"]
    for url in urls:
        r = requests.get(
            url,
            stream=True,
        )
        url = url.split("?")
        ext = url[0].split(".")[-1]
        with open(
            "%s.%s" % ("resume", ext), "wb"
        ) as f:  # open the file to write as binary - replace 'wb' with 'w' for text files
            for chunk in r.iter_content(1024):  # iterate on stream using 1KB packets
                f.write(chunk)  # write the file
        global resume_id
        resume_data = read(os.getcwd()+"\\resume."+ext)
        name = extract_name(resume_data)
        email = extract_email(resume_data)
        mobile = extract_mobile_number(resume_data)
        skills = extract_skills(resume_data)
        # skills=['Autocad','Ms office','Powerpoint','Word','C++']
        education=extract_education(resume_data)
        job_strings,job_list=extract_job_context(resume_data)
        job_data=extract_all(job_strings,job_list,resume_data)
        # if len(job_data)==0:
        #     company_strings,company_list=extract_company_context(resume_data)
        #     job_data=extract_all_companies_version(company_strings,company_list)
        cert_degree=get_degree_2(resume_data)
        education=get_all_educations(resume_data)
        college=get_college_2(resume_data)
        urls=get_url(resume_data)
        languages=extract_languages(resume_data)
        location=sentence_extractor(resume_data)
        try:
            company=[i[1] for i in job_data]
        except:
            company=''
        synopsis="Your Candidate {0} is a potential job candidate for your company with a qualification of {1} from {2} University. The candidate is well versed with the following skills: {3}. Here are the contact details :- Phone : {4} and Email : {5}".format(name,(', '.join(cert_degree)),(', '.join(list(set(college)))),(' ,'.join(skills)),mobile,email)
        resume.insert_one(
            {
                "Resume ID": resume_id,
                "Name": name,
                "Email": email,
                "Phone": mobile,
                "Education": list(set(education)),
                "College":list(set(college)),
                "Degree":cert_degree,
                "Skills": skills,
                "Job_data": job_data,
                "Resume_data":resume_data,
                "Urls":urls,
                'Languages':languages,
                "Synopsis":synopsis,
                'Location':location
            }
        )
        resume_id += 1
        os.remove("resume."+ext)
    return "Data parsed"


@app.route("/getData", methods=["GET"])
def getdata():
    final = []
    data = resume.find()
    for d in data:
        try:
            del d["_id"]
        except:
            continue
        final.append(d)
    return {"data": final}

# @app.route("/insertskills",methods=["POST"])
# def insert_skills():
#     str_list = request.json
#     str_list = str_list["skills"]
#     for data in resume.find():
#         temp=data.copy()
#         data['inserted_skills']=str_list
#         resume.replace_one(temp,data)
    

@app.route("/matching", methods=["POST"])
def matching_resume():
    final = []
    str_list = request.json
    str_list = str_list["skills"]
    data = resume.find()
    for d in data:
        temp=d.copy()
        percentage_match = matching(str_list, d["Skills"])
        final.append(percentage_match)
        d['match_percentage']=percentage_match
        resume.replace_one(temp,d)
    return {"Percentage": final}

@app.route('/metrics',methods=["POST"])
def metrics():
    final=[]
    data=request.json
    job_desc=data['job_desc']
    data = resume.find()
    top,mid,low=0,0,0
    best_100=0
    for d in data:
        temp=d.copy()
        resume_text=d["Resume_data"]
        content = [job_desc, resume_text]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(content)
        mat = cosine_similarity(count_matrix)
        percentage=round(mat[1][0]*100)
        if percentage<40:
            low+=1
        elif percentage>=40 and percentage<70:
            mid+=1
        else:
            top+=1
            if percentage==100:
                best_100+=1
        final.append(percentage)
        d['match_percentage']=percentage
        resume.replace_one(temp,d)
    return {"Metrics":final,'percentage_table':[low,mid,top],'best_count':best_100}

@app.route('/sortbymatch',methods=['GET'])
def sort_by():
    final=[]
    data=resume.find().sort('match_percentage',-1)
    for d in data:
        try:
            del d["_id"]
        except:
            continue
        final.append(d)
    return {"data": final}

@app.route('/bestmatch',methods=['GET'])
def best_match():
    final=[]
    data=resume.find().sort('match_percentage',-1)
    for d in data:
        try:
            del d["_id"]
        except:
            continue
        final.append(d)
        break
    return {"data": final}

@app.route('/topfive',methods=['GET'])
def top_five():
    final=[]
    data=resume.find().sort('match_percentage',-1)
    count=0
    for d in data:
        if count==5:
            break
        try:
            del d["_id"]
        except:
            continue
        final.append(d)
        count+=1
    return {"data": final}

# Skill filtering API

@app.route('/skillfilter',methods=["POST"])
def skill_filter():
    inp=request.json
    skills_given=inp['skills_given']
    final=[]
    data=resume.find( { 'Skills': { '$all': skills_given } } )
    for d in data:
        try:
            del d["_id"]
        except:
            continue
        final.append(d)
    return {'data':final}

@app.route('/analytics',methods=["GET"])
def analytics():
    low,mid,top,highest_percentage=0,0,0,0
    data=resume.find()
    temp_dicts=[]
    for d in data:
        percentage=d['match_percentage']
        if highest_percentage<percentage:
            highest_percentage=percentage
        skills=d['Skills']
        temp_dicts.append(Counter(skills))
        try:
            del d["_id"]
        except:
            continue
        if percentage<40:
            low+=1
        elif percentage>=40 and percentage<70:
            mid+=1
        else:
            top+=1
    final=Counter({})
    for t in temp_dicts:
        final+=t
    final=dict(final)
    sorted_final = sorted(final.items(), key=lambda x: x[1], reverse=True)
    sorted_skills=[i[0] for i in sorted_final]
    try:
        sorted_skills=sorted_skills[:5]
    except:
        pass
    return {'percentage_table':[low,mid,top],'highest_percentage':highest_percentage,'top_skills':sorted_skills}


if "__name__" == "__main__":
    app.run(debug=True)
