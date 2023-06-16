from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
import requests
from datetime import datetime, timedelta

#----Weather api-----
url_w = "https://weatherapi-com.p.rapidapi.com/forecast.json"
headers_w = {
	"X-RapidAPI-Key": "f5fad11093msh2681d2cd76ba7d1p1dc47ejsn873cec1bd25b",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

#----Date----
current_date = datetime.now()
date = []
date_mod = []
for i in range(0, 4):
	day = current_date + timedelta(days=i)
	date.append(day)
	day_mod = day.strftime("%A %d/%b")
	date_mod.append(day_mod)

weat_data = {
	'temp':[],
	'wind':[],
	'text':[],
	'icon':[],
	'precip':[],
	'hum':[]
}

#----Call 4 times----
for i in range (0,4):
	querystring = {"q":"Bangkok","dt":date[i]}
	response = requests.get(url_w, headers=headers_w, params=querystring)
	x=response.json()

	cur_con = x["forecast"]['forecastday'][0]['day']
	# ----Temp(C)----
	temp_cur = cur_con['maxtemp_c']
	weat_data['temp'].append(temp_cur)
	# ----Wind(kph)----
	wind_cur = cur_con['maxwind_kph']
	weat_data['wind'].append(wind_cur)
	# ----Condition-----
	text_con = cur_con['condition']['text']
	weat_data['text'].append(text_con)
	# -----Icon-----
	icon_cur = cur_con['condition']['icon']
	weat_data['icon'].append(icon_cur)
	# -----Precipitation-----
	precip_cur = cur_con['totalprecip_mm']
	weat_data['precip'].append(precip_cur)
	# -----Humidity-----
	hum_cur = cur_con['avghumidity']
	weat_data['hum'].append(hum_cur)


#--------News api-------------------------
news_data = {
	'title':[],
	'url':[],
	'description':[],
	'image':[]
}
url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"
querystring = {"q":"Thailand","pageNumber":"1","pageSize":"10","autoCorrect":"true","fromPublishedDate":"null","toPublishedDate":"null"}
headers = {
	"X-RapidAPI-Key": "f5fad11093msh2681d2cd76ba7d1p1dc47ejsn873cec1bd25b",
	"X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
news = response.json()
for i in range(0,4):
	news_data['title'].append(news['value'][i]['title'])
	news_data['url'].append(news['value'][i]['url'])
	news_data['description'].append(news['value'][i]['description'])
	news_data['image'].append(news['value'][i]['image']['url'])

#----Manga----
url = "https://api.npoint.io/e6738e461eee48f67b43/Manga/"
response = requests.get(url)
y=response.json()
manga = {
	'title':[],
	'url':[],
	'img':[],
	'description':[],
}
for i in range(0,4):
	manga['title'].append(y[f'{i}']['title'])
	manga['url'].append(y[f'{i}']['url'])
	manga['description'].append(y[f'{i}']['description'])
	manga['img'].append(y[f'{i}']['img'])


#----Web--------
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html',date=date_mod,weather=weat_data, news=news_data, manga=manga)

if __name__ == "__main__":
    app.run(debug=True)
