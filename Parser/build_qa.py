from lxml import etree
from pathlib import Path
import csv, re

HTML_RE = re.compile('<.*?>')

def remove_html(_str):
    return re.sub(HTML_RE, '', _str)

def clean_text(_str):
    _str = remove_html(_str)
    return _str.replace("\r\n"," ").replace("\r"," ").replace("\n", " ").replace("\\", "")

tables = {
    "Comments": ["Id","PostId","Score","Text","CreationDate","UserDisplayName","UserId","ContentLicense"],
    "Posts": ["Id","PostTypeId","ParentId","AcceptedAnswerId","Score","Body","Title","Tags","AnswerCount","CommentCount","FavoriteCount"],
}

stackexchangefiles = ["{}.xml".format(table) for table in tables]

path = ".meta.stackexchange.com"
domain = "3dprinting"
full_path = domain+path

xmlfile = "{}\\{}".format(full_path, stackexchangefiles[1])

columns = tables["Posts"]

f = open("out.csv", 'w', newline='', encoding="utf-8")
w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
#w.writerow(columns)
l = []
l.append(columns)

context = etree.iterparse(xmlfile, events=('end',), tag='row')
for event, element in context:
    row=[clean_text(element.attrib[column]) if column in element.attrib else '' for column in columns]
    #w.writerow(row)
    l.append(row)

parentId_i = 2
Id_i = 0
title_i = 6
body_i = 5
score_i = 4

qa = {}

for i, row in enumerate(l):
    if i != 0:
        qa_pair = ["", ""]
        if row[parentId_i] == "":
            qa_pair[0] = row[title_i] + " " + row[body_i]
            qa[row[Id_i]] = qa_pair
        else:
            qa[row[parentId_i]][1] += row[body_i]

#print(qa)

w.writerow(["question", "answer"])

answer_length = []

for _qa in qa.items():
    w.writerow(_qa[1])
    answer_length.append(len(_qa[1][1]))
    
avg_len = sum(answer_length) / len(answer_length)
print(avg_len)
f.close()
