import json,sys
d=json.load(open(sys.argv[1]))
import os
_x=os.path.join(os.path.dirname(sys.argv[1]),'extra_courses.json')
if os.path.exists(_x): d=d+json.load(open(_x))
for _c in d: _c.setdefault('track','core' if _c['num']<=10 else 'em')
t=open(sys.argv[2]).read().replace('__DATA__',json.dumps(d,ensure_ascii=False).replace('</','<\\/'))
import os
car=json.load(open(os.path.join(os.path.dirname(sys.argv[1]),'careers.json')))
t=t.replace('__CAREERS__',json.dumps(car,ensure_ascii=False).replace('</','<\\/'))
prod=json.load(open(os.path.join(os.path.dirname(sys.argv[1]),'products.json')))
t=t.replace('__PRODUCTS__',json.dumps(prod,ensure_ascii=False).replace('</','<\\/'))
uni=json.load(open(os.path.join(os.path.dirname(sys.argv[1]),'unicorn.json')))
t=t.replace('__UNICORN__',json.dumps(uni,ensure_ascii=False).replace('</','<\\/'))
open(sys.argv[3],'w').write(t)
