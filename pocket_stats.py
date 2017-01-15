import sys
import json
import requests
import numpy as np
# import matplotlib.pyplot as plt
from config import consumer_key, access_token, redirect_uri


def get_pocket_data():	
	access_data = { "consumer_key": consumer_key,
					"access_token": access_token,
					"detailType":"simple",
					"sort":"newest"
					}

	#headers = {"content-type":"application/json"}	#No need to feed headers (gives error). requests lib takes care of it.

	pocket_response = requests.post("https://getpocket.com/v3/get",
						data = access_data)
	
	if pocket_response.status_code == 200:
		return pocket_response.json()
	else:
		return None
	

json_data = get_pocket_data()
if json_data is None: #Exit the program
	print "Invalid response. Exiting program..."
	sys.exit(0)


#Write json data to a text file, if needed
#file = open('pocket_stats.txt','w')	#File is created
#file.write(str(json_data))
#file.close()	#Close the file after data is written

items_list = json_data["list"]	#Listing of all the items

keys = items_list.keys()	#array of item keys

total_items = len(keys)		#Total no of saved items
print "Total number of saved items is:", total_items

word_count = np.zeros(total_items)

#To pull out any index number
for i in range(0,total_items):
	word_count[i] = items_list[keys[i]]["word_count"]
	print "+ " + items_list[keys[i]]["resolved_title"]


#Word count analysis
less_than_1000 = 0		#initialization
between_1000_3000 = 0
between_3000_5000 = 0
over_5000= 0

for x in range(0,len(word_count)):
	if word_count[x] < 1000:
		less_than_1000 += 1
	elif word_count[x] < 3000:
		between_1000_3000 += 1
	elif word_count[x] < 5000:
		between_3000_5000 += 1
	else:
		over_5000 += 1

labels = 'less than 1000 words','between 1000-3000 words', 'between 3000-5000 words', 'over 5000 words'
sizes = [less_than_1000, between_1000_3000, between_3000_5000, over_5000]
plt.pie(sizes,labels = labels, autopct = '%1.1f%%', shadow = True, startangle = 140)
plt.axis('equal')
plt.title('Articles according to word count.')
plt.show()		#Plotting of the Pie chart