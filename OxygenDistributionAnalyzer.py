import pandas as pd
import numpy as np
import plotly.express as px


OxyProd_df = pd.read_csv(r'OxygenProductionIndia.csv')
OxyDemand_df = pd.read_csv(r'OxygenNeed.csv')


OxySurplus = OxyProd_df['Oxygen Produced (Tonnes)'] - OxyDemand_df['Oxygen Needed Daily(tonnes)']

Output_df = pd.DataFrame()
Output_df['State'] = OxyProd_df['State']
Output_df['Surplus Oxygen (Tonnes)'] = OxySurplus

print(Output_df)

# Mapping the Oxygen surplus data by state
## Source for Basis of mapping and Geojson of mapping Script: https://gist.githubusercontent.com/jbrobst






    
fig = px.choropleth(
    Output_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Surplus Oxygen (Tonnes)',
    color_continuous_scale='rdbu',
    title = "Formulated Surplus(Blue) and Deficit(Red) of Oxygen by State in India, April 2021" 
)

fig.update_geos(fitbounds="locations", visible=False)
fig.show()