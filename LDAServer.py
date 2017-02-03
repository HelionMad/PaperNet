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
import csv


cnx = mysql.connector.connect(user='root', password='starcraft2',
                              host='127.0.0.1',
                              database='citeseer')
cursor1 = cnx.cursor(buffered=True)
cursor2 = cnx.cursor(buffered=True)
cursor3 = cnx.cursor(buffered=True)

class Papernet_LDAService(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')

    def PUT(self, querystring, qtype):
        cherrypy.session['querystring'] = querystring
        cherrypy.session['qtype'] = qtype

    def GET(self,info,GETtype):
        if GETtype=='top':
            lda = getLDA()
            #cId="10.1.1.110.4050"
            #cId="10.1.1.15.2541"
            #cId='10.1.1.25.5975'
            cId=cherrypy.session['querystring']
            lda.computeLDAgraph(cId)
            lda.computeRELDAgraph(cId)
            return 'success'

class getLDA(object):
    def __init__(self):
        self.idSet=[]
        self.paperData=[]
        self.paperReData=[]

    def computeLDAgraph(self,cId):
        print 'startLDA'

        with open('weight.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.paperData.append(row);
        f.close()
        for paper in self.paperData:
            self.idSet.append(paper[0])
            self.idSet.append(paper[1])
        self.idSet=list(set(self.idSet))

        allId=[]
        link=[]
        #cId='10.1.1.110.4050'
        #cId='10.1.1.11.9133'
        allId.append(cId)

        print 'start tree'
        count=0
        src=0
        while(self.getNextLevel(cId)):
            tar=len(allId)
            temp=[]
            for i in self.paperData:
                if i[0]==cId:
                    temp.append(i)
            for j in range(len(temp)):
                for k in range(j+1,len(temp)):
                    if float(temp[j][2])<float(temp[k][2]):
                        tt=temp[j]
                        temp[j]=temp[k]
                        temp[k]=tt
            print len(temp)
            try:
                allId.append(temp[0][1])
                link.append({"source":src,"target":tar,"value":temp[0][2]})
            except:
                pass
            try:
                allId.append(temp[1][1])
                link.append({"source":src,"target":tar+1,"value":temp[1][2]})
            except:
                pass
            try:
                allId.append(temp[2][1])
                link.append({"source":src,"target":tar+2,"value":temp[2][2]})
            except:
                pass
            print 'cid',cId
            cId=temp[0][1]
            src=tar

        print 'treeover'

        allTitle=[]
        allAbstract=[]
        allKeyword=[]
        allAuthor=[]

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
        gdict = { "nodes" : [ x for x in node],
            "links" : [ x for x in link]}

        filename="LDA.json"
        with open("search/"+filename, 'w') as outfile:
            json.dump(gdict, outfile, indent=4, separators=(',', ': '))

        le=[]
        for i in range(len(self.paperData)):
            le.append(self.paperData[i][0])
            le.append(self.paperData[i][1])
        le=list(set(le))
        print 'length of ALLLLLLLLL',len(le)


    def computeRELDAgraph(self,cId):
        print 'startLDA'

        with open('refreshedWeight.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.paperReData.append(row);
        f.close()
        for paper in self.paperReData:
            self.idSet.append(paper[0])
            self.idSet.append(paper[1])
        self.idSet=list(set(self.idSet))

        allId=[]
        link=[]
        #cId='10.1.1.110.4050'
        #cId='10.1.1.11.9133'
        allId.append(cId)

        print 'start tree'
        count=0
        src=0
        while(self.getNextReLevel(cId)):
            tar=len(allId)
            temp=[]
            for i in self.paperReData:
                if i[0]==cId:
                    temp.append(i)
            for j in range(len(temp)):
                for k in range(j+1,len(temp)):
                    if float(temp[j][2])<float(temp[k][2]):
                        tt=temp[j]
                        temp[j]=temp[k]
                        temp[k]=tt
            print len(temp)
            try:
                allId.append(temp[0][1])
                link.append({"source":src,"target":tar,"value":temp[0][2]})
            except:
                pass
            try:
                allId.append(temp[1][1])
                link.append({"source":src,"target":tar+1,"value":temp[1][2]})
            except:
                pass
            try:
                allId.append(temp[2][1])
                link.append({"source":src,"target":tar+2,"value":temp[2][2]})
            except:
                pass
            print 'cid',cId
            cId=temp[0][1]
            src=tar

        print 'treeover'

        allTitle=[]
        allAbstract=[]
        allKeyword=[]
        allAuthor=[]

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
        gdict = { "nodes" : [ x for x in node],
            "links" : [ x for x in link]}

        filename="LDA_refresh.json"
        with open("search/"+filename, 'w') as outfile:
            json.dump(gdict, outfile, indent=4, separators=(',', ': '))

    def getNextLevel(self,targetId): 
        for i in self.paperData:
            if targetId==i[0]:
                return True
        return False

    def getNextReLevel(self,targetId):
        for i in self.paperReData:
            if targetId==i[0]:
                return True
        return False


