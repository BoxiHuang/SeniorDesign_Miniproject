import json
import ployly.plotly as py
import plotly.graph_objs as go
import plotly

plotly.tools.set_credentials_file(username='borishuang', api_key='NIbKvT2IQHAFDlfnRim0')


with open('data.json', 'r') as f:                #Need to change data.json file to link
    dict_file = json.load(f)

dict_temp = []
for x in dict_file:
    dict_temp = x['temp']

dict_humid =[]
for x in dict_file:
    dict_humid = x['humidity']

dict_time = []
for x in dict_file:
    dict_time = x['time']



trace0 = go.Scatter(
    x=dict_time,
    y=dict_temp
)

trace1 = go.Scatter(
    x=dict_time,
    y=dict_humid
)

data = [trace0, trace1]

layout = dict(title = 'Time vs Temperature & Humidity Sensor Data',
              xaxis = dict(title = 'Time'),
              yaxis = dict(title = 'Temperature (degrees F) & Humidity'),
              )

fig = dict(data=data, layout=layout)
py.plot(fig, filename = 'sensor_diagram', auto_open=True)
