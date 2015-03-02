#!/usr/bin/env python
import json

f = open('states.csv','rb')
line = f.readline()
out = {}
while line != "":
	comps = line.split()
	id = comps[0]
	name = " ".join(comps[1:len(comps)]).strip()
	out[id] = name
	line = f.readline()

#print json.dumps(out)

out2 = {}
for i in out:
	out2[i] = []

f = open('municipalities.csv','rb')
line = f.readline()
while line != "":
        comps = line.split()
        id = comps[0]
	id2 = comps[1]
        name = " ".join(comps[2:len(comps)]).strip()
        out2[id].append([id2,name])
        line = f.readline()

#print json.dumps(out2)


out3 = {}
for i in out:
	for j in out2[i]:
		out3[i + " "+ j[0]] = []

f = open('neighborhoods.csv','rb')
line = f.readline()
while line != "":
        comps = line.split()
        id = comps[0]
        id2 = comps[1]
        id3 = comps[2]
        name = " ".join(comps[3:len(comps)]).strip()
	key = id + " " + id2
	if key in out3:
        	out3[key.strip()].append([id3,name])
        line = f.readline()

print json.dumps(out3)

