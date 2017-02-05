import sys
import json
import requests
import numpy as np
from flask import Flask, make_response
from flask import render_template

from flask import Flask
app = Flask(__name__)

from config import consumer_key, access_token, redirect_uri

@app.route("/")
def hello():
    resp = get_pocket_data()
    return render_template('index.html', data=resp)

def get_pocket_data():	
	access_data = { "consumer_key": consumer_key,
					"access_token": access_token,
					"detailType":"simple",
					"sort":"newest"
					}

	#headers = {"content-type":"application/json"}	#No need to feed headers (gives error). requests lib takes care of it.

	pocket_response = requests.post("https://getpocket.com/v3/get",
						data = access_data)
	
	if pocket_response.status_code != 200:
		print "No response from API"
		return None
	
	else:
		json_data = pocket_response.json()
		if json_data is None: #Exit the program
			print "Invalid response. Exiting program..."
			sys.exit(0)

		items_list = json_data["list"]	#Listing of all the items

		keys = items_list.keys()	#array of item keys

		total_items = len(keys)		#Total no of saved items
		print "Total number of saved items is:", total_items

		word_count = np.zeros(total_items)

		#To pull out any index number
		for i in range(0,total_items):
			word_count[i] = items_list[keys[i]]["word_count"]
			# print "+ " + items_list[keys[i]]["resolved_title"]

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


		data = {}
		data.update({'less than 1000 words' : less_than_1000})
		data.update({'between 1000-3000 words' : between_1000_3000})
		data.update({'between 3000-5000 words' : between_3000_5000})
		data.update({'over 5000 words' : over_5000})

		return data

if __name__ == '__main__':
	app.run(debug=True)