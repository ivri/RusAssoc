# -*- coding: utf-8 -*-
import math
import collections

fn = "urals.0911.srt.lc.ann_rel"
thres = 1000

features=[None,None,None,'gender','age','occup','city']

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


def default_row_info():
	return {
		'count':0,'nngf':0,'nngf13':0,'nngf100':0,'sumlogngf':0,
		'nrel':collections.defaultdict(lambda:0)
	}

fvals = [collections.defaultdict(default_row_info) for i in range(len(features)) ]
overall = default_row_info() 
rvals = set()
forstimul = collections.defaultdict(default_row_info) 


def addline(dst,fields,k):
	global rvals
	dst['count']+=1*k
	ngf = int(fields[9])
	if (ngf):
		dst['nngf'] += 1*k
		if ngf > 13:
			dst['nngf13'] += 1*k
		if ngf > 100:
			dst['nngf100'] += 1*k
		dst['sumlogngf'] += math.log(1+ngf , 2)*k
	rels = fields[10].split(',')
	for rel in rels:
			if rel:
				dst['nrel'][rel]+=1*k
				rvals.add(rel)

def loadforstimuli():
    global forstimul
    for l in open(fn).readlines():
	fields = l.strip().split(';')
	stimul=fields[1]
	fields = l.strip().split(';')
	addline(forstimul[stimul],fields,1.0)
    for stimul,r in forstimul.iteritems():
	divide(r)

def load():
    global overall
    for l in open(fn).readlines():
	fields = l.strip().split(';')
	stimul=fields[1]
	addline(overall,fields,1.0)
	minus(overall,forstimul[stimul])
	for j in range(len(features)):
		if features[j]:
			if features[j] in remove_val and fields[j] in remove_val[features[j]]:
				continue
			try:
				fields[j] = rename_val[features[j]][fields[j]]
			except KeyError:
				pass
			dst = fvals[j][fields[j]]
			addline(dst,fields,1.0)
			minus(dst,forstimul[stimul])

def minus(src,y):
	src['sumlogngf'] -= ((y['sumlogngf']))
	src['nngf'] -= ((y['nngf']))
	src['nngf13'] -= ((y['nngf13']))
	src['nngf100'] -= ((y['nngf100']))

	for val in rvals:
		src['nrel'][val] -= ((y['nrel'][val]) if val in src['nrel'] else 0)

def divide(src):
	c = src['count']
	src['sumlogngf'] = (float(src['sumlogngf'])/c)
	src['nngf'] = (float(src['nngf'])/c)
	src['nngf13'] = (float(src['nngf13'])/c)
	src['nngf100'] = (float(src['nngf100'])/c)

	for val in rvals:
		src['nrel'][val] = (float(src['nrel'][val])/c if val in src['nrel'] else 0)
	
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
	print (';'.join(display_row('overall',overall)))
	for j in range(len(features)):
		if features[j]:
			for val,src in fvals[j].iteritems():
				if src['count'] >= thres:
					print (';'.join(display_row(features[j]+'='+val,src)))
				
			


loadforstimuli()
load()
display()
			
