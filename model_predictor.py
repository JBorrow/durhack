import datapoint as dp
import numpy as np
import yaml
import footfall_model as fm

conn = dp.connection(api_key="a1e2dddc-6528-496b-89ba-39bdaca995cc")

for site in conn.get_all_sites():
    if site.name == "Durham":
        break

forecast = conn.get_forecast_for_site(site.id, "3hourly")

output = []
streets = [['ss', 'Silver Street'], ['eb', 'Elvet Bridge']]
fake_streets = [['x', 'Street X'], ['y', 'Street Y'], ['z', 'Street Z']]

for i, street in enumerate(streets):
    output.append( {'name': street[1], 'id': street[0]})
    output[i]['days'] = []
    for j, day in enumerate(forecast.days):
        dayn = day.date.strftime("%A")
        day_number_in_year = int(day.date.strftime("%j"))
        output[i]['days'].append({'dayname': dayn})

        output[i]['days'][j]['temp'] = float(day.timesteps[4].temperature.value)
        output[i]['days'][j]['desc'] = day.timesteps[4].weather.text
        if street[0] == 'ss':
            op = fm.footfall_model(fm.ss16, day_number_in_year)
        if street[0] == 'eb':
            op = fm.footfall_model(fm.eb16, day_number_in_year)
        output[i]['days'][j]['footfall'] = float(op[0])
        output[i]['days'][j]['modifier'] = float(op[1])

    
with open('web/data/streets.yml', 'w') as outfile:
    yaml.dump(output, outfile)
