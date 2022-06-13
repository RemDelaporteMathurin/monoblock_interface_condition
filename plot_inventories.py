import matplotlib.pyplot as plt
import numpy as np

phi_heat = 7e6  # W/m2
phi_imp = 1e21  # H/m2/s

for phi_heat, phi_imp in zip([3e6, 6e6, 7e6], [1e21, 1e21, 1e21]):

    folder = "results/phi_heat={:.1e}_phi_imp={:.1e}".format(phi_heat, phi_imp)

    data_concentration = np.genfromtxt(
        folder + "/concentration_continuity/derived_quantities.csv",
        delimiter=",",
        names=True,
    )

    t_concentration = data_concentration["ts"]

    inventory_concentration = sum(
        [
            data_concentration["Total_retention_volume_{}".format(vol_id)]
            for vol_id in [8]
        ]
    )

    data_chemical = np.genfromtxt(
        folder + "/chemical_potential_continuity/derived_quantities.csv",
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
