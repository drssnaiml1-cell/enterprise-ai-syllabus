import json,sys
d=json.load(open(sys.argv[1]))
t=open(sys.argv[2]).read().replace('__DATA__',json.dumps(d,ensure_ascii=False).replace('</','<\\/'))
import os
car=json.load(open(os.path.join(os.path.dirname(sys.argv[1]),'careers.json')))
t=t.replace('__CAREERS__',json.dumps(car,ensure_ascii=False).replace('</','<\\/'))
prod=json.load(open(os.path.join(os.path.dirname(sys.argv[1]),'products.json')))
t=t.replace('__PRODUCTS__',json.dumps(prod,ensure_ascii=False).replace('</','<\\/'))
open(sys.argv[3],'w').write(t)
