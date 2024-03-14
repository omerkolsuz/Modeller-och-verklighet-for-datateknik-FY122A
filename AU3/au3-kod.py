"""

Arbetsuppgift 3, Solen som energikälla
Authors: Firoz & Ömer

Vår uppdrag är att konstruera ett eller flera program i Python och att utnyttja informationen
i tabell 1 och appendix A för att utföra uppgifter nedan för en solpanel med verkningsgraden
ε = 0.15 och arean A = 50 m2 .

"""

import numpy as np
from matplotlib import pyplot as plt
import math

verk_grad = 0.15
area = 50
panel_lat = 65.6 
panel_azi = 150
panel_alt = 25
solar_konst = 1360.0

"""
1. Skapa plottar som visar effekten i Watt [W] som funktion av tiden på dygnet för er grupps
stationära solpanel (se tabell 1) för ett dygn i januari och i juni. Ni ska inte ta hänsyn till
antalet soltimmar, d.v.s. anta alltid soligt väder (se figur 2 i appendix A för exempel).
"""
def calculate_1(dag,tid):
    dek_vinkel = math.radians(-23.44)*np.cos((math.radians(360)/365) * dag)
    #print('deklinationsvinekeln är',np.degrees(dek_vinkel))

    tim_vinkel = math.radians(15) * tid- math.radians(180)
    #print('timvinkeln är',np.degrees(tim_vinkel))

    sol_alt = np.arcsin(np.sin(math.radians(panel_lat)) * np.sin(dek_vinkel) + np.cos(math.radians(panel_lat)) * np.cos(dek_vinkel) * np.cos(tim_vinkel))
    #print('solpanelen är',np.degrees(sol_alt))
    
    if sol_alt > 0:

        if tim_vinkel > 0:
            azi_vinkel = math.radians(180) + np.arccos((np.sin(math.radians(panel_lat)) * np.sin(sol_alt) - np.sin(dek_vinkel)) / (np.cos(math.radians(panel_lat)) * np.cos(sol_alt)))
            #print('azimutvinkeln är',np.degrees(azi_vinkel))

        elif tim_vinkel < 0:
            azi_vinkel = math.radians(180) - np.arccos((np.sin(math.radians(panel_lat)) * np.sin(sol_alt) - np.sin(dek_vinkel)) / (np.cos(math.radians(panel_lat)) * np.cos(sol_alt)))
            #print('azimutvinkeln är',np.degrees(azi_vinkel))

        intensitet = 1.1 * solar_konst * 0.7**((1/np.sin(sol_alt))**0.678)
        #print('intensitet är',intensitet)

        intens_panel = intensitet * ((np.cos(math.radians(panel_alt) - sol_alt) * np.cos(math.radians(panel_azi) - azi_vinkel)) + ((1 - np.cos(math.radians(panel_azi) - azi_vinkel)) * (np.sin(math.radians(panel_alt)) * np.sin(sol_alt))))
        #print('intensiteten mot solpanelen är',intens_panel)

        effekt = verk_grad * intens_panel * area
        #print('solpanelens levererade effekt är',effekt)

    else:
        effekt = 0

    if effekt < 0:
        effekt = 0

    return effekt
    
dag_tider = np.linspace(0, 24, 100)
effekter_jan = [calculate_1(15, tid) for tid in dag_tider]
effekter_jun = [calculate_1(167,tid) for tid in dag_tider]
    
total_effekt_jan = 0.0
total_effekt_jun = 0.0
total_effekt_ = 0.0

sol_timmar_jan = 0
sol_timmar_jun = 0
sol_timmar_ = 0

# Effekten för varje dag i ett helt år, start dag == 1
for i in range(365):  # Ett år har 365 dagar
    effekt_ = np.array([calculate_1(1+i, tid) for tid in dag_tider])

    tecken = np.diff(np.sign(effekt_)) != 0

    index = np.where(tecken)[0]

    avst_ar = dag_tider[index[1:]] - dag_tider[index[:-1]]
    dag_timmar = avst_ar[0]
    sol_timmar_ += dag_timmar

    area_ = np.trapz(effekt_, dag_tider)
    total_effekt_ += area_

# Effekten för varje dag i januari, start dag == 1
for i in range(31):  # Januari har 31 dagar
    effekt_jan = np.array([calculate_1(1+i, tid) for tid in dag_tider])

    tecken = np.diff(np.sign(effekt_jan)) != 0

    index = np.where(tecken)[0]

    avst_ar = dag_tider[index[1:]] - dag_tider[index[:-1]]
    dag_timmar = avst_ar[0]
    sol_timmar_jan += dag_timmar

    area_jan = np.trapz(effekt_jan, dag_tider)
    total_effekt_jan += area_jan

