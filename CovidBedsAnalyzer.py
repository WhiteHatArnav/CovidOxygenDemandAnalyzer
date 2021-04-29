import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import rcParams
import plotly.express as px

Hosp_df = pd.read_csv('HospitalBedsIndia.csv')
Cases_df = pd.read_csv('StatewiseNewCases2.csv')
AbbStateList = pd.read_csv('StateList2.csv')
rAdm = 0.2
rICU = 0.05

TotalActiveCases = 3084814 
NewCases = Cases_df.loc[:,'Cases'].astype(int)
NewC = NewCases.values
Total = sum(NewC)
Proportions  = NewCases/Total

Admissions = round(Cases_df['Cases'] * rAdm)
ICUAdm = round(Cases_df['Cases'] * rICU)

OccupiedHospBeds = Proportions * rAdm * TotalActiveCases
OccupiedICUBeds = Proportions * rICU * TotalActiveCases

Output_df = pd.DataFrame()
Output_df['State'] = Hosp_df['State']
Output_df['Occupied ICU Beds']  = OccupiedICUBeds
Output_df['Occupied Hospital Beds']  = OccupiedHospBeds
Output_df['Hospital Beds'] = Hosp_df['Public Hospital Beds'] + Hosp_df['Private Hospital Beds'] 
Output_df['ICU Beds'] = Hosp_df['Public ICU Beds'] + Hosp_df['Private ICU Beds'] 
Output_df ['Admissions'] = Admissions
Output_df['Expected Daily ICU Admissions'] = ICUAdm
Output_df['Current Expected Surplus Beds']  = Output_df['Hospital Beds'] - OccupiedHospBeds
Output_df['Current Expected Surplus/Deficit of ICU Beds']  = Output_df['ICU Beds'] - OccupiedICUBeds


Output_df.to_csv("IndiaHospitalBedsSummary.csv")

#Output_df.loc = Output_df['Current Surplus ICU Beds' <= 0, 'ColorScale'] == 'Reds'
#Output_df.loc = Output_df['Current Surplus ICU Beds' <= 0, 'ColorScale'] == 'Blues'

print("Nationwide Surplus of Hospital Beds:")
print(int(sum(Output_df['Current Expected Surplus Beds'])))

print("Nationwide Shortage of ICU Beds:")
print(-(int(sum(Output_df['Current Expected Surplus/Deficit of ICU Beds']))))


fig = px.choropleth(
    Output_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color= 'Current Expected Surplus/Deficit of ICU Beds',
    color_continuous_scale='rdbu',
    color_continuous_midpoint = 0
)




fig.update_geos(fitbounds="locations", visible=False)
fig.show()

fig = px.choropleth(
    Output_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Expected Daily ICU Admissions',
    color_continuous_scale='Reds',
)

fig.update_geos(fitbounds="locations", visible=False)
fig.show()

Output_df['State'] = AbbStateList['State']
pl = Output_df.plot.bar(x="State", y = 'Expected Daily ICU Admissions')
pl.set_title("Expected Daily ICU Admissions by State in India, April 29th 2021")
pl.get_figure().tight_layout()
plt.show()

pl = Output_df.plot.bar(x="State", y = 'Current Expected Surplus/Deficit of ICU Beds')
pl.set_title("Current Expected Surplus/Deficit of ICU Beds by State in India, April 29th 2021")
pl.get_figure().tight_layout()
plt.show()






