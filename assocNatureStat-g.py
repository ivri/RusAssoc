# -*- coding: utf-8 -*-
import math
import collections

fn = "urals.0911.srt.lc.ann_rel"
thres = 1000

features=[None,None,None,None,'age','occup','city']

rename_val ={
'occup':
{
"вми":"информационные технологии",
"тмио":"технология машиностроения",
"бжд":"физическая культура",
"организация работы с молодежью":"связи с общественностью",
"тгсив":"гидравлика",
"управление персоналом":"документоведение и доу",
"городской кадастр":"документоведение и доу",
"налоги и налогообложение":"финансы и кредит",
#"гидравлика","",
"бухгалтерский учет":"финансы и кредит",
"культурология":"гуманитарное образование",
"история":"гуманитарное образование"
}
}

remove_val = {'occup':
{
"студент"
}
}


def zerodict():
	return collections.defaultdict(lambda:0)

def default_row_info():
	return {
		'count':zerodict(),'nngf':zerodict(),'nngf13':zerodict(),'nngf100':zerodict(),'sumlogngf':zerodict(),
		'nrel':collections.defaultdict(lambda:zerodict())
	}

fvals = [collections.defaultdict(default_row_info) for i in range(len(features)) ]
overall = default_row_info() 
rvals = set()


def addline(dst,fields):
	global rvals
	gender=fields[3]
	dst['count'][gender]+=1
	ngf = int(fields[9])
	if (ngf):
		dst['nngf'][gender] += 1
		if ngf > 13:
			dst['nngf13'][gender] += 1
		if ngf > 100:
			dst['nngf100'][gender] += 1
		dst['sumlogngf'][gender] += math.log(1+ngf , 2)
	rels = fields[10].split(',')
	for rel in rels:
			if rel:
				dst['nrel'][rel][gender]+=1
				rvals.add(rel)

def load():
    global overall
    for l in open(fn).readlines():
	fields = l.strip().split(';')
	addline(overall,fields)
	for j in range(len(features)):
		if features[j]:
			if features[j] in remove_val and fields[j] in remove_val[features[j]]:
				continue
			try:
				fields[j] = rename_val[features[j]][fields[j]]
			except KeyError:
				pass
			dst = fvals[j][fields[j]]
			addline(dst,fields)

def balanced(x,counts):
	s = 0
	cs = 0
	for g,v in x.iteritems():
		s += 0.5*x[g]/counts[g]
		cs += counts [g]
	return s*cs

def balance_gender(src):
	dst = {}
	counts = src['count']
	for k in ('count','sumlogngf','nngf', 'nngf13', 'nngf100'):
		dst[k] = balanced(src[k],counts)
	dst['nrel']={}
	for k in src['nrel']:
		dst['nrel'][k] = balanced(src['nrel'][k],counts)
	return dst

def display_row(name, src):
	row = [name]
	c = src['count']
	row.append(c)
	row.append(100*float(src['sumlogngf'])/c)
	row.append(100*float(src['nngf'])/c)
	row.append(100*float(src['nngf13'])/c)
	row.append(100*float(src['nngf100'])/c)


	for val in rvals:
		row.append(100*float(src['nrel'][val])/c if val in src['nrel'] else 0)
	
	return map(lambda x:'%.3f' % x if isinstance(x,float) else str(x),row)
	
def display():
	hdr=['','count','sumlogngf','%nngf','%ngf13','%ngf100']
	for val in rvals:
		hdr.append(val)
	print (';'.join(hdr))
	print (';'.join(display_row('overall',balance_gender(overall))))
	for j in range(len(features)):
		if features[j]:
			for val,src in fvals[j].iteritems():
				bsrc = balance_gender(src)
				if bsrc['count'] >= thres:
					print (';'.join(display_row(features[j]+'='+val,bsrc)))
				
			

load()
display()
			