# Effekten för varje dag i juni, start dag == 153
for i in range(30):  # Juni har 30 dagar
    effekt_jun = np.array([calculate_1(153+i,tid) for tid in dag_tider])

    tecken = np.diff(np.sign(effekt_jun)) != 0

    index = np.where(tecken)[0]

    avst_ar = dag_tider[index[1:]] - dag_tider[index[:-1]]
    dag_timmar = avst_ar[0]
    sol_timmar_jun += dag_timmar

    area_jun = np.trapz(effekt_jun, dag_tider)
    total_effekt_jun += area_jun

jan_kwh = round(total_effekt_jan/1000,2)
jun_kwh = round(total_effekt_jun/1000,2)
tot_kwh = round(total_effekt_/1000,2)

print('Soltimmar för året: ' + str(round(sol_timmar_,1)) + '\nSoltimmar för januari: ' + str(round(sol_timmar_jan,1)) + '\nSoltimmar för juni: ' + str(round(sol_timmar_jun,1)))

plt.figure(figsize=(10, 6))
plt.plot(dag_tider,effekter_jan,label='Panel 15 Januari', color='blue')
plt.plot(dag_tider,effekter_jun,label='Panel 15 Juni', color='red')
plt.ylabel("P (W)")
plt.xlabel("t (h)")
plt.grid()
plt.legend()
plt.show()


"""
2. Beräkna energin i kWh som en stationär solpanel för er grupp (se tabell nedan) levererar
under januari månad, juni månad och under ett helt år. Ni ska utföra beräkningarna både
med och utan hänsyn taget till antalet soltimmar. 

Soltimmar för:
Januari == 23
Juni == 299
Ett år == 1872
"""

print('\nBeräkning av energin utan hänsyn till soltimmar:\n' + 'Energin för ett helt år: ' + str(tot_kwh) + ' kWh\n' + 'Energin för Januari månad: ' 
      + str(jan_kwh) + ' kWh\n' + 'Energin för Juni månad: ' + str(jun_kwh) + ' kWh\n')

def calculate_kwh(kwh,sol,sol_tabell):
    kwh_tabell = sol_tabell / (sol/kwh)
    return kwh_tabell

total_effekt_jan_sol = calculate_kwh(jan_kwh,sol_timmar_jan,23)
total_effekt_jun_sol = calculate_kwh(jun_kwh,sol_timmar_jun,299)
total_effekt_sol = calculate_kwh(tot_kwh,sol_timmar_,1872)

jan_kwh_sol = round(total_effekt_jan_sol,2)
jun_kwh_sol = round(total_effekt_jun_sol,2)
tot_kwh_sol = round(total_effekt_sol,2)

print('Soltimmar för året: ' + str(1872) + '\nSoltimmar för januari: ' + str(23) + '\nSoltimmar för juni: ' + str(299) + '\n')

print('Beräkning av energin med hänsyn till soltimmar:\n' + 'Energin för ett helt år: ' + str(tot_kwh_sol) + ' kWh\n' + 'Energin för Januari månad: ' 
      + str(jan_kwh_sol) + ' kWh\n' + 'Energin för Juni månad: ' + str(jun_kwh_sol) + ' kWh\n')

"""
3. Optimera θp med hänsyn taget till antalet soltimmar så att levererad energi i kWh under
ett år blir så stor som möjligt för gruppens stationära solpanel. Hur stor blir den maximala
energin i kWh och vid vilken vinkel θp? Vinkeln αp enligt tabell.
"""

ny_tider = np.linspace(0, 24, 10)
max_effekt = 0.0
opt_panel_alt = 0

for i in range(90):
    kwh_ = 0.0
    nu_effekt = 0.0
    panel_alt = i
    # Effekten för varje dag i ett helt år, start dag == 1
    for j in range(365):  # Ett år har 365 dagar
        effekt_opt = np.array([calculate_1(1+j, tid) for tid in ny_tider])
        area_opt = np.trapz(effekt_opt, ny_tider)
        nu_effekt += area_opt
    kwh_ = calculate_kwh(nu_effekt,sol_timmar_,1872)
    if kwh_ > max_effekt:
        max_effekt = kwh_
        opt_panel_alt = panel_alt

max_kwh = round(max_effekt/1000,2)
print('Maximala energi under ett år med optimerat θp (med hänsyn till soltimmar): ' + str(max_kwh) + ' kWh\n' + 'θp är då: ' + str(opt_panel_alt) + '°\n')

"""
4. Anta vidare att den stationära solpanelen kostar 200 000 kr att installera och att den el som
solpanelen producerar får används ’gratis’ och att underskott/överskott av el kan köpas/säljas
på elbörsen för 2 kr/kWh. Om ett hushåll där solpanelen är installerad förbrukar 14 000
kWh/år, efter hur många år har solpanelen betalat sig (jämfört med att köpa all el på
elbörsen)? Använd optimerad vinkel θp i uppgift 3 för att lösa uppgiften och ta hänsyn till
antalet soltimmar. Vinkeln αp enligt tabell.
"""

def calculate_pris(kwh,hus_kwh,panel_kostnad,pris_kwh):

    netto_energi = kwh -hus_kwh
    pengar = pris_kwh * kwh
    antal_solvarv = panel_kostnad / pengar

    if netto_energi < 0:
        print('Vi får ett underskott under året på ' + str(round(netto_energi,2)) + ' kWh' + '\nDet måste köpas till energi för ' + str(round((-netto_energi*pris_kwh),0)) + ' Kr')

    elif netto_energi > 0:
        print('Vi får ett överskott under året på ' + str(round(netto_energi,2)) + ' kWh' + '\nEnergin kan säljas för ' + str(round((netto_energi*pris_kwh),0)) + ' Kr')

    print('Det kommer ta ' + str(round(antal_solvarv,1)) + ' år för sol panelen att ha betalat för sig själv \nDå man köper all el på elbörsen\n')
print('Solpanel som kostar 200 000 kr:')
calculate_pris(max_kwh,14000,200000,2)

"""
5. Anta nu att solpanelen görs rörlig kring två axlar och att den förses med elmotorer så att den
kan följa solens gång exakt (θp = θs och αp = αs). Hur stor energi i kWh levererar solpanelen
på ett år nu? Beräkningar utförs med hänsyn till antalet soltimmar. Totalt kostar en sådan
panel 400 000 kr att installera. Efter hur många år har denna solpanel betalat sig (jämfört
med att köpa all el på elbörsen)? Den el som motorerna drar för att vrida solpanelen i solens
riktning kan försummas. Övriga uppgifter som i uppgift 4 ovan.
"""
def calculate_2(dag,tid):
    dek_vinkel = math.radians(-23.44)*np.cos((math.radians(360)/365) * dag)
    #print('deklinationsvinekeln är',np.degrees(dek_vinkel))

    tim_vinkel = math.radians(15) * tid- math.radians(180)
    #print('timvinkeln är',np.degrees(tim_vinkel))

    sol_alt = np.arcsin(np.sin(math.radians(panel_lat)) * np.sin(dek_vinkel) + np.cos(math.radians(panel_lat)) * np.cos(dek_vinkel) * np.cos(tim_vinkel))
    #print('solpanelen är',np.degrees(sol_alt))
    panel_alt = math.degrees(sol_alt)

    if sol_alt > 0:

        if tim_vinkel > 0:
            azi_vinkel = math.radians(180) + np.arccos((np.sin(math.radians(panel_lat)) * np.sin(sol_alt) - np.sin(dek_vinkel)) / (np.cos(math.radians(panel_lat)) * np.cos(sol_alt)))
            #print('azimutvinkeln är',np.degrees(azi_vinkel))

        elif tim_vinkel < 0:
            azi_vinkel = math.radians(180) - np.arccos((np.sin(math.radians(panel_lat)) * np.sin(sol_alt) - np.sin(dek_vinkel)) / (np.cos(math.radians(panel_lat)) * np.cos(sol_alt)))
            #print('azimutvinkeln är',np.degrees(azi_vinkel))

        panel_azi = math.degrees(azi_vinkel)

        intensitet = 1.1 * solar_konst * 0.7**((1/np.sin(sol_alt))**0.678)
        #print('intensitet är',intensitet)

        intens_panel = intensitet * ((np.cos(math.radians(panel_alt) - sol_alt) * np.cos(math.radians(panel_azi) - azi_vinkel)) + ((1 - np.cos(math.radians(panel_azi) - azi_vinkel)) * (np.sin(math.radians(panel_alt)) * np.sin(sol_alt))))
        #print('intensiteten mot solpanelen är',intens_panel)

        effekt = verk_grad * intens_panel * area
        #print('solpanelens levererade effekt är',effekt)

    else:
        effekt = 0

    if effekt < 0:
        effekt = 0

    return effekt

opt_total_effekt = 0.0

# Effekten för varje dag med optimerad θp och αp i ett helt år, start dag == 1
for i in range(365):  # Ett år har 365 dagar
    effekt_ = np.array([calculate_2(1+i, tid) for tid in dag_tider])
    area_ = np.trapz(effekt_, dag_tider)
    opt_total_effekt += area_

opt_tot_kwh = round(calculate_kwh((opt_total_effekt/1000),sol_timmar_,1872),2)

print('Solpanel som kostar 400 000 kr:')
calculate_pris(opt_tot_kwh,14000,400000,2)

print('Energin för ett helt år med elmotorer: ' + str(opt_tot_kwh) + ' kWh')
