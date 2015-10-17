#!/usr/bin/env python
import environ
import os
from opinion.opinion_core.models import *
try:
    import json
except ImportError:
    import simplejson as json
import numpy
from opinion.includes.queryutils import *
import csv
datapath= settings.MEDIA_ROOT + "/mobile/stats_data/"

country_list={"USA":0,
"AFG":0,
"ALA":0,
"ALB":0,
"DZA":0,
"ASM":0,
"AND":0,
"AGO":0,
"AIA":0,
"ATA":0,
"ATG":0,
"ARG":0,
"ARM":0,
"ABW":0,
"AUS":0,
"AUT":0,
"AZE":0,
"BHS":0,
"BHR":0,
"BGD":0,
"BRB":0,
"BLR":0,
"BEL":0,
"BLZ":0,
"BEN":0,
"BMU":0,
"BTN":0,
"BOL":0,
"BES":0,
"BIH":0,
"BWA":0,
"BVT":0,
"BRA":0,
"IOT":0,
"BRN":0,
"BGR":0,
"BFA":0,
"BDI":0,
"KHM":0,
"CMR":0,
"CAN":0,
"CPV":0,
"CYM":0,
"CAF":0,
"TCD":0,
"CHL":0,
"CHN":0,
"CXR":0,
"CCK":0,
"COL":0,
"COM":0,
"COG":0,
"COD":0,
"COK":0,
"CRI":0,
"CIV":0,
"HRV":0,
"CUB":0,
"CUW":0,
"CYP":0,
"CZE":0,
"DNK":0,
"DJI":0,
"DMA":0,
"DOM":0,
"ECU":0,
"EGY":0,
"SLV":0,
"GNQ":0,
"ERI":0,
"EST":0,
"ETH":0,
"FLK":0,
"FRO":0,
"FJI":0,
"FIN":0,
"FRA":0,
"GUF":0,
"PYF":0,
"ATF":0,
"GAB":0,
"GMB":0,
"GEO":0,
"DEU":0,
"GHA":0,
"GIB":0,
"GRC":0,
"GRL":0,
"GRD":0,
"GLP":0,
"GUM":0,
"GTM":0,
"GGY":0,
"GIN":0,
"GNB":0,
"GUY":0,
"HTI":0,
"HMD":0,
"VAT":0,
"HND":0,
"HKG":0,
"HUN":0,
"ISL":0,
"IND":0,
"IDN":0,
"IRN":0,
"IRQ":0,
"IRL":0,
"IMN":0,
"ISR":0,
"ITA":0,
"JAM":0,
"JPN":0,
"JEY":0,
"JOR":0,
"KAZ":0,
"KEN":0,
"KIR":0,
"PRK":0,
"KOR":0,
"KWT":0,
"KGZ":0,
"LAO":0,
"LVA":0,
"LBN":0,
"LSO":0,
"LBR":0,
"LBY":0,
"LIE":0,
"LTU":0,
"LUX":0,
"MAC":0,
"MKD":0,
"MDG":0,
"MWI":0,
"MYS":0,
"MDV":0,
"MLI":0,
"MLT":0,
"MHL":0,
"MTQ":0,
"MRT":0,
"MUS":0,
"MYT":0,
"MEX":0,
"FSM":0,
"MDA":0,
"MCO":0,
"MNG":0,
"MNE":0,
"MSR":0,
"MAR":0,
"MOZ":0,
"MMR":0,
"NAM":0,
"NRU":0,
"NPL":0,
"NLD":0,
"NCL":0,
"NZL":0,
"NIC":0,
"NER":0,
"NGA":0,
"NIU":0,
"NFK":0,
"MNP":0,
"NOR":0,
"OMN":0,
"PAK":0,
"PLW":0,
"PSE":0,
"PAN":0,
"PNG":0,
"PRY":0,
"PER":0,
"PHL":0,
"PCN":0,
"POL":0,
"PRT":0,
"PRI":0,
"QAT":0,
"REU":0,
"ROU":0,
"RUS":0,
"RWA":0,
"BLM":0,
"SHN":0,
"KNA":0,
"LCA":0,
"MAF":0,
"SPM":0,
"VCT":0,
"WSM":0,
"SMR":0,
"STP":0,
"SAU":0,
"SEN":0,
"SRB":0,
"SYC":0,
"SLE":0,
"SGP":0,
"SXM":0,
"SVK":0,
"SVN":0,
"SLB":0,
"SOM":0,
"ZAF":0,
"SGS":0,
"SSD":0,
"ESP":0,
"LKA":0,
"SDN":0,
"SUR":0,
"SJM":0,
"SWZ":0,
"SWE":0,
"CHE":0,
"SYR":0,
"TWN":0,
"TJK":0,
"TZA":0,
"THA":0,
"TLS":0,
"TGO":0,
"TKL":0,
"TON":0,
"TTO":0,
"TUN":0,
"TUR":0,
"TKM":0,
"TCA":0,
"TUV":0,
"UGA":0,
"UKR":0,
"ARE":0,
"GBR":0,
"UMI":0,
"URY":0,
"UZB":0,
"VUT":0,
"VEN":0,
"VNM":0,
"VGB":0,
"VIR":0,
"WLF":0,
"ESH":0,
"YEM":0,
"ZMB":0,
"ZWE":0}

gender_dict={"m":0,"f":0,"NA":0}
#age_dict={"<15":0,"15-18":0,"19-22":0,"23-25":0,"26-30":0,"31-35":0,"36-40":0,"41-45":0,"46-50":0,"51-55":0,"56-60":0,">60":0,"NA":0}
age_list=[0,0,0,0,0,0,0,0,0,0,0,0,0] #follow the order above
year_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #total 17 categories


exclude_list=['goldberg@berkeley.edu','nonnecke@citris-uc.org','nonnecke@berkeley.edu','sanjay@eecs.berkeley.edu','goldberg@eecs.berkeley.edu','angelaslin@berkeley.edu','matti@example.com','patel24jay@gmail.com','ccrittenden@berkeley.edu','alisoncliff@berkeley.edu','alisoncliff@berkeley.edu','hunallen@gmail.com','hunallen@berkeley.edu']
user=User.objects.exclude(username__in=exclude_list).filter(is_active=True).order_by('id')
alluser=user[11:]
user_exclude=User.objects.filter(username__in=exclude_list)

#calculate number of students in each country
for user in alluser:
    country=UserData.objects.filter(user=user,key='country')
    if len(country)>0:
        country_val=country[0].value
        if (country_val!='-1' and country_val!=''):
            country_list[country_val]=country_list[country_val]+1

ofile  = open(settings.MEDIA_ROOT + "/mobile/stats_data/"+"country_student_r.csv", "wb")
writer=csv.writer(ofile,delimiter=',')
title=['ISO','fillKey','total']
writer.writerow(title)
for country in country_list:
    fillcolor=""
    if country_list[country]==0:
        fillcolor="0"
    elif (country_list[country]>0 and country_list[country]<=5):
        fillcolor="1-5"
    elif (country_list[country]>5 and country_list[country]<=10):
        fillcolor="6-10"
    elif (country_list[country]>10 and country_list[country]<=15):
        fillcolor="11-15"
    elif (country_list[country]>15 and country_list[country]<=20):
        fillcolor="16-20"
    elif (country_list[country]>20 and country_list[country]<=25):
        fillcolor="21-25"
    elif (country_list[country]>25 and country_list[country]<=30):
        fillcolor="26-30"
    else:
        fillcolor=">30"
    row=[country,fillcolor,country_list[country]]
    writer.writerow(row)


#calculate gender distribution
ofile_gender=open(settings.MEDIA_ROOT + "/mobile/stats_data/"+"gender_r.csv", "wb")
writer=csv.writer(ofile_gender,delimiter=',')
title=['gender','number']
writer.writerow(title)
for user in alluser:
    gender=UserData.objects.filter(user=user,key='gender')
    if len(gender)>0:
        gender_val=gender[0].value
        if (gender_val=='-1' or gender_val==''):
            gender_dict['NA']=gender_dict['NA']+1
        else:
            gender_dict[gender_val]=gender_dict[gender_val]+1

for gender in gender_dict:
    if gender=='m':
        row=["Male",gender_dict[gender]]
        writer.writerow(row)
    elif gender=='f':
        row=["Female",gender_dict[gender]]
        writer.writerow(row)
    else:
        row=["NA",gender_dict[gender]]
        writer.writerow(row)


#calculate age distribution
ofile_age=open(settings.MEDIA_ROOT + "/mobile/stats_data/"+"age_r.csv", "wb")
writer=csv.writer(ofile_age,delimiter=',')
title=['age','total']
writer.writerow(title)
for user in alluser:
    age=UserData.objects.filter(user=user,key='age')
    if len(age)>0:
        age_val=age[0].value
        if (age_val=='-1' or age_val==''):
            age_list[12]=age_list[12]+1
        else:
            age_val=int(age_val)
            if age_val<15:
                age_list[0]=age_list[0]+1
            elif (age_val>=15 and age_val<=18):
                age_list[1]=age_list[1]+1
            elif (age_val>=19 and age_val<=22):
                age_list[2]=age_list[2]+1
            elif (age_val>=23 and age_val<=25):
                age_list[3]=age_list[3]+1
            elif (age_val>=26 and age_val<=30):
                age_list[4]=age_list[4]+1
            elif (age_val>=31 and age_val<=35):
                age_list[5]=age_list[5]+1
            elif (age_val>=36 and age_val<=40):
                age_list[6]=age_list[6]+1
            elif (age_val>=41 and age_val<=45):
                age_list[7]=age_list[7]+1
            elif (age_val>=46 and age_val<=50):
                age_list[8]=age_list[8]+1
            elif (age_val>=51 and age_val<=55):
                age_list[9]=age_list[9]+1
            elif (age_val>=56 and age_val<=60):
                age_list[10]=age_list[10]+1
            else:
                age_list[11]=age_list[11]+1

#age_dict={"<15":0,"15-18":0,"19-22":0,"23-25":0,"26-30":0,"31-35":0,"36-40":0,"41-45":0,"46-50":0,"51-55":0,"56-60":0,">60":0,"NA":0}
for i in range(13):
    if i==0:
        row=["<15",age_list[i]]
        writer.writerow(row)
    elif i==1:
        row=["15-18",age_list[i]]
        writer.writerow(row)
    elif i==2:
        row=["19-22",age_list[i]]
        writer.writerow(row)
    elif i==3:
        row=["23-25",age_list[i]]
        writer.writerow(row)
    elif i==4:
        row=["26-30",age_list[i]]
        writer.writerow(row)
    elif i==5:
        row=["31-35",age_list[i]]
        writer.writerow(row)
    elif i==6:
        row=["36-40",age_list[i]]
        writer.writerow(row)
    elif i==7:
        row=["41-45",age_list[i]]
        writer.writerow(row)
    elif i==8:
        row=["46-50",age_list[i]]
        writer.writerow(row)
    elif i==9:
        row=["51-55",age_list[i]]
        writer.writerow(row)
    elif i==10:
        row=["56-60",age_list[i]]
        writer.writerow(row)
    elif i==11:
        row=[">60",age_list[i]]
        writer.writerow(row)
    else:
        row=["NA",age_list[i]]
        writer.writerow(row)



#calculate training years distribution
ofile_age=open(settings.MEDIA_ROOT + "/mobile/stats_data/"+"college_r.csv", "wb")
writer=csv.writer(ofile_age,delimiter=',')
title=['year','total']
writer.writerow(title)
for user in alluser:
    year=UserData.objects.filter(user=user,key='trainingYears')
    if len(year)>0:
        year_val=year[0].value
        if (year_val=='-1' or year_val==''):
            year_list[16]=year_list[16]+1
        else:
            year_val=int(year_val)
            if year_val==0:
                year_list[0]=year_list[0]+1
            elif year_val==1:
                year_list[1]=year_list[1]+1
            elif year_val==2:
                year_list[2]=year_list[2]+1
            elif year_val==3:
                year_list[3]=year_list[3]+1
            elif year_val==4:
                year_list[4]=year_list[4]+1
            elif year_val==5:
                year_list[5]=year_list[5]+1
            elif year_val==6:
                year_list[6]=year_list[6]+1
            elif year_val==7:
                year_list[7]=year_list[7]+1
            elif year_val==8:
                year_list[8]=year_list[8]+1
            elif year_val==9:
                year_list[9]=year_list[9]+1
            elif year_val==10:
                year_list[10]=year_list[10]+1
            elif year_val==11:
                year_list[11]=year_list[11]+1
            elif year_val==12:
                year_list[12]=year_list[12]+1
            elif year_val==13:
                year_list[13]=year_list[13]+1
            elif year_val==14:
                year_list[14]=year_list[14]+1
            else:
                year_list[15]=year_list[15]+1


for i in range(16):
    row=[i,year_list[i]]
    writer.writerow(row)

writer.writerow(["NA",year_list[16]])
