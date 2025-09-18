us_steel_prod=5_000_000
starty=1929
tons_truck=1
pct_truck=.3
trucks=pct_truck*us_steel_prod/tons_truck
end=1937
years=end-starty
truckes=0
pctrussia=.9
for i in range(starty,end):
	truckes+=trucks
russiatrucks=truckes*pctrussia
print("in 1937 russia had trucks ",russiatrucks)
pct_recycled=.4
today=russiatrucks*pct_recycled
print("today russia has ",today)
lendlease=300_000
print("lend elase was ", lendlease/russiatrucks," percent")