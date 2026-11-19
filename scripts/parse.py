import re, json, sys
T=open(sys.argv[1]).read()
T=re.sub(r'Dr S Satyanarayana Ph\.D\., PDF\(AI\), FARSC \d+\nENTERPRISE AI PRODUCT DEVELOPMENT CURRICULUM Industry-Aligned Syllabus\n','',T)
T=T.replace('A WS','AWS').replace('T ypeScript','TypeScript').replace('SW AYAM','SWAYAM').replace('T wo','Two')
starts=[m.start() for m in re.finditer(r'^COURSE \d+ \| EAI-1\d\d$',T,re.M)]
end=T.index('Course-to-Career Alignment Matrix: Core AI Track')
starts.append(end)
def join(s):
    s=re.sub(r'(\w)-\n(\w)',r'\1\2',s)
    return re.sub(r'\s*\n\s*',' ',s).strip()
courses=[]
for a,b in zip(starts,starts[1:]):
    c=T[a:b]; L=c.split('\n')
    num=int(re.match(r'COURSE (\d+)',L[0]).group(1)); code=L[0].split('| ')[1]
    title=L[1].strip(); tag=L[2].strip()
    pb=re.search(r'Prerequisites (.*?)Core Competencies',c,re.S).group(1)
    pb=re.sub(r'-\n','',pb)
    pre=re.search(r'(.*?)\s*Contact Hours (\d+ L \+ \d+ P)\s*(.*)',pb,re.S)
    prereq=join(pre.group(1)+' '+pre.group(3)) if pre else join(pb)
    hrs=pre.group(2) if pre else '45 L + 30 P'
    comp=re.search(r'Core Competencies\n(.*?)Five-Unit Curriculum',c,re.S).group(1)
    comps=[join(x) for x in comp.split('▶') if x.strip()]
    units=[]
    for m in re.finditer(r'UNIT (I|II|III|IV|V) (.*?) (\d+) Hours\n(.*?)Hands-on Outcome: (.*?)(?=\nUNIT |\nIndustry Tools)',c,re.S):
        units.append(dict(n=m.group(1),title=m.group(2).strip(),hours=int(m.group(3)),topics=join(m.group(4)),outcome=join(m.group(5))))
    tools=[]
    tb=re.search(r'Industry Tools & Platforms\n(.*?)Hands-on Laboratory',c,re.S).group(1)
    labs=re.search(r'Hands-on Laboratory \(30 Hours\)\n(.*?)Course Outcomes',c,re.S).group(1)
    labitems={}
    for m in re.finditer(r'L(\d) (.*?)(?= L\d |\nL\d |$)',join(labs)):
        labitems[int(m.group(1))]=m.group(2).strip()
    labl=[labitems[k] for k in sorted(labitems)]
    cos=[]
    for m in re.finditer(r'^(CO\d) (.*?) (L\d) (Remember|Understand|Apply|Analyse|Evaluate|Create)$',re.sub(r'\n(?!CO\d )',' ',re.search(r'Course Outcomes\n(.*?)Enterprise Capstone',c,re.S).group(1)).strip()+'\n',re.M):
        cos.append(dict(co=m.group(1),text=m.group(2),bloom=m.group(3)+' '+m.group(4)))
    cap=join(re.search(r'Enterprise Capstone Product\n(.*?)Aligned Careers',c,re.S).group(1))
    capname,capdesc=cap.split(':',1) if ':' in cap else ('Capstone',cap)
    car=join(re.search(r'Aligned Careers\n(.*?)\nTop 3 Programming',c,re.S).group(1))
    langs=re.findall(r'^#(\d) (\S+(?: / \S+)?|C\+\+ / CUDA|OpenQASM 3)',c,re.M)
    certs=re.search(r'Recommended Industry Certifications\nCertification Issuer Level Units\n(.*?)Text & Reference',c,re.S).group(1)
    cj=join(certs)
    LV=r'(Project-based|Course badge|Assoc\./Prof\.|Core / Intermediate|Foundational|Associate|Professional|Academic|Course certificate|Specialty|Expert|Intermediate|Practitioner|Advanced|Fundamentals|Entry|Beginner)'
    segs=re.findall(r'(.*?)\s+'+LV+r'\s+([IVX]+(?:\s*[–,-]\s*[IVX]+)*)\s*',cj)
    ISS=["IIT faculty, Govt. of India","DeepLearning.AI (Coursera)","Univ. of Alberta (Coursera)","Northwestern Univ. (Coursera)","Univ. of Toronto (Coursera)","HarvardX (edX)","Snowflake / Confluent","PECB, BSI and others","GIAC / SANS","Linux Foundation","Google Cloud","NVIDIA DLI","IBM Quantum","Hugging Face","OpenCV .org","Databricks","Microsoft","CompTIA","NVIDIA","ISACA","IAPP","AWS","IBM"]
    certnames=[]
    for raw,lv,u in segs:
        raw=raw.strip(); iss=''
        for i in ISS:
            if raw.endswith(i): iss=i.replace('OpenCV .org','OpenCV.org'); raw=raw[:-len(i)].strip(); break
        certnames.append(dict(name=raw.replace('(RLH- F/DPO) ',''),issuer=iss,level=lv.replace('Core / Intermediate','Intermediate'),units=u))
    courses.append(dict(num=num,code=code,title=title,tagline=tag,prereq=prereq,hours=hrs,competencies=comps,units=units,labs=labl,cos=cos,capstone=dict(name=capname.strip(),desc=capdesc.strip()),careers=[x.strip() for x in re.findall(r'.*?(?:Engineer|Scientist|Architect|Manager|Analyst|Developer|Auditor|Specialist|Lead|Researcher|Officer|Consultant|Designer|Technologist|Hunter|Responder)(?: \([^)]*\))?(?=\s|$)',car)],languages=[l[1] for l in langs],certs=certnames))
for c in courses: print(c['num'],c['code'],c['title'],len(c['units']),len(c['labs']),len(c['cos']),c['languages'],len(c['certs']),file=sys.stderr)
json.dump(courses,open(sys.argv[2],'w'),indent=1,ensure_ascii=False)
