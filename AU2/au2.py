"""

Arbetsuppgift 2, RLC-kretsen, resonans och filter
Authors: Firoz & Ömer

Vårt python program ska göra följande utifrån användarens val:

Lösa differentialekvationen numeriskt för en RLC-krets,
plottar spänningen och strömmen som funktion av tiden och
beräkna fasvinkeln. 

Plottar en  ̈overföringsfunktion för någon av komponenterna i en RLC-krets.
Plottar överföringsfunktionen för ett analogt filter baserat på en RLC-krets
och optimerar resistansen så att överföringsfunktionen blir så jämn som möjligt.

"""
#Lösa diffrentialekvation för en RLC-krets där användaren ger värden på R,L,C samt uppgifter om spänningen från spänningskällan och begynnelsevilkor
import tkinter as tk
from tkinter import simpledialog
import numpy as np
import matplotlib.pyplot as plt
import math

def submit():
    global R,L,C,dt,omega,U0
    R = float(entry1.get())
    L = float(entry2.get())
    C = float(entry3.get())
    dt = float(entry4.get())
    omega = float(entry5.get())
    U0 = float(entry6.get())
    root.destroy()  # Stänger fönstret efter att ha tagit emot indata

# Skapa huvudfönstret
root = tk.Tk()
root.title("Input Fönster")

# Skapa och packa etiketter och inmatningsfält

tk.Label(root, text="Resistansen, R").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Induktansen, L").pack()
entry2 = tk.Entry(root)
entry2.pack()

tk.Label(root, text="Kapacitansen, C").pack()
entry3 = tk.Entry(root)
entry3.pack()

tk.Label(root, text="Spänning, U\u2080").pack()
entry6 = tk.Entry(root)
entry6.pack()

tk.Label(root, text="Vinkelfrekvensen, \u03C9").pack()
entry5 = tk.Entry(root)
entry5.pack()

tk.Label(root, text="Steglängden, \u0394t").pack()
entry4 = tk.Entry(root)
entry4.pack()

# Skapa och packa en knapp som samlar in och skriver ut de insamlade värdena när den klickas
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

# Starta händelseloopen
root.mainloop()

tmax = 0.08
t = np.arange(0,tmax,dt)
dim = len(t)

# Beräkna impedansen Z och initiala strömamplituden I0
Z = np.sqrt(R**2 + (1/(omega*C) - omega*L)**2)
I0 = U0 / Z  # Initial amplitud av strömmen baserat på U0 och Z
phi = np.arctan((1/(omega*C) - omega*L) / R)  # Initial fasvinkel

# Analytisk lösning av strömmen I(t)
I_a = I0 * np.sin(omega * t + phi)

# Numerisk lösning
# Initialisera vektorer
I_n = np.zeros(dim)  # Ström I(t)
Id = np.zeros(dim) # Derivatan av strömmen I'(t)
Idd = np.zeros(dim) # Andra derivatan av strömmen I''(t)

# Begynnelsevillkor
I_n[0] = I0  # Initial ström ges av I0
Id[0] = -omega * U0 * np.cos(omega * t[0]) / R  # Initial derivata av ström, härledd från U'(t) = U0 * omega * cos(omega * t)

# Numerisk lösning med Euler-metoden
for i in range(dim - 1):
    Idd[i] = (U0 * omega * np.cos(omega * t[i]) - R * Id[i] - I_n[i] / C) / L # Beräkna andra derivatan av strömmen, härleds från diff.ekv.
    Id[i+1] = Id[i] + Idd[i] * dt # Uppdatera första derivatan av strömmen
    I_n[i+1] = I_n[i] + Id[i] * dt # Uppdatera strömmen

# Spänningen U(t) är en sinusvåg
U_t = U0 * np.sin(omega * t)

# Nu plottar vi både strömmen och spänningen i samma diagram
plt.figure(figsize=(12, 6))
plt.plot(t, U_t, label='U(t)', color='blue')
plt.plot(t, Z * I_a, label='Z * I(t) analytisk', color='black', linestyle='--')
plt.plot(t, Z * I_n, label='Z * I(t) numerisk', color='orange')
phi_round = round(math.degrees(phi), 2)
plt.title('Fasvinkeln är : ' + str(phi_round) + '\u00B0')
plt.xlabel('Tid (s)')
plt.ylabel('Amplitud (V)')
plt.legend()
plt.grid(True)
plt.show()

def transfer_function_coil(omega, R, L, C):
    XL = omega * L  # Beräknar induktiv reaktans XL = ωL
    XC = 1 / (omega * C)  # Beräknar kapacitiv reaktans XC = 1/(ωC)
    Z = np.sqrt(R**2 + (XL - XC)**2)  # Beräknar totala impedansen Z för RLC-kretsen
    H = XL / Z  # Beräknar överföringsfunktionen för spolen H(ω) = XL / Z
    return H

# Beräknar resonansfrekvensen omega_0 
omega_0 = 1 / np.sqrt(L * C)

omega_range = np.linspace(0.01 * omega_0, 3 * omega_0, 10000)

H_values = transfer_function_coil(omega_range, R, L, C)

plt.figure(figsize=(10, 6))  # Skapar en figur med storleken 10x6 tum
plt.plot(omega_range / omega_0, H_values)  # Plottar H(ω) som funktion av normaliserad frekvens ω/ω_0
plt.xlabel(r'$\omega/\omega_0$')  # Sätter etikett för x-axeln
plt.ylabel(r'$H(\omega)$')  # Sätter etikett för y-axeln
plt.title('Överföringsfunktion för spolen i RLC-kretsen')  # Titel för grafen
plt.grid(True)  # Aktiverar rutnät för grafen
plt.show()  # Visar grafen


def cost_function(H_values, omega_range, omega_0):

    # Skapar Ideal funktion: 0 för frekvenser ≤ omega_0 (lågpass), 1 för frekvenser > omega_0 (högpass).
    target_function = np.where(omega_range <= omega_0, 0, 1)
    
    # Beräknar medelkvadratfelet (MSE) mellan filtrets faktiska respons och Ideal funktionen.
    cost = np.mean((H_values - target_function)**2)
    
    return cost

def optimize_R(L, C, omega_0, omega_range):
    R_min = 1  # Sätter ett minimumvärde för resistansen R.
    R_max = 1000  # Sätter ett maximumvärde för R.
    num_steps = 100  # Bestämmer antalet steg i sökområdet.

    best_cost = np.inf  # Initierar best_cost med oändlighet.
    best_R = R_min  # Anta att det lägsta möjliga R-värdet är det bästa.

    for R in np.linspace(R_min, R_max, num_steps):
        # Beräknar överföringsfunktionen för varje R.
        H_values = transfer_function_coil(omega_range, R, L, C)
        # Beräknar medelkvadratfelet, ett mått på hur väl filtret med det aktuella R-värdet uppfyller kraven.
        current_cost = cost_function(H_values, omega_range, omega_0)

        # Jämför den aktuella kostnaden med den bästa (lägsta) kostnaden hittills.
        # Detta steg hittar det R-värde som ger den lägsta kostnaden.
        if current_cost < best_cost:
            best_cost = current_cost
            best_R = R

    return best_R


# Hitta det optimala R-värdet
optimal_R = optimize_R(L, C, omega_0, omega_range)

# Beräknar överföringsfunktionen med det optimala R-värdet
H_values_optimal = transfer_function_coil(omega_range, optimal_R, L, C)

# Plottar överföringsfunktionen
plt.figure(figsize=(10, 6))
plt.plot(omega_range / omega_0, H_values_optimal, label=f'Optimalt R = {optimal_R:.2f} Ohm')
plt.xlabel(r'$\omega/\omega_0$')
plt.ylabel(r'$H(\omega)$')
plt.title('Överföringsfunktion för spolen med optimalt R')
plt.grid(True)
plt.legend()
plt.show()
