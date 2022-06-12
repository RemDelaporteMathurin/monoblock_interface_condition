import matplotlib.pyplot as plt
import numpy as np

data_concentration = np.genfromtxt(
    "results/concentration_continuity/derived_quantities.csv", delimiter=",", names=True
)

t_concentration = data_concentration["ts"]

inventory_concentration = sum(
    [data_concentration["Total_retention_volume_{}".format(vol_id)] for vol_id in [8]]
)

data_chemical = np.genfromtxt(
    "results/chemical_potential_continuity/derived_quantities.csv",
    delimiter=",",
    names=True,
)

t_chemical = data_chemical["ts"]

inventory_chemical = sum(
    [data_chemical["Total_retention_volume_{}".format(vol_id)] for vol_id in [8]]
)

plt.plot(t_concentration, inventory_concentration)
plt.plot(t_chemical, inventory_chemical)
plt.yscale("log")
plt.xscale("log")
plt.show()
