import json,sys
d=json.load(open(sys.argv[1]))
t=open(sys.argv[2]).read().replace('__DATA__',json.dumps(d,ensure_ascii=False).replace('</','<\\/'))
open(sys.argv[3],'w').write(t)
