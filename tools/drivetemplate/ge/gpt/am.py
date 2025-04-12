import math

glassairheattransferpercm2perk=0.0005
plasticairheattransferpercm2perk=0.0005
r27width=20
amraamwidth=17
r27front=r27width**2
amfront=amraamwidth**2
airdensgperm3= 1000
hvlcm=1
r27frontvol=r27front*hvlcm
amfrontvol=hvlcm*amfront
r27massg=175000
ammassg=150000
fuelpercent=.9
r27fuel=fuelpercent*r27massg
amfuel=ammassg*fuelpercent
enerdensjperg=35000
oxpercent=.8
resper=1-oxpercent
r27fuel=r27fuel*resper
amfuel=amfuel*resper
r27en=r27fuel*enerdensjperg
amen=amfuel*enerdensjperg
glassmeltc=1500
plasticmeltc=300
glassspecheatjpergperk=1
plasticspecheatjpergperk=1
r27maxenpercm2=glassspecheatjpergperk*glassmeltc*hvlcm
ammaxenpercm2=plasticspecheatjpergperk*plasticmeltc*hvlcm
heatpersecpercm2r27=glassairheattransferpercm2perk*glassmeltc*hvlcm
heatpersecpercm2am=plasticairheattransferpercm2perk*plasticmeltc*hvlcm
airpersecr27kg=math.sqrt(heatpersecpercm2r27*2)
airpersecamkg=math.sqrt(heatpersecpercm2am*2)
airdenskgpercm3=airdensgperm3/1000000
airvolpersr27=(airpersecr27kg/airdenskgpercm3)
airpersam=(airpersecamkg/airdenskgpercm3)
r27ms=airvolpersr27
amms=airpersam

print(f"r27 ", r27ms)
print("amraam max speed ", amms)