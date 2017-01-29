import datapoint as dp
import numpy as np
import yaml

def model(x, street):
    return x

conn = dp.connection(api_key="a1e2dddc-6528-496b-89ba-39bdaca995cc")

for site in conn.get_all_sites():
    if site.name == "Durham":
        break

forecast = conn.get_forecast_for_site(site.id, "3hourly")

output = {}
streets = [['ss', 'Silver Street'], ['x', 'Street X'], ['y', 'Street Y'], ['z', 'Street Z']]

for street in streets:
    output[street[0]] = {'name': street[1]}
    for day in forecast.days:
        dayn = day.date.strftime("%A")
        output[street[0]][dayn] = {}
        output[street[0]][dayn]['temp'] = float(day.timesteps[4].temperature.value)
        output[street[0]][dayn]['desc'] = day.timesteps[4].weather.text

        output[street[0]][dayn]['footfall'] = model(5000*float(np.random.rand(1)), street)
        output[street[0]][dayn]['modifier'] = model(float(np.random.rand()), street)


    
with open('data/streets.yml', 'w') as outfile:
    yaml.dump(output, outfile)
