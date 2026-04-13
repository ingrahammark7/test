import pandas as pd
import numpy as np
import math as ma

df=pd.read_csv('oil.csv')
years=df['Year'].values
prod=df['Production_mbd'].values
dif2=pd.DataFrame()
sd2=0
curs={}

def docur(pro,yea,curveset):
	curn=pd.DataFrame()
	datrr=0
	sder=0
	cum=pro[0]
	pc=pd.DataFrame()
	difs=pd.DataFrame()
	sumdif=0
	dif2e=pd.DataFrame()
	yed=0
	for i in range(1,len(yea)):
		cum=prod[i]+cum
		p=pro[i]
		pct=p/cum
		pc=np.append(pc,pct)
		ppct=pro[i-1]/cum
		dif=pct-ppct
		thr=ma.pow(ma.e,-ma.sqrt(i))
		thr=dif/thr
		if(datrr==0):
			if(thr<.5):
				yed=years[i]
				datrr=1
		else:
			dif2e=np.append(dif2e,dif)
			sder+=dif		
		difs=np.append(difs,dif)
		sumdif+=dif
	curveset[len(curveset)]=curn
	numef={}
	numef[0]=dif2e
	numef[1]=curveset
	numef[2]=sder
	numef[3]=yed
	numef[4]=sumdif
	return numef

numerf=docur(prod,years,curs)
dif2=numerf[0]
curs=numerf[1]
sd2=numerf[2]
yedf=numerf[3]
sdf=numerf[4]
dif2av=sd2/dif2.size
fo=.995*dif2.size
fo=int(fo)-1
fo=dif2[fo]
print(fo,sdf)