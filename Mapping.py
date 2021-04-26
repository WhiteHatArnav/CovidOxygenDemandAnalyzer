import pandas as pd
import plotly.express as px

# Source for basis of mapping Script: https://gist.github.com/jbrobst
df = pd.read_csv(r"C:\Users\Arnav Joshi\OxygenNeed.csv")

fig = px.choropleth(
    df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Oxygen Needed Daily(tonnes)',
    color_continuous_scale='Blues'
)

fig.update_geos(fitbounds="locations", visible=False)

fig.show()