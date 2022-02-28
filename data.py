# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 00:17:49 2022

@author: ahmed
"""

import openreview
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime
import pathlib
def extract_profiles(authors):
    lastNoOfAuthor=0
    CurrentNoOfAuthor=0
    dic={}
    while(len(authors)>0):
        CurrentNoOfAuthor=len(authors)
        if(CurrentNoOfAuthor==lastNoOfAuthor):
            break
        profiles=client.search_profiles(list(set(authors)))
        missed=[]
        for x in authors:
            if(x in profiles):
                if  "@" in x:
                    dic[x]=[profiles[x].content['names'][0]['first']+
                    " "+profiles[x].content['names'][0]['last'],profiles[x].id]
                else:
                    dic[x]=[profiles[x].content['names'][0]['first']+
                    " "+profiles[x].content['names'][0]['last']]
            else:
                missed.append(x)
        authors=missed
        lastNoOfAuthor=CurrentNoOfAuthor
        
    return dic
def combining_profiles(emails_and_id):
    ids = list(filter(lambda x: "@" not in x, set(emails_and_id)))
    emails = list(filter(lambda x: "@" in x, set(emails_and_id)))
    dic = extract_profiles(ids)
    dic.update(extract_profiles(emails))  
    return dic
def adder(dic,user):
    if user in list(dic.keys()):
        dic[user]=dic[user]+1
    else:
        dic[user]=1
    return dic

def nameToDate(s):
    d= datetime.strptime(s, '%B')
    if int(d.strftime('%m'))<5:
        return d.strftime('2022- %m-%d')
    return d.strftime('2021- %m-%d')
def add_missing_assignments(user,dic,dic2):
    if (user in list(dic.keys())):
        if (email2id[user][1] in list(dic2.keys())):
            return dic2[email2id[user][1]]
        else:
            return 0.0
    else:
        return 0.0
def email2name(user,dic):
    if (user in list(dic.keys())):
        return dic[user][0]
    else:
        return user
load_dotenv()
USER = os.getenv('USER')
password = os.getenv('password')
client = openreview.Client(baseurl='https://api.openreview.net', username=USER, password=password)

review_iterator = openreview.tools.iterget_notes(client, invitation='aclweb.org/ACL/ARR/20.*Paper.*Official_Review', details="writable")
data=list(review_iterator)

review_iterator = openreview.tools.iterget_notes(client, invitation='(?=aclweb.org/ACL/ARR/.*Recruit.*)(?!.*Area_Chairs).*')
reviewers_recruitment=list(review_iterator)

authors=[]
[authors.append(x.tauthor) for x in data]
email2id=combining_profiles(authors)
ids=[i[1] for i in list(email2id.values())]
emails=list(email2id.keys())
missed_assg={}
for review_assignment in reviewers_recruitment:
    user = review_assignment.content['user']
    if review_assignment.content['response']=="No":
        if (user in emails):
            ID=email2id[user][1]
            missed_assg=adder(missed_assg,ID)
        if  (user in ids):
            missed_assg=adder(missed_assg,user)
            
contents=[]
authors=[]
for x in data:
    dic=x.content
    dic["author"]=x.tauthor
    dic["month"]=x.invitation
    contents.append(dic)
df=pd.DataFrame(contents)
AVGfeatures=["paper_summary" ,"summary_of_strengths","summary_of_weaknesses","comments,_suggestions_and_typos"]
NUMfeatures=["confidence" ,"overall_assessment","reproducibility","datasets","software","author_identity_guess"]
for feature in AVGfeatures:
    df[feature] = df[feature].apply(lambda x: len(x))
for feature in NUMfeatures:
    df[feature]=df[feature].str.extract('(\d*\.?\d+)')
    df[feature]=df[feature].astype(float)
df["month"]=df["month"].str.extract('aclweb.org/ACL/ARR/\d+/(.*)/Paper.*')
df["month"]=df["month"].apply(lambda x: nameToDate(x))
df= df.drop(["best_paper_justification" ,"limitations_and_societal_impact","ethical_concerns" ,"replicability" ,"ethical_concernes","reproducibility","needs_ethics_review"], axis=1)
df['missed_assignments']=df['author'].apply(lambda x: add_missing_assignments(x,email2id,dic))

df['author']=df['author'].apply(lambda x: email2name(x,email2id))
f=df.groupby(["month","author"]).mean()
f["count"]="No. of papers: "
f["count"]=f["count"].map(str) + df.groupby(["month","author"]).count()["confidence"].map(str)

PATH = pathlib.Path(__file__)
DATA_PATH = PATH.joinpath("../datasets").resolve()
f.to_csv(DATA_PATH.joinpath("statistics.csv"))



