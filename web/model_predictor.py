import datapoint as dp
import numpy as np
import json

def model(x, street):
    return x

conn = dp.connection(api_key="a1e2dddc-6528-496b-89ba-39bdaca995cc")

for site in conn.get_all_sites():
    if site.name == "Durham":
        break

forecast = conn.get_forecast_for_site(site.id, "3hourly")

output = {}
streets = [['ss', 'Silver Street'], ['x', 'Street X'], ['y', 'Street Y'], ['z', 'Street Z']]

for day in forecast.days:
    # midday
    dayn = day.date.strftime("%A")
    output[dayn] = {}
    output[dayn]['temp'] = float(day.timesteps[4].temperature.value)
    output[dayn]['desc'] = day.timesteps[4].weather.text

    for street in streets:
        output[dayn][street[0]] = {'name': street[1]}
        output[dayn][street[0]]['footfall'] = model(5000*float(np.random.rand(1)), street)
        output[dayn][street[0]]['modifier'] = model(float(np.random.rand()), street)

    
with open('data/streets.json', 'w') as outfile:
    json.dump(output, outfile)
