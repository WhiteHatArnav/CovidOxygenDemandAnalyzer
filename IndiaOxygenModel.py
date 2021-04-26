
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import plotly.express as px


# input variables
MassOxProdDaily = 7100 #tonnes
VolOxyReqPerson = 550 # liters
nDailyCasesToday = 350000
rHosp = 0.060
rOxSup = 0.04
rICU = 0.02
rLtoTn = 0.00114
df = pd.read_csv(r'StatewiseNewCases.csv')
StateList= pd.read_csv('StateList.csv')

#initial formulations
NewCases = df.loc[:,'New Cases'].astype(int)
NewC = NewCases.values
Total = sum(NewC)
Proportions  = NewCases/Total
df['Proportions'] = Proportions
ltoTnConv = VolOxyReqPerson * rLtoTn
df['Oxygen Needed Daily(tonnes)'] = Proportions * nDailyCasesToday * rOxSup * ltoTnConv




# primary output variables (direct formulation)
nDailyOxSupNeed = int(rOxSup * nDailyCasesToday)
massOxSupNeed = nDailyOxSupNeed * VolOxyReqPerson * rLtoTn
massDailyOxyBacklog = max(massOxSupNeed-MassOxProdDaily, 0)
nPeopleBacklog = round(massDailyOxyBacklog/ltoTnConv)


# text Output
print("Number of people who need O2:")
print(nDailyOxSupNeed)
print("Volume Needed in Tonnes:")
print(massOxSupNeed)
print("Backlog in Tonnes:")
print(massDailyOxyBacklog)
print("Number of Oxygen Deprived Patients that wont get oxygen at Current Production Levels:")
print(nPeopleBacklog)


#Building sheet for Bar Chart
BarChartdata = StateList
BarChartdata['Oxygen Needed Daily(tonnes)'] = df['Oxygen Needed Daily(tonnes)']

#BarChartOutput
pl = BarChartdata.plot.bar(x="State")
pl.set_title("Daily Oxygen Requirement for Covid Patients by State (India)")
pl.get_figure().tight_layout()
plt.show()

OxyNeed_df = pd.DataFrame()
OxyNeed_df['State'] = df['State']
OxyNeed_df['Oxygen Needed Daily(tonnes)'] = df['Oxygen Needed Daily(tonnes)']


# Mapping the Oxygen Need data by state
## Source for Basis of mapping and Geojson of mapping Script: https://gist.githubusercontent.com/jbrobst
fig = px.choropleth(
    OxyNeed_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Oxygen Needed Daily(tonnes)',
    color_continuous_scale='Blues'
)

fig.update_geos(fitbounds="locations", visible=False)
fig.show()
