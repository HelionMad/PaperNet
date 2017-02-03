#coding=utf-8 
from __future__ import division
import os, os.path
import cherrypy
import string
import json
import mysql.connector
import math
import re
import numpy
from mysql.connector import errorcode

cnx = mysql.connector.connect(user='root', password='starcraft2',
                              host='127.0.0.1',
                              database='citeseer')
cursor1 = cnx.cursor(buffered=True)
cursor2 = cnx.cursor(buffered=True)
cursor3 = cnx.cursor(buffered=True)

record=[]
class Papernet_exploreService(object):
	exposed = True
	

	@cherrypy.tools.accept(media='text/plain')

	#def PUT(self, querystring, qtype):


	def GET(self,info,GETtype):
		if GETtype=="top":
			del record[:]
			record.append("top")
			return "top"
		elif GETtype=="landmark":
			result = computeLandmark(int(info))
			record.append(result)
			return result
		elif GETtype=="getGroup":
			result=computegroup(info)
			record.append(result)
			return result
		elif GETtype=="getPaper":
			result=computePaper(info)
			record.append(result)
			return result
		elif GETtype=="back":
			print record
			print record.pop()
			result=record[len(record)-1]
			return result



def computeLandmark(cid):
	getLandmark="select paper_id from citepaper where citecluster="+str(cid)+" limit 1;"
	cursor1.execute(getLandmark)
	center = cursor1.fetchone()[0]
	getCC="select cluster from papers where id='"+center+"';"
	cursor1.execute(getCC)
	cenCluster=cursor1.fetchone()[0]
	getChildren="select count(paperid) from citations where cluster='"+str(cenCluster)+"';"
	cursor1.execute(getChildren)
	group = int(math.floor(cursor1.fetchone()[0]/100))

	print "start"
	getDetail="select title,abstract from papers where id='"+center+"';"
	print center
	cursor1.execute(getDetail)
	result=cursor1.fetchone()
	cTitle=result[0]
	cAbstract=result[1]
	getKey="select keyword from keywords where paperid='"+center+"';"
	cursor1.execute(getKey)
	cKeywords=""
	for line in cursor1:
		cKeywords+=line[0]+", "
	cKeywords=cKeywords[:-2]
	getAuthor="select name from authors where paperid='"+center+"';"
	cursor1.execute(getAuthor)
	cAuthors=""
	for line in cursor1:
		cAuthors+=line[0]+", "
	cAuthors=cAuthors[:-2]
	#split groups
	node=[]
	link=[]
	node.append({"name":"landmark","title":cTitle,"abstract":cAbstract,"keyword":cKeywords,"author":cAuthors,"group":1})
	for i in range(group):
		node.append({"name":"group"+str(i+1),"group":i+1})
		link.append({"source":0,"target":i+1,"value":1})

	gdict = { "nodes" : [ x for x in node],
				"links" : [ x for x in link]}

	with open('plot/groupgraph.json', 'w') as outfile:
		json.dump(gdict, outfile, indent=4, separators=(',', ': '))

	print "done"
	return 'group'+str(cid)


def computegroup(info):
	print '***********************'
	print info
	cluster=record[len(record)-1]
	cluster=cluster[5:]
	print cluster
	getCenter="select paper_id from citepaper where citecluster="+ cluster +" limit 1;"
	print getCenter
	cursor1.execute(getCenter)
	center = cursor1.fetchone()[0]
	getCC="select cluster from papers where id='"+center+"';"
	cursor1.execute(getCC)
	cenCluster=cursor1.fetchone()[0]

	allId=[]
	allTitle=[]
	allAbstract=[]
	allKeyword=[]
	allAuthor=[]
	allId.append(center)
	getChildren="select paperid from citations where cluster='"+str(cenCluster)+ "' \
					limit "+str((int(info)*100))+",100;"
	cursor1.execute(getChildren)
	for row in cursor1:
		allId.append(row[0])
	
	for i in range(len(allId)):
		getTA="select title,abstract from papers where id='"+allId[i]+"';"
		cursor2.execute(getTA)
		for line in cursor2:
			allTitle.append(line[0])
			allAbstract.append(line[1])
	for i in range(len(allId)):
		getKey="select keyword from keywords where paperid='"+allId[i]+"';"
		cursor2.execute(getKey)
		keywords=""
		for line in cursor2:
			keywords+=line[0]+", "
		keywords=keywords[:-2]
		allKeyword.append(keywords)
	for i in range(len(allId)):
		getAuthor="select name from authors where paperid='"+allId[i]+"';"
		cursor2.execute(getAuthor)
		authors=""
		for line in cursor2:
			authors+=line[0]+", "
		authors=authors[:-2]
		allAuthor.append(authors)
	node=[]
	for i in range(len(allId)):
		node.append({"name":allId[i],"title":allTitle[i],"abstract":allAbstract[i],
						"group":i,"keyword":allKeyword[i],"author":allAuthor[i]})
	
	link=[]
	for i in range(len(allId)):
		for j in range(i+1,len(allId)):
			getWeight="select weight from citegraph where id_cite='"+allId[j]+"' and id_cited='"+allId[i]+"';"
			cursor2.execute(getWeight)
			for line in cursor2:
				link.append({"source":i,"target":j,"value":line[0]})
	#print getWeight


	gdict = { "nodes" : [ x for x in node],
				"links" : [ x for x in link]}

	filename="group"+info+".json"
	with open("plot/"+filename, 'w') as outfile:
		json.dump(gdict, outfile, indent=4, separators=(',', ': '))

	return filename

def computePaper(pid):
	getCenter="select cluster from papers where id='"+str(pid)+"';"
	cursor1.execute(getCenter)
	cenCluster=cursor1.fetchone()[0]
	getChildren="select count(paperid) from citations where cluster='"+str(cenCluster)+"';"
	cursor1.execute(getChildren)
	group = int(math.floor(cursor1.fetchone()[0]/100))


	if group>5:
		#split
		getDetail="select title,abstract from papers where id='"+pid+"';"
		cursor1.execute(getDetail)
		result=cursor1.fetchone()
		cTitle=result[0]
		cAbstract=result[1]
		getKey="select keyword from keywords where paperid='"+pid+"';"
		cursor1.execute(getKey)
		cKeywords=""
		for line in cursor1:
			cKeywords+=line[0]+", "
		cKeywords=cKeywords[:-2]
		getAuthor="select name from authors where paperid='"+pid+"';"
		cursor1.execute(getAuthor)
		cAuthors=""
		for line in cursor1:
			cAuthors+=line[0]+", "
		cAuthors=cAuthors[:-2]
		#split groups
		node=[]
		link=[]
		node.append({"name":"landmark","title":cTitle,"abstract":cAbstract,"keyword":cKeywords,"author":cAuthors,"group":1})
		for i in range(group):
			node.append({"name":"group"+str(i+1),"group":i+1})
			link.append({"source":0,"target":i+1,"value":1})

		gdict = { "nodes" : [ x for x in node],
					"links" : [ x for x in link]}

		with open('plot/groupgraph.json', 'w') as outfile:
			json.dump(gdict, outfile, indent=4, separators=(',', ': '))

		print "done"
		return 'group'
	else:
		#plot all
		allId=[]
		allTitle=[]
		allAbstract=[]
		allKeyword=[]
		allAuthor=[]
		allId.append(pid)
		getChildren="select paperid from citations where cluster='"+str(cenCluster)+ "';"
		cursor1.execute(getChildren)
		for row in cursor1:
			allId.append(row[0])
		
		for i in range(len(allId)):
			getTA="select title,abstract from papers where id='"+allId[i]+"';"
			cursor2.execute(getTA)
			for line in cursor2:
				allTitle.append(line[0])
				allAbstract.append(line[1])
		for i in range(len(allId)):
			getKey="select keyword from keywords where paperid='"+allId[i]+"';"
			cursor2.execute(getKey)
			keywords=""
			for line in cursor2:
				keywords+=line[0]+", "
			keywords=keywords[:-2]
			allKeyword.append(keywords)
		for i in range(len(allId)):
			getAuthor="select name from authors where paperid='"+allId[i]+"';"
			cursor2.execute(getAuthor)
			authors=""
			for line in cursor2:
				authors+=line[0]+", "
			authors=authors[:-2]
			allAuthor.append(authors)
		node=[]
		for i in range(len(allId)):
			if allAbstract[i]!=None:
				node.append({"name":allId[i],"title":allTitle[i],"abstract":allAbstract[i],
							"group":i,"keyword":allKeyword[i],"author":allAuthor[i]})
			else:
				print allAbstract[i]
		
		link=[]
		for i in range(len(allId)):
			for j in range(i+1,len(allId)):
				getWeight="select weight from citegraph where id_cite='"+allId[j]+"' and id_cited='"+allId[i]+"';"
				cursor2.execute(getWeight)
				for line in cursor2:
					link.append({"source":i,"target":j,"value":line[0]})
		#print getWeight


		gdict = { "nodes" : [ x for x in node],
					"links" : [ x for x in link]}

		filename=allId[0]+".json"
		with open("plot/"+filename, 'w') as outfile:
			json.dump(gdict, outfile, indent=4, separators=(',', ': '))

		return filename

'''def getBack():
	###no need to recompute just maintain a list of return info
	center=record[len(record)-1]
	prior=record[len(record)-2]
	if isInt(center):
		if prior=="top":

	else:

	print center
	print record

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False'''





