import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

plt.rcParams['font.size'] = 8
rcParams['mathtext.default'] = 'regular'

class isotherm:
    def __init__(self, file_name, surf_conc = 1, surf_vol = 160):
        """
        Parameters
        file_name: file name in str
            1st col: record of time (s)
            2nd col: record of surface area (cm^2)
            4th col: surface pressure
        surf_conc: concentration of surfactant in spreading solution (mM)
        surf_vol : volume of spread solution (uL)
        
        t: time (s)
        a: area per molecule (Ang^2/molecule)
        p: surface pressure (mN/m)
        
        """
        self.surf_conc = surf_conc
        self.surf_vol = surf_vol
        data = np.genfromtxt(file_name, skip_header=1, delimiter='\t', comments='#')
        self.t = data[:,0]
        self.a = data[:,1] / (self.surf_conc * 6.02 * 0.01 * self.surf_vol)
        self.p = data[:,5]
        
    def trim(self, hp=10):
        """
        Remove data entries after reaching the target pressure
        hp: hold pressure
        """
        for i, p_ in enumerate(self.p):
            if p_ > hp-0.1:
                break
        
        max_idx = i+1000
        self.t = self.t[:max_idx]
        self.a = self.a[:max_idx]
        self.p = self.p[:max_idx]
        
Er_ODPA = isotherm('ODPA_data/ODPA_Er.txt')
Nd_ODPA = isotherm('ODPA_data/ODPA_Nd.txt')
Mix_ODPA = isotherm('ODPA_data/ODPA_mixture.txt')

Er_DHDP = isotherm('Er_pure/Er_pure_iso.txt',surf_vol=120)
Nd_DHDP = isotherm('Nd_pure/Nd_pure_iso.txt',surf_vol=100)
Mix_DHDP= isotherm('mixture/mixture_iso.txt',surf_vol=120)

fig = plt.figure()
fig_width = 3.25
fig_height = fig_width / (1.618)
fig.set_size_inches(fig_width, fig_height)

ax = fig.add_axes([0.2,0.2,0.7,0.7])
ax.set_title('ODPA Isotherms', weight='bold')
ax.set_xlabel('Area/Alkyl Tail ($\AA^{2}$)')
ax.set_ylabel('Surface Pressure (mN/m)')
ax.set_xlim(0,40)
ax.set_ylim(-0.5,12)

ODPA_isotherms = [Er_ODPA, Nd_ODPA, Mix_ODPA]
DHDP_isotherms = [Er_DHDP, Nd_DHDP, Mix_DHDP]
labels = ['Er', 'Nd', 'Mix']

for i, isotherm in enumerate(ODPA_isotherms):
    isotherm.trim(hp=4)
    ax.plot(isotherm.a, isotherm.p, label=labels[i]+'+ODPA')

for i, isotherm in enumerate(DHDP_isotherms):
    isotherm.trim(hp=9)
    ax.plot(isotherm.a, isotherm.p, label=labels[i]+'+DHDP')

ax.legend(loc='lower left')

plt.savefig('isotherms.png', dpi=500)