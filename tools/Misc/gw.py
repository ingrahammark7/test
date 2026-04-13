h1bbase=85000
nonwage=h1bbase*1.5
stock=nonwage*4
contractor=stock*3
revenue={"google":[400e9,200e3,.32],"meta":[200e9,75e3,.34],"apple":[420e9,170e3,.27],"amazon":[716e9,400e3,.1],"nflx":[45e9,16e3,.24]}
for i in revenue:
	re=revenue[i]
	rme=re[0]
	em=re[1]
	cost=contractor*em
	rep=cost/rme
	pro=1-rep
	pp=re[2]
	print(i,"estimated profit ",pro, "actual",pp)