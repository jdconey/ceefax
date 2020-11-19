# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 09:41:41 2020

@author: Owner
"""
import cv2
import numpy as np
import time
import bs4
import urllib.request


#get current day and time for annotation
cur_day = time.strftime('%a %e %b',time.localtime())
cur_time = time.strftime('%H:%M/%S')
day = time.strftime('%A',time.localtime())
tmrw = time.strftime('%A',time.localtime(time.time()+86400))

#you need a Met Office API key thing.
keyt=open('/home/pi/weather/key.txt',"r")
key2=keyt.read()
keyt.close()


#get temperatures
cities={'Inverness':[352021,(530,135)],
        'Fort William':[324186,(500,240)],
       'Dumfries':[351271,(530,350)],
       'Belfast':[350347,(325,425)],
       'Kendal':[352071,(630,425)],
       'Manchester':[310013,(650,530)],
       'Leeds':[352241,(0,0)],
       'Edinburgh':[351351,(0,0)],
       'Stafford':[310141,(630,600)],
       'Cambridge':[310042,(800,640)],
       'London':[352409,(750,710)],
       'Exeter':[351425,(500,780)],
       'Cardiff':[371381,(500,680)]  
        }
temps=['Inverness','Fort William','Dumfries','Belfast','Kendal',
       'Manchester','Stafford','Cambridge','London','Exeter','Cardiff']

data={}

timeos=['midday','tonight','tomorrow']
desc={'midday':'Weather for Midday on '+str(day),
      'tonight':'Weather for '+str(day)+ ' night',
      'tomorrow':'Weather for Midday on '+str(tmrw)    
      }

today = time.strftime('%Y-%m-%d',time.localtime())
for city in cities:
    data[city]={}
    link = 'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/xml/'+str(cities[city][0])+'?res=3hourly&key='+key2
    webpage=str(urllib.request.urlopen(link).read())
    soup = bs4.BeautifulSoup(webpage,"lxml")
    by_line=webpage.split('>')
    i=0
    get=[]
    while i<len(by_line):
        if by_line[i]=='720</Rep':
            get.append(i)
        i=i+1
    get=sorted(get)
    ours=get[0]-1
    templine = by_line[ours]
    deets = templine.split(' ')
    i=0
    while i<len(deets):
        if deets[i].startswith('T='):
            temperature = deets[i]
            temperature = temperature[3:]
            temperature = temperature[:-1]
            
        if deets[i].startswith('W='):
            weather = deets[i]
            weather=weather[3:]
            weather=weather[:-1]
        i=i+1
    data[city]['midday']=[temperature,weather]
    
    
    ours=get[1]-1
    templine = by_line[ours]
    deets = templine.split(' ')
    i=0
    while i<len(deets):
        if deets[i].startswith('T='):
            temperature = deets[i]
            temperature = temperature[3:]
            temperature = temperature[:-1]
            
        if deets[i].startswith('W='):
            weather = deets[i]
            weather=weather[3:]
            weather=weather[:-1]
        i=i+1
    data[city]['tomorrow']=[temperature,weather]
    
    
    i=0
    get2=[]
    while i<len(by_line):
        if by_line[i]=='1260</Rep':
            get2.append(i)
        i=i+1
    get2=sorted(get2)
    ours=get2[0]-1
    templine = by_line[ours]
    deets = templine.split(' ')
    i=0
    while i<len(deets):
        if deets[i].startswith('T='):
            temperature = deets[i]
            temperature = temperature[3:]
            temperature = temperature[:-1]
            
        if deets[i].startswith('W='):
            weather = deets[i]
            weather=weather[3:]
            weather=weather[:-1]
        i=i+1
    data[city]['tonight']=[temperature,weather]

codes={
'NA':'Not available',
0:  'Clear',
1:  'Sunny',
2:  'Partly cloudy',
3:  'Partly cloudy',
4:  'Not used',
5:  'Mist',
6:  'Fog',
7:  'Cloudy',
8:  'Overcast',
9:  'Light rain shower',
10: 'Light rain shower',
11: 'Drizzle',
12: 'Light rain',
13: 'Heavy rain shower',
14: 'Heavy rain shower',
15: 'Heavy rain',
16: 'Sleet shower',
17: 'Sleet shower',
18: 'Sleet',
19: 'Hail shower',
20: 'Hail shower',
21: 'Hail',
22: 'Light snow shower',
23: 'Light snow shower',
24: 'Light snow',
25: 'Heavy snow shower',
26: 'Heavy snow shower',
27: 'Heavy snow',
28: 'Thunder shower',
29: 'Thunder shower',
30: 'Thunder',
31: 'Rain',
32: 'Wintry showers'
}


blocks={'Inverness':{72:list(np.linspace(499,529,3))+list(np.linspace(574,604,3)),
                     84:[424]+list(np.linspace(484,619,10)),
                     96:[409,424]+list(np.linspace(469,619,11)),
                     108:list(np.linspace(469,499,3))+[604],
                     120:[394,409,604]+list(np.linspace(454,499,4)),
                     132:list(np.linspace(454,499,4))+[394,424],
                     144:[379]+list(np.linspace(424,589,12)),
                     156:[379]+list(np.linspace(409,664,18)),
                     168:[379]+list(np.linspace(424,679,18)),                         
                     180:list(np.linspace(424,649,16)),
                     192:[409]+list(np.linspace(439,679,17))
                     },
       'Fort William':{204:list(np.linspace(424,529,8)),
                       216:[394]+list(np.linspace(424,469,4)),
                       228:[424,454,469],
                       240:[454,469],
                       252:list(np.linspace(439,529,7)),
                       264:list(np.linspace(424,529,8)),
                       276:list(np.linspace(424,529,8)),
                       288:list(np.linspace(439,529,7)),
                       300:list(np.linspace(424,529,8)),
                       312:list(np.linspace(424,529,8)),
                       324:[409,424]+list(np.linspace(454,499,4)),
                       336:[409,439,469,484,499],
                       348:[409]
                       },       
       'Kendal':{348:[484,499],
                 360:list(np.linspace(484,604,9)),
                 372:list(np.linspace(469,544,6))+list(np.linspace(574,604,3)),
                 384:list(np.linspace(454,529,6))+list(np.linspace(559,604,4)),
                 396:[454,469,499]+list(np.linspace(544,589,4)),
                 408:[469]+list(np.linspace(544,589,4)),
                 420:list(np.linspace(544,589,4)),
                 432:[469]+list(np.linspace(544,649,8)),
                 444:[454,469]+list(np.linspace(559,649,7)),
                 456:[454]+list(np.linspace(574,649,6))
                 },
       'Edinburgh':{204:list(np.linspace(544,664,9)),
                    216:list(np.linspace(574,664,7)),
                    228:list(np.linspace(574,649,6)),
                    240:list(np.linspace(574,649,6)),
                    252:list(np.linspace(544,634,7)),
                    264:list(np.linspace(544,604,5)),
                    276:list(np.linspace(544,634,7)),
                    288:list(np.linspace(544,634,7)),
                    300:list(np.linspace(544,604,5)),
                    312:list(np.linspace(544,634,7)),
                    324:list(np.linspace(604,664,5)),
                    336:list(np.linspace(604,679,6)),
                    348:list(np.linspace(604,679,6)),
                    360:list(np.linspace(619,679,5)),
                    372:list(np.linspace(619,679,5)),
                    384:list(np.linspace(619,694,6)),
                    396:[694,709],
                    408:[694,709],
                    420:[694,709],
                    432:list(np.linspace(664,724,5)),
                    444:list(np.linspace(664,724,5))            
                    },
       'Belfast':{360:[334,349],
                  372:list(np.linspace(304,364,5)),
                  384:list(np.linspace(274,379,8)),
                  396:list(np.linspace(259,289,3))+[394],
                  408:list(np.linspace(244,289,4))+[394],
                  420:list(np.linspace(259,289,3))+[394,409],
                  432:list(np.linspace(244,409,12)),
                  444:list(np.linspace(259,409,11)),
                  456:list(np.linspace(274,409,10)),
                  468:[289,304,364,379,394],
                  480:[304,349,364,379],
                  492:[379]
           },
       'Manchester':{468:list(np.linspace(604,649,4)),
                     480:list(np.linspace(589,649,5)),
                     492:list(np.linspace(604,649,4)),
                     504:[604,619],
                     516:[589,604,619],
                     528:[604,619,469],
                     540:[454,469]+list(np.linspace(544,649,8)),
                     552:list(np.linspace(469,649,13)),
                     564:list(np.linspace(469,649,13)),
                     576:list(np.linspace(454,589,10)),
                     588:[454]+list(np.linspace(484,589,8)),
                     600:list(np.linspace(499,589,7))
                     },
       'Leeds':{456:list(np.linspace(664,724,5)),
                468:list(np.linspace(664,754,7)),
                480:list(np.linspace(664,754,7)),
                492:list(np.linspace(664,769,8)),
                504:list(np.linspace(724,784,5)),
                516:list(np.linspace(724,799,6)),
                528:list(np.linspace(724,799,6)),
                540:list(np.linspace(664,799,10)),
                552:list(np.linspace(664,799,10))
           },
       'Cambridge':{564:list(np.linspace(664,799,10)),
                    576:list(np.linspace(694,784,7))+[829,844,859],
                    588:list(np.linspace(694,799,8))+[829,844,859,874],
                    600:list(np.linspace(694,889,14)),
                    612:list(np.linspace(679,769,7))+[874,889],
                    624:list(np.linspace(679,769,7))+[874,889],
                    636:list(np.linspace(679,769,7))+[874,889],
                    648:list(np.linspace(679,889,15))
           },
       'Cardiff':{612:list(np.linspace(499,664,12)),
                  624:list(np.linspace(499,664,12)),
                  636:list(np.linspace(499,664,12)),
                  648:list(np.linspace(574,664,7)),
                  660:[424,439,454,469]+list(np.linspace(574,664,7)),
                  672:[409,424,439,454,469]+list(np.linspace(574,664,7)),
                  684:[454]+list(np.linspace(499,559,5))+list(np.linspace(634,664,3)),
                  696:list(np.linspace(514,559,4))+list(np.linspace(619,664,4)),
                  708:list(np.linspace(619,664,4))
           },
       'London':{660:list(np.linspace(679,874,14)),
                 672:list(np.linspace(679,874,14)),
                 684:[679,694,709,829,844,859],
                 696:[679,694,709,829,844,859],
                 708:[679,694,709]+list(np.linspace(829,919,7)),
                 720:list(np.linspace(694,904,15)),
                 732:list(np.linspace(694,889,14)),
                 744:list(np.linspace(694,889,14)),
                 756:list(np.linspace(694,799,8)),
                 768:list(np.linspace(724,829,8)),
                 780:[694,709,814],
                 792:[709]
           },
       'Exeter':{720:list(np.linspace(514,679,12)),
                 732:list(np.linspace(514,679,12))+[484],
                 744:list(np.linspace(484,679,14)),
                 756:list(np.linspace(574,649,6)),
                 768:[439]+list(np.linspace(574,679,8)),
                 780:[439]+list(np.linspace(574,664,7)),
                 792:[454,469,529,544,559],
                 804:list(np.linspace(409,454,4))+[544],
                 816:[394,424]
                 
           }
       }

small={'Inverness':{108:[394,409],144:[409],180:[664,679]},
       'Belfast':{468:[349]},
       'Manchester':{468:[589],504:[589]},
       'Cardiff':{684:[574,589]},
       'London':{756:[814,829,844,859]},
       'Exeter':{756:[664,679],792:[424,439]}
       }

for period in timeos:
    connies=[]
    groups={}
    for city in blocks:
        if data[city][period][1] not in connies:
            connies.append(data[city][period][1])
            groups[data[city][period][1]]=[city]
        else:
            groups[data[city][period][1]].append(city)
    if len(connies)>4:
        if '2' in connies and '3' in connies:
                connies.remove(2)
                for city4 in blocks:
                    if data[city4][period][1]=='2':
                        data[city4][period][1]='3'
        if len(connies)>4:
            if '3' in connies and '7' in connies:
                connies.remove('3')
                for city4 in blocks:
                    if data[city4][period][1]=='3':
                        data[city4][period][1]='7'
        if len(connies)>4:
            if '5' in connies and '6' in connies:
                connies.remove('5')
                for city4 in blocks:
                    if data[city4][period][1]=='5':
                        data[city4][period][1]='6'
        if len(connies)>4:
            light_rain=['9','10','11','12']
            score=0
            for k in connies:
                if k in light_rain:
                    score=score+1
            if score>1:
                if '9' in connies:
                    connies.remove('9')
                if '10' in connies:
                    connies.remove('10')
                if '11' in connies:
                    connies.remove('11')
                for city4 in blocks:
                    if data[city4][period][1] in light_rain:
                        data[city4][period][1] = '12'
        if len(connies)>4:
            heavy_rain=['13','14','15']
            score=0
            for k in connies:
                if k in heavy_rain:
                    score=score+1
            if score>1:
                if '13' in connies:
                    connies.remove('13')
                if '14' in connies:
                    connies.remove('14')
                for city4 in blocks:
                    if data[city4][period][1] in heavy_rain:
                        data[city4][period][1] = '15'
        if len(connies)>4:
            if '12' in connies and '15' in connies:
                connies.remove('12')
                connies.remove('15')
                connies.append('31')
                for city4 in blocks:
                    if data[city4][period][1] in ['12','15']:
                        data[city4][period][1]='31'
        if len(connies)>4:
            wintry = ['31','16','17','19','20','22','23','24','25','26']
            score=0
            for k in connies:
                if k in wintry:
                    score=score+1
                
            if score>1:
                for l in wintry:
                    if l in connies:
                        connies.remove(l)
                connies.append('32')
            
   
     #   print(groups)
    img = cv2.imread('/media/pi/D608-D7E6/ceefax_base/0.jpg')
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(img,'401 CEEFAX 1     401',(0,26),font, 2, (255,255,255),2,cv2.LINE_AA)
    cv2.putText(img,cur_day,(600,26),font,2,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img,cur_time,(1000,26),font,2,(0,255,255),2,cv2.LINE_AA)
    
    cv2.putText(img,desc[period],(350,60),font,2,(255,255,255),2,cv2.LINE_AA)
    
    cv2.putText(img,'Data: The Met Office',(400,855),font,2,(255,255,255),2,cv2.LINE_AA)


    for city2 in temps:
         cv2.putText(img,str(data[city2][period][0]),cities[city2][1],font,2,(255,255,255),2,cv2.LINE_AA)
    colours=[(0,255,0),(255,0,255),(255,255,0),(0,255,255)]
    posns= [(0,400),(0,250),(0,200),(0,750)]
    i=0
    words=[]
    posy={}
    while i<len(connies):
        words.append(connies[i])
        i=i+1
    for city3 in blocks:
        j=0
        while j<len(connies):
            if city3 in groups[connies[j]]:
                cx=colours[j]
                if cx not in posy.keys():
                    posy[cx]=[]
                posy[cx]=posy[cx]+list(blocks[city3].keys())


            j=j+1
        for y in blocks[city3]:
            for x in blocks[city3][y]:
                img=cv2.rectangle(img,(int(x),y),(int(x)+11,y+8),cx,-1)
        if city3 in small:
            for y in small[city3]:
                for x in small[city3][y]:
                    img=cv2.rectangle(img,(int(x),y),(int(x)+11,y+5),cx,-1)
        
        
    ab=0
    while ab<len(connies):
        diff=connies[ab]
        posns[ab]=(0,int(np.mean(posy[colours[ab]])))
     #   print(colours[ab])
     #   print(posy[colours[ab]])

        cv2.putText(img,codes[int(diff)],posns[ab],font,2,colours[ab],2,cv2.LINE_AA)
        ab=ab+1

    i=1
    while i<len(posns):
        j=0
        while j<i:
            if abs(posns[i][1]-posns[j][1])<30:
                posns[i] = (0, posns[i][1]+35)
            j=j+1
        i=i+1
