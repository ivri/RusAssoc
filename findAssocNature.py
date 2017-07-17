import json
import  requests
import logging
logging.getLogger("requests").setLevel(logging.WARNING)

def check (x,y,lx,ly):
	#ngrams
	query = [x.split(' ')+ y.split(' '), lx.split(' ')+y .split(' '),\
		 x.split(' ')+ly.split(' '), lx.split(' ')+ly.split(' '),\
		 y.split(' ')+ x.split(' '), ly.split(' ')+x .split(' '),\
		 y.split(' ')+lx.split(' '), ly.split(' ')+lx.split(' ')
	]
	if (len(query[0])) > 3:
		print "Skipped:", query[0]
		resp_n=0
	else:
		r= requests.get("http://0.0.0.0:6564/checkngram", json=query)
		#print "Content:", r.content
		resp_n = max ( json.loads(r.content.strip().strip('"')) )
	#print "Response_n", resp_n,isinstance(resp_n,list)
		
	#rels
	query = [[lx,ly]]
	r= requests.get("http://0.0.0.0:6565/checkrel", json=query)
	#print "Content:", r.content
	resp_r = reduce(lambda x,y:x+y, json.loads(r.content.strip().strip('"') ))
		
	#print "Response", resp_r,isinstance(resp_r,list)
	classes = ((filter(lambda x: isinstance(x,(str,unicode) ) and not
		x[1].isdigit(),resp_r)) )
	#print x, y, lx, ly, classes
	return unicode(resp_n)+';'+','.join(classes)



fn = "urals.0911.srt.lc.final"


#of = open(fn+'.rela')
for l in open(fn).readlines():
	la=l.strip().decode('utf-8').upper().encode('utf-8').split(';')
	d = check(la[1],la[2],la[7],la[8])
	outl = l.strip().decode('utf-8')+';'+d
	print outl.encode('utf-8') # > of
	
