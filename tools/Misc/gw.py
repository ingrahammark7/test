airmass=10
thermvel=500
avogadkg=6e26
pm=2e-8
numpm=airmass/pm
direc=numpm**(1/3)
aireng=.5*(thermvel**2)*airmass
print(aireng,"air has 1mj available")
humpow=10000
airdens=1
airvol=airmass/airdens
enlen=airvol**(1/3)
print(enlen,"rough engine length")
dirvel=thermvel**(1/3)
print(dirvel,"directiinal speed")
hz=dirvel/enlen
print(hz,"system frequency")
poww=hz*aireng
print(poww,"engine power rate")
htco=1
airtemp=(aireng/1000)/airmass
print(airtemp,"eng temp")
htl=htco*(enlen**2)*6*airtemp
print(htl,"heat loss")

humanpow=9.81*100*1
print("a 100kg hunan standing watts",humanpow)
mutlfortorsothigh=2**3
humanpow*=mutlfortorsothigh
print(humanpow,"with loss")

numpmvol=airdens/pm
mfp=numpmvol**(1/3)
mfp=1/mfp
print(mfp,"mean free path of air grains")
gren=pm*(thermvel**2)*.5
af=gren*mfp
print(af,"torque force of free air")
#a 1 gram piston moving at 1m/s overcomes air torque

humhz=1
humlen=1
humt=(humanpow/humhz)*humlen
print(humt,"human torque")
engw=5000
engs=1
enghz=1
englen=engs/enghz
engpow=((engs**2)*enghz)*engw*.5
engt=(engpow/enghz)*englen
print(engt,"torque of massive marine engine for comparison")