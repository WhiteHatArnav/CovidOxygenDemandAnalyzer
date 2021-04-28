
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import plotly.express as px

# input variables (default declarations)
MassOxProdDaily = 7100 #tonnes
VolOxyReqPerson = 550 # liters
nDailyCasesToday = 350000
rHosp = 0.060
rOxSup = 0.04
rICU = 0.02
rLtoTn = 0.00114

print("Please make sure that your current working directory has the table of new daily covid cases by state with the name StatewiseNewCases.csv")
print("You are welcome to use the one I have includded in my repository if you want to rely on data from Late April in India")
print("  ")

df = pd.read_csv(r'StatewiseNewCases.csv')
StateList= pd.read_csv('StateList.csv')

# input variables (dynamic input)
indic = (input("Would you like to enter your own data? Type Y/N: "))
if indic == 'Y':
    MassOxProdDaily =  float(input("Enter Daily National Oxygen Production in tonnes: "))
    VolOxyReqPerson =  float(input("Enter Daily Anticipated Oxygen needed per person in liter (Human Avg is 500 to 550 liters): "))
    nDailyCasesToday = float(input("Enter Daily number of cases you wish to analyze Oxygen demand for: "))
    rOxSup = float(input("Enter proportion of patients that would need oxygen  support (typically 0.03 to 0.04): "))

    # dynamic code based input of statewise data not included yet but can later be included for potential future use

if indic == 'N':
    print("\nScript will proceed with default values gathered on 26th of April, 2021 for India from online sources\n")

else:
    print("\nInvalid Input (user did not type Y or N). Script will proceed with default values gathered on 26th of April, 2021 for India from online sources\n")



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

print("\nMapping the Data...\n")

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
# testchange