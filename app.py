from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

API_KEY = '4c11e8ca0705fc64a4e8b0885e46dc7e'

# HTML + CSS (Frontend)
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Weather App 🌤️</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #74ABE2, #5563DE);
            color: white;
            text-align: center;
            padding-top: 100px;
        }
        input {
            padding: 10px;
            border-radius: 10px;
            border: none;
            width: 250px;
            text-align: center;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            background-color: #FFD700;
            color: black;
            font-weight: bold;
            cursor: pointer;
        }
        .weather-box {
            margin-top: 30px;
            padding: 20px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.2);
            display: inline-block;
        }
    </style>
</head>
<body>
    <h1>🌦 Weather App</h1>
    <form method="POST">
        <input type="text" name="city" placeholder="Enter city name" required>
        <button type="submit">Check Weather</button>
    </form>

    {% if weather %}
    <div class="weather-box">
        <h2>{{ weather['city'] }}</h2>
        <p>🌤 {{ weather['description'] }}</p>
        <p>🌡 Temperature: {{ weather['temp'] }}°C</p>
        <p>💧 Humidity: {{ weather['humidity'] }}%</p>
        <p>💨 Wind: {{ weather['wind'] }} m/s</p>
    </div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                'city': city.title(),
                'description': data['weather'][0]['description'],
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed']
            }
        else:
            weather = {'city': 'Not Found', 'description': 'Invalid city name!', 'temp': '-', 'humidity': '-', 'wind': '-'}

    return render_template_string(HTML_PAGE, weather=weather)

if __name__ == '__main__':
    app.run(debug=True)
