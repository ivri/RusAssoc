#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')



import codecs
import re
#борода{борода};черная{черный|черная}
#вдовый{вдовый};-
#совместный{совместный};не{не} один{один}
lemm_list = codecs.open('stim.reacts.stm','r','utf-8').readlines()

lemmas_list=[]
for line in lemm_list:
	lemms = ''
	pair = line.split(';')
	for item in pair:
		subtoks = item.split(' ')
		for i in range(0,len(subtoks)):
			if '{' in subtoks[i]:
				lemmas = re.findall(r'\{([^}]+)\}',subtoks[i])[0]
				if '|' in lemmas:
					lemms += lemmas.split('|')[0].replace('?','')
				else:
					lemms += lemmas.replace('?','')
			else:
				lemms += subtoks[i].replace('\n','')
			if len(subtoks)>1 and i<len(subtoks)-1:
				lemms +=' '
		lemms += ';'
#	print lemms
	if not re.match(r'^ +; +$',lemms):
		lemmas_list.append(re.sub(r';$','',lemms))



reader = codecs.open('urals.0911.srt.lc.upd','r','utf-8')
writer = codecs.open('urals.0911.srt.lc.final','w','utf-8')


i = 0
for line in reader.readlines():
#       print line
        #tokens = line.split(';')
	writer.write(line.replace('\n','')+';' + lemmas_list[i]+'\n')
	i+=1
writer.close()
reader.close()

		
