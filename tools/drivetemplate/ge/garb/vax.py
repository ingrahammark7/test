import numpy as np

#vax death model
#leukemia has a 10y asymptomatic period
pop=200_000_000
power=6
year=10
start=2022
years=np.array([])
deaths=np.array([])


for x in range(year):
	vall = x/year
	pow=vall**power
	res=pop*pow
	cur=start+x
	np.append(years,cur)
	np.append(deaths,res)
	print(" in year " , cur , " there will be " , res  ," vax deaths")