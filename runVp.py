import pandas as pd

data = pd.read_csv("VprokData.csv")

for i in range(len(data)):
	if list(data['Name']).count(data['Name'][i]) > 1:
		data.drop(i, inplace=True)
		print(i)

print(len(data))
data.to_csv("DataVprok.csv", index=None)
