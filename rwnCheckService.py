# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import collections
import tarfile
import re

rel_re=re.compile(u'<relation parent_id="(\w+)" child_id="(\w+)" name="(\w+)"/>')

sense2synset =    {}
relations    =    {}
ant = set()

poss = ['A','N','V']
tgzname = 'rwn-xml-2017-03-30.tgz'

revrels = {'hypernym':'hyponym','meronym':'holonym','cause':'effect','entailment':'precondition', 'domain':'part-of-domain'}
revrels.update({v:k for k,v in revrels.iteritems()})

def revrelname(rel_name):
	try:
		toks = rel_name.split(' ')
		toks[-1]=revrels[toks[-1]]
		return ' ' . join(toks)
	except KeyError:
		return rel_name
	
def readsynsets(tar_obj):
	global sense2synset
	for pos in poss:
		s=BeautifulSoup(tar_obj.extractfile('./synsets.'+pos+'.xml').read(),"lxml")
		for syns in s.find_all('synset'):
			for sense in syns.find_all('sense'):
				if not   sense.attrs['id'] in sense2synset:
					sense2synset[sense.text] = []
				sense2synset[sense.text].append(syns.attrs['id'])
		
def readantonyms():
	global ant
	for rels in open('lvov.n').readlines():
				la=rels.strip().decode('utf-8').upper().encode('utf-8'). split('—')
				if len(la) < 2:
					la=rels.strip().decode('utf-8').upper().encode('utf-8'). split(' ')
					if len(la) < 2:
						print "Bad antonym rec: ", rels
						continue
				print la[0], la[1]
				ant.add((la[0].decode('utf-8'),la[1].decode('utf-8')))


def readrelations(tar_obj):
	global relations
	for pos in poss:
		s=BeautifulSoup(tar_obj.extractfile('./synset_relations.'+pos+'.xml').read(),"lxml")
		for rels in s.find_all('relation'):
				print rels.attrs['parent_id'], rels.attrs['child_id']
				relations[rels.attrs['parent_id'],rels.attrs['child_id']] =revrelname(rels.attrs['name'])
				relations[rels.attrs['child_id'],rels.attrs['parent_id']] =rels.attrs['name']
		

def init():
	tar_obj = tarfile.open(tgzname,'r:gz')
	readsynsets(tar_obj)
	readantonyms()
	readrelations(tar_obj)

def check(x,y):
	r = []
	if (x,y) in ant or (y,x) in ant:
		return ['antonym']
	try:
	   for xs in sense2synset[x]:
		for ys in sense2synset[y]:
			if xs == ys:
				r.append('synonym')
			else:
				try:
					r.append(relations[xs,ys])
				except  KeyError:
					pass
	   if r:
		return r
	   else:
			return [ xs,ys ]
	except  KeyError:
		pass
	return r

from flask import Flask, request, Response
from flask_restful import Resource, Api 
import sys
import json

app = Flask(__name__)
api = Api(app)


class TagAPI_REST(Resource):
    def get(self):
	q = json.loads(request.data) 
	out = []
	for p in q:
		out.append(check(p[0],p[1]))
	return Response(json.dumps(out), status=200,  mimetype='application/json')

	

if __name__ == '__main__':
    init()
    api.add_resource(TagAPI_REST, '/checkrel')
    app.run(debug=True, host='0.0.0.0', port=6565)
