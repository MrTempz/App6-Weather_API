from flask import Flask, render_template
import pandas as pd
from os import path

app = Flask(__name__)

stations_info_file = path.join('data_small', 'stations.txt')
stations = pd.read_csv(stations_info_file, skiprows=17)
stations =stations[['STAID','STANAME                                 ','CN']]

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())
    
@app.route("/api/v1/<station>/<date>")
def about(station, date):
    station_data_file = path.join('data_small', 
        f'TG_STAID{str(station).zfill(6)}.txt')
    df = pd.read_csv(station_data_file, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {'station': station,
            'date': date,
            'temperature': temperature}

@app.route("/api/v1/<station>")
def all_data(station):
    station_data_file = path.join('data_small', 
        f'TG_STAID{str(station).zfill(6)}.txt')
    df = pd.read_csv(station_data_file, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient='records')
    return result

@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    station_data_file = path.join('data_small', 
        f'TG_STAID{str(station).zfill(6)}.txt')
    df = pd.read_csv(station_data_file, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    df = df[df['    DATE'].str.startswith(str(year))]
    result = df.to_dict(orient='records')
    return result

if __name__ == '__main__':
     app.run(debug=True)