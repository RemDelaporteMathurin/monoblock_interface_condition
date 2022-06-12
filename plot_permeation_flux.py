import matplotlib.pyplot as plt
import numpy as np

data_concentration = np.genfromtxt(
    "results/concentration_continuity/derived_quantities.csv", delimiter=",", names=True
)

t_concentration = data_concentration["ts"]

flux_concentration = -data_concentration["Flux_surface_10_solute"]


data_chemical = np.genfromtxt(
    "results/chemical_potential_continuity/derived_quantities.csv",
    delimiter=",",
    names=True,
)

t_chemical = data_chemical["ts"]

flux_chemical = -data_chemical["Flux_surface_10_solute"]

plt.plot(t_concentration, flux_concentration)
plt.plot(t_chemical, flux_chemical)
plt.yscale("log")
plt.xscale("log")
plt.show()
