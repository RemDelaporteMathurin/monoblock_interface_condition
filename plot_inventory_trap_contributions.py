import matplotlib.pyplot as plt
import numpy as np

vol_w = 8
vol_cu = 7
vol_cucrzr = 6

grey_w = (183 / 255, 183 / 255, 183 / 255)
orange_cu = (230 / 255, 145 / 255, 56 / 255)
orange_cucrzr = (180 / 255, 95 / 255, 6 / 255)


def plot_inventory_contributions(phi_heat, phi_imp):
    folder = "results/phi_heat={:.1e}_phi_imp={:.1e}".format(phi_heat, phi_imp)

    data = np.genfromtxt(
        folder + "/chemical_potential_continuity/derived_quantities.csv",
        delimiter=",",
        names=True,
    )

    t = data["ts"]

    inventory = sum(
        [data["Total_retention_volume_{}".format(vol_id)] for vol_id in [8, 7, 6]]
    )

    trap_w = data["Total_1_volume_{}".format(8)] + data["Total_2_volume_{}".format(8)]
    trap_cu = data["Total_1_volume_{}".format(vol_cu)]
    trap_cucrzr = data["Total_1_volume_{}".format(vol_cucrzr)]
    mobile = sum(
        [data["Total_solute_volume_{}".format(vol_id)] for vol_id in [8, 7, 6]]
    )

    plt.fill_between(
        t, np.zeros(t.shape), trap_w / inventory * 100, alpha=0.5, color=grey_w
    )

    plt.fill_between(
        t,
        trap_w / inventory * 100,
        (trap_w + mobile) / inventory * 100,
        alpha=0.5,
        color="tab:blue",
    )

    plt.fill_between(
        t,
        (mobile + trap_w) / inventory * 100,
        (mobile + trap_cu + trap_w) / inventory * 100,
        alpha=0.5,
        color=orange_cu,
    )

    plt.fill_between(
        t,
        (mobile + trap_cu + trap_w) / inventory * 100,
        (mobile + trap_cucrzr + trap_cu + trap_w) / inventory * 100,
        alpha=0.5,
        color=orange_cucrzr,
    )


if __name__ == "__main__":
    plot_inventory_contributions(phi_heat=6e6, phi_imp=1e21)

    plt.annotate("W", (3e5, 0.5 * 100), fontsize=25, color="tab:grey")
    plt.annotate("mobile", (4e6, 0.85 * 100), fontsize=15, color="tab:blue")
    plt.annotate("CuCrZr", (8e6, 0.95 * 100), fontsize=12, color=orange_cucrzr)

    plt.xscale("log")
    # plt.xlim(t.min(), t.max())
    plt.xlabel("Time (s)")

    plt.ylim(0, 100)
    plt.ylabel("Inventory contributions (%)")

    plt.gca().spines.right.set_visible(False)
    plt.gca().spines.top.set_visible(False)

    plt.show()
