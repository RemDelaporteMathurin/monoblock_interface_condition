import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d


def get_flux_chemical(phi_heat, phi_imp):
    folder = "results/phi_heat={:.1e}_phi_imp={:.1e}".format(phi_heat, phi_imp)

    data_chemical = np.genfromtxt(
        folder + "/chemical_potential_continuity/derived_quantities.csv",
        delimiter=",",
        names=True,
    )
    t_chemical = data_chemical["ts"]

    flux_chemical = -data_chemical["Flux_surface_10_solute"]

    return t_chemical, flux_chemical


def get_flux_concentration(phi_heat, phi_imp):
    folder = "results/phi_heat={:.1e}_phi_imp={:.1e}".format(phi_heat, phi_imp)

    data_concentration = np.genfromtxt(
        folder + "/concentration_continuity/derived_quantities.csv",
        delimiter=",",
        names=True,
    )

    t_concentration = data_concentration["ts"]

    flux_concentration = -data_concentration["Flux_surface_10_solute"]

    return t_concentration, flux_concentration


def get_absolute_difference(phi_heat, phi_imp):
    t_concentration, flux_concentration = get_flux_concentration(phi_heat, phi_imp)
    flux_concentration_interp = interp1d(t_concentration, flux_concentration)
    t_chemical, flux_chemical = get_flux_chemical(phi_heat, phi_imp)

    abs_diff = 100 * (
        np.absolute(flux_concentration_interp(t_chemical) - flux_chemical)
        / flux_chemical
    )
    threshold = 1e7
    indexes = np.where(flux_chemical > threshold)
    return t_chemical[indexes], abs_diff[indexes]


if __name__ == "__main__":
    for phi_heat, phi_imp in zip([3e6, 5e6, 6e6, 7e6], [1e21, 1e21, 1e21, 1e21]):
        plt.plot(*get_absolute_difference(phi_heat, phi_imp))
    plt.xscale("log")
    plt.show()
