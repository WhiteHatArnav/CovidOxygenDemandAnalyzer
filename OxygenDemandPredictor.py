import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

nActiveCasesPeak = 4800000
nCurrentActiveCases = 2813658
presentNewCases = 350000
PeakNewCases = 460000
nCurrentNewActiveCases = 130900
durationToPeak =  20 #days
RecoveryRatio = nCurrentNewActiveCases/presentNewCases


VolOxyReqPerson = 550
rOxSup = 0.04
rLtoTn = 0.00114
PolyRegCases = 4
PolyRegOxy = 3
# input variables (dynamic input)
indic = (input("Would you like to enter your own data? Type Y/N: "))
if indic == 'Y':
    VolOxyReqPerson =  float(input("Enter Daily Anticipated Oxygen needed per person in liter (Human Avg is 500 to 550 liters): "))
    rOxSup = float(input("Enter proportion of patients that would need oxygen  support (typically 0.03 to 0.04): "))
    PolyRegCases = int(input("What degree of polynomial would you like to regress the new and total active cases prediction to? Please enter an integer (recommended:  4): " ))
    PolyRegOxy = int(input("What degree of polynomial would you like to regress the oxygen supply prediction to? Please enter an integer (recommended:  3): " ))
    # dynamic code based input of statewise data not included yet but can later be included for potential future use

if indic == 'N':
    print("\nScript will proceed with default values gathered on 27th of April, 2021 for India from online sources\n")

else:
    print("\nInvalid Input (user did not type Y or N). Script will proceed with default values gathered on 27th of April, 2021 for India from online sources\n")




TotalActiveCaseList = [0]*durationToPeak
TotalActiveCaseList[0] = nCurrentActiveCases
TotalActiveCaseList[19] = nActiveCasesPeak

DailyAcceleration =  ((PeakNewCases - presentNewCases)/10)
IndexList = list(range(1,21))
IndexList1 = [0]*10
IndexList1[0:9] = list(range(1,11))
IndexList1[10] = 20


newCaselist = [0] * 20
newCaselist[0] = presentNewCases

for i in range(1,10):
    newCaselist[i] = (int)(newCaselist[i-1] + DailyAcceleration)

for j in range(1,10):
    TotalActiveCaseList[j] = (int)(TotalActiveCaseList[j-1] + RecoveryRatio*newCaselist[j])


RegressList = [0]*11
RegressList[0:10] = TotalActiveCaseList[0:10]
RegressList[10] = TotalActiveCaseList[19]


PolyModel = np.poly1d(np.polyfit(IndexList1,RegressList, PolyRegCases))
PolyLine = np.linspace(1, 20, nActiveCasesPeak)

r2 = r2_score(RegressList, PolyModel(IndexList1))


for k in range(10,20):
    TotalActiveCaseList[k] = int(PolyModel(k+1))
    
for a in range(10,20):    
    newCaselist[a] = (int)((TotalActiveCaseList[a] - TotalActiveCaseList[a-1])/RecoveryRatio)
    if newCaselist[a] <= 0:
        newCaselist[a] = newCaselist[a-1]


massOxSupNeed = [0]*20
for p in range(0,20):
    nDailyOxSupNeed = int(rOxSup * newCaselist[p])
    massOxSupNeed[p] = nDailyOxSupNeed * VolOxyReqPerson * rLtoTn

print("\nR Squared Value for cubic polynomial best fit curve for Oxygen Demand in India April 26th through May 16th:")
print("{:.6f}".format(r2))


OxyModel = np.poly1d(np.polyfit(range(1,18),massOxSupNeed[0:17], PolyRegOxy))
OxyLine = np.linspace(1, 17, 100)

OxyR2 = r2_score(massOxSupNeed[0:17], OxyModel(range(1,18)))

print("R Squared Value for quartic polynomial regression of Total Active Cases in India April 26th through May 16th:")
print("{:.6f}".format(OxyR2))



plt.scatter(IndexList1,RegressList)
plt.plot(PolyLine, PolyModel(PolyLine)) 
plt.title('Predictive Polynomial Regression of Active Covid Cases in India')
plt.xlabel('Days from April 26th, 2021')
plt.ylabel('Projected Total Active Covid-19 Cases in India')
plt.xticks(np.arange(min(IndexList1), max(IndexList1)+1, 1))
plt.show()


plt.scatter(range(1,18), massOxSupNeed[0:17])
plt.plot(OxyLine,OxyModel(OxyLine))
plt.title('Predictive Polynomial Best Fit Curve for Oxygen Demand in India till Peak in May, 2021')
plt.xlabel('Days from April 26th, 2021')
plt.ylabel('Oxygen Demand in India(Tonnes)')
plt.xticks(np.arange(1, 18, 1))
plt.show()
















