import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d


def get_inventory_chemical(phi_heat, phi_imp):
    folder = "results/phi_heat={:.1e}_phi_imp={:.1e}".format(phi_heat, phi_imp)

    data_chemical = np.genfromtxt(
        folder + "/chemical_potential_continuity/derived_quantities.csv",
        delimiter=",",
        names=True,
    )

    t_chemical = data_chemical["ts"]

    inventory_chemical = sum(
        [
            data_chemical["Total_retention_volume_{}".format(vol_id)]
            for vol_id in [8, 7, 6]
        ]
    )
    return t_chemical, inventory_chemical


def get_inventory_concentration(phi_heat, phi_imp):
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
            for vol_id in [8, 7, 6]
        ]
    )

    return t_concentration, inventory_concentration


def get_absolute_difference(phi_heat, phi_imp):
    t_concentration, inventory_concentration = get_inventory_concentration(
        phi_heat, phi_imp
    )
    inventory_concentration_interp = interp1d(t_concentration, inventory_concentration)
    t_chemical, inventory_chemical = get_inventory_chemical(phi_heat, phi_imp)

    abs_diff = 100 * (
        np.absolute(inventory_concentration_interp(t_chemical) - inventory_chemical)
        / inventory_chemical
    )

    return t_chemical, abs_diff


if __name__ == "__main__":
    for phi_heat, phi_imp in zip([3e6, 5e6, 6e6, 7e6], [1e21, 1e21, 1e21, 1e21]):
        # t_concentration, inventory_concentration = get_inventory_concentration(
        #     phi_heat, phi_imp
        # )
        # t_chemical, inventory_chemical = get_inventory_chemical(phi_heat, phi_imp)
        # plt.plot(t_concentration, inventory_concentration)
        # plt.plot(t_chemical, inventory_chemical)
        plt.plot(*get_absolute_difference(phi_heat, phi_imp))

    # plt.yscale("log")
    plt.xscale("log")
    plt.show()
