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

output = []
streets = [['ss', 'Silver Street'], ['x', 'Street X'], ['y', 'Street Y'], ['z', 'Street Z']]

for i, street in enumerate(streets):
    output.append( {'name': street[1], 'id': street[0]})
    output[i]['days'] = []
    for j, day in enumerate(forecast.days):
        dayn = day.date.strftime("%A")
        output[i]['days'].append({'dayname': dayn})

        output[i]['days'][j]['temp'] = float(day.timesteps[4].temperature.value)
        output[i]['days'][j]['desc'] = day.timesteps[4].weather.text

        output[i]['days'][j]['footfall'] = model(5000*float(np.random.rand(1)), street)
        output[i]['days'][j]['modifier'] = model(float(np.random.rand()), street)


    
with open('data/streets.yml', 'w') as outfile:
    yaml.dump(output, outfile)
