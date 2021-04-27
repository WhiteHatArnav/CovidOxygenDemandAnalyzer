import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

OxyProd_df = pd.read_csv('OxygenProductionIndia.csv')
OxyDemand_df = pd.read_csv('OxygenNeed.csv')
StateList= pd.read_csv('StateList2.csv')


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

Output_df['State'] = StateList['State']
pl = Output_df.plot.bar(x="State")
pl.set_title("Bar Chart of Expected Local Deficit and Surplus of Oxygen in Indian States")
pl.get_figure().tight_layout()
plt.show()