import pen
import nuct 
import thull

class tankin:
	def __init__(self):
		co=5
		self.cf={}
		for i in range (co):
			t=thull.baseobj()
			t.x=i
			t.y=0
			self.cf[i]=t		
		t=thull.baseobj()
		f1=t.turn(90)
		
tt=tankin()
print(tt.cf)
		
	