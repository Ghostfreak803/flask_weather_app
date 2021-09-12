from flask import Flask, render_template, redirect, request
import requests
import json

app = Flask(__name__)
weather_api = ''
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':

        # get the country code from restcountries.eu API
        country_name = request.form['countryname']
        r = requests.get(f'https://restcountries.eu/rest/v2/name/{country_name}', params={'fields': 'alpha2Code', 'fullText': 'true'})
        json_data = json.loads(r.text)
        country_code = json_data[0]['alpha2Code'] 

        # get the weather data from openweather api
        if request.form['radio'] == 'cityname':
            city_data = request.form['location']
            weather_request = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_data}&appid={weather_api}')
            if weather_request.ok: #no errors in the response
                json_data = json.loads(weather_request.text)
                return render_template('result.html', data=json_data)

        elif request.form['radio'] == 'zip':
            city_data = request.form['location']
            weather_request = requests.get(f'https://api.openweathermap.org/data/2.5/weather?zip={city_data},{country_code}&appid={weather_api}')
            if weather_request.ok: #no errors in response
                json_data = json.loads(weather_request.text)
                return render_template('result.html', data=json_data)



if __name__ == ('__main__'):
    app.run(debug=True)

