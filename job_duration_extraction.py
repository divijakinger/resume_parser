s="CURRICULUM VITAE    B.MOHAMED SABEEK    39-A, Muslim West Street,    Natham-624401                              Mobile: +91-9943856262    Dindigul District    Email: sabeek.93@rediffmail.com    CARRIER OBJECTIVE:    To learn and function effectively in an organization and be able to deliver to the     bottom-line and to upgrade my knowledge and skills and make a difference in whatever I do.    ACADEMIC CHRONICLES:     B.E - ELECTRICAL AND ELECTRONICS ENGINEERING WITH 66% IN APRIL - 2015.    \uf0b7 S.B.M College of Engineering and Technology \u2013 Dindigul.     DIPLOMA IN ELECTRICAL AND ELECTRONICS ENGINEERING WITH 78% IN APRIL - 2012.    \uf0b7 N.P.R College of Engineering and Technology \u2013 Natham.     X \u2013 STANDARD STATE BOARD EXAMINATION IN APRIL - 2009.    \uf0b7 Sarva Seva higher secondary school \u2013 Natham.          Worked was an Electrical Site Engineer and load estimator in DNR Electrical     Working as an Electrical Site Engineer (Erection, Commissioning & Procurement) on     Industrial and Commercial Projects in HARI Engineering \u2018A\u2019 Grade Electrical Contractor in     PROFESSIONAL EXPERIENCE:    From May 2015 to July 2016:-    Consultancy Trichy.      From August 2016 to Till Date:-    Madurai.     NATURE OF JOB INVOLVED:    LBS and RTCC panels.    \uf0b7 Erection and Commissioning of EB pole structures, RMU & FRTU unit, VCB panel,    \uf0b7 Erection, Testing and Commissioning of Transformers both Oil type and Dry type as well    as Bus duct Erections both Sandwich and Air insulated type, Cable trays and Earth bits.    \uf0b7 Executing Electrification based on the design, Monitoring subordinates works, Maintain    records and Man power Management.    \uf0b7 All Type of panel boards like MV Panel, MCC, MPCC, SSB, MLSB, APFC, VFD and    Harmonic filter panels Testing, Erection and Commissioning.    TECHNICAL SKILLS:    \uf0b7 Project Execution, planning and implementation at all stages.    \uf0b7 Preparation of Electrical Load Calculations and Single line diagram.    \uf0b7 Studying and execution as per electrical designs layout.    \uf0b7 Selections of cables, bus bars and switch gears ratings based on the load.    \uf0b7 Basic CADD, MS \u2013 Office, Selection of Light Fixtures based on LUX level.    Project Title: Design of matrix converter based UPFC for grid integration of     \uf0b7 Preparation of BOQ\u2019s & Tender Documents.    \uf0b7 Prepare daily progress reports and Checking RA bills.    \uf0b7 Co-Ordination with Client and Consultants.    Basic Knowledge About:    \uf0b7 HVAC    \u2013 Chiller, VRF and AHU.    \uf0b7 CCTV     \u2013 DVR and NVR.    \uf0b7 Fire Protection \u2013 Conventional & Addressable.    \uf0b7 Building Management Systems.    Engineering Project:    renewable energy source.    Personal Data:    Objective:  Voltage Regulation.    Name     : B. Mohamed Sabeek     Date of Birth     : 10/12/1993    Father\u2019s name     : S.K. Basheer    Languages Known     : English, Tamil    Passport Number     : P5468130     : Indian     : Playing chess and surfing internets.    Nationality    Hobbies    Declaration:    knowledge.    DATE   :    PLACE :                                  I hereby declare that the information furnished above is true to the best of my    NAME    (B.MOHAMED SABEEK)    "

main=s.split('.')
print(main)

# 3 types ka duration format hai
# 1) Year to year (2018-2019)
#    - Month, Year to Month, Year
# 2) Year to present (2019-Present)
# 3) X years Y months (5 years 4 months)

# Need to work on Present wala key word

import re
ans = []
def find_con(n, s):
    result = re.findall('\d{%s}'%n, s)
    return result

temp=[]
final=['Developer','Software Engineer','Analyst']     # Example titles until now baadme aur add karenge
for t in main:
    for f in final:
        if f.lower() in t.lower():
            temp.append(t)

print(temp)
print(len(temp))
years=[]
for t in temp:
    l=find_con(4, t)
    for i in l:
        years.append(i)

final=[]
for year in years:
    if 1900<int(year)<=2022:
        final.append(year)


print(final)






# --- Waste ---

# for i in temp:
#     temp_years=find_con(4, i)
#     for y in temp_years:
#         try:
#             final.remove(y)
#         except:
#             pass

# print(final)