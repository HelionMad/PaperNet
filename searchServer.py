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

class Papernet_dashboardService(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')

    def PUT(self, querystring, qtype):
        with open('stdev.txt', 'r') as f:
            cherrypy.session['mean'] = float(f.readline())
            cherrypy.session['stdev'] =  float(f.readline())

        cherrypy.session['querystring'] = querystring
        cherrypy.session['qtype'] = qtype
        cherrypy.session['queryresult'] = ''
        cherrypy.session['n_dev']=2

    def GET(self,info,GETtype):
        if GETtype=="update":
            print "&&&&&&&&&&&&&&&",info
            cherrypy.session['n_dev']=info
            computegraph()
            return "updated"
        elif GETtype=="getstdev":
            print "*********stdev**********"
            return str(cherrypy.session['n_dev'])
        elif GETtype=="result":
            print "*********ready to compute*********"
            computegraph()
            return 'a'
        elif GETtype=="getpaper":
            return 0


def computegraph(n_dev=2):
    print cherrypy.session['qtype']
    if cherrypy.session['qtype'] == "title":
        queryKey = cherrypy.session['querystring'].encode().lower().translate(None,string.punctuation) 
        key=queryKey.split();
        #searchQuery = "SELECT distinct cluster from papers where "
        searchQuery = "SELECT distinct cluster from papers inner join citepaper on papers.id=citepaper.paper_id where "
        i=0
        clusterSize=[0 for row in range(22)]
        for i in range(len(key)-1):
            searchQuery+= "title like \'% " + key[i] + " %\' and ";
        i=i+1
        #searchQuery+="title like \'% " + key[i] + " %\';"
        searchQuery+="title like \'% " + key[i] + " %\' order by degree DESC limit 200;"
        print searchQuery
        cursor1.execute(searchQuery)
        allCluster=[]
        for row in cursor1:
            allCluster.append(row[0])

        print "+++++++start process++++++++"
        allId=[]
        allTitle=[]
        allAbstract=[]
        allKeyword=[]
        allAuthor=[]
        
        for i in range(len(allCluster)):
            getChildren="select id from papers where cluster='"+str(allCluster[i])+"' limit 1;"
            cursor1.execute(getChildren)
            allId.append(cursor1.fetchone()[0])
        
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
                    if line[0]>cherrypy.session['mean']+cherrypy.session['stdev']*float(n_dev):
                        link.append({"source":i,"target":j,"value":line[0]})
                getWeight="select weight from citegraph where id_cite='"+allId[i]+"' and id_cited='"+allId[j]+"';"
                cursor2.execute(getWeight)
                for line in cursor2:
                    if line[0]>cherrypy.session['mean']+cherrypy.session['stdev']*float(n_dev):
                        link.append({"source":i,"target":j,"value":line[0]})

        #print getWeight

        print '*********processed***********'
        gdict = { "nodes" : [ x for x in node],
                    "links" : [ x for x in link]}

        filename="result.json"
        with open("search/"+filename, 'w') as outfile:
            json.dump(gdict, outfile, indent=4, separators=(',', ': '))

        return filename
        '''for j in range(1,23):
            paperQuery = searchQuery+"and cite_cluster="+str(j)+";"
            print paperQuery
            try:
                cursor1.execute(paperQuery)
                
                count=0
                dict_weight=[]
                dict_name=[]
                idList=[]
                filename="cluster"+str(j)+".json"
                for cluster in cursor1:
                    if count<200:
                        searchCluster="SELECT id from papers where cluster= "+str(cluster[0])+" limit 1;"
                        cursor2.execute(searchCluster)
                        id=cursor2.fetchone()
                        idList.append(id[0])
                        searchDetail1 = "SELECT title, abstract from papers where id= \'"+ id[0] +"\';"
                        cursor3.execute(searchDetail1)
                        result1=cursor3.fetchone()
                        searchDetail2 = "SELECT name from authors where paperid =\'"+ id[0] +"\';"
                        cursor3.execute(searchDetail2)
                        result2=""
                        for row in cursor3:
                            result2+=row[0]+"  "
                        dict_name.append({'name':result1[0],'abstract':result1[1],'authors':result2})

                    else:
                        break;
                clusterSize[j-1]=cluster[1]
                for k1 in range(len(idList)):
                    for k2 in range(len(idList)):
                        if k1!=k2:
                            searchWeight="SELECT weight from citegraph where id_cite=\'"+idList[k1]+"\' and id_cited =\'"+idList[k2]+"\';"
                            cursor3.execute(searchWeight)
                            for line in cursor3:
                                dict_weight.append({'source':k1,'target':k2,'value':line[0]})
                sdict = { "nodes" : [ x for x in dict_name ],
                    "links" : [x for x in dict_weight]}
                 
                with open(filename, 'w') as outfile:
                    json.dump(sdict, outfile, indent=4, separators=(',', ': '))

            except:
                continue'''



def compare(stringA,stringB):
    stringA.encode().lower().translate(None,string.punctuation)
    stringB.encode().lower().translate(None,string.punctuation)
    A=stringA.split()
    B=stringB.split()
    ban=['the','to','and','of','be','is','are','in']
    banlist = {k:v for k, v in zip(ban, map(hash, ban))}
    intersection = 0
    dictT={}
    for i in range(len(A)):
        if banlist.has_key(A[i]):
            #print 'common true'
            continue
        if dictT.has_key(A[i]):
            intersection=intersection+1
            continue
        for j in range(len(B)):
            
            if banlist.has_key(B[j]):
                continue
            if Levenshtein.ratio(A[i],B[j])>0.8:
                intersection=intersection+1
                dictT[A[i]]=hash(A[i])
                dictT[B[j]]=hash(B[j])
    for i in range(len(B)):
        if dictT.has_key(B[i]):
            intersection=intersection+1
    union=len(A)+len(B)-intersection
    if union==0:
        union=1
    return intersection/union
