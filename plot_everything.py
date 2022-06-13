from plot_inventories import (
    get_absolute_difference,
    get_inventory_chemical,
    get_inventory_concentration,
)
from plot_inventory_trap_contributions import plot_inventory_contributions

import matplotlib.pyplot as plt

fig, axs = plt.subplots(
    3,
    4,
    sharex="col",
    sharey="row",
    gridspec_kw={"height_ratios": [1, 0.5, 1]},
    figsize=(6.4, 6.4),
)

grey_w = (183 / 255, 183 / 255, 183 / 255)
orange_cu = (230 / 255, 145 / 255, 56 / 255)
orange_cucrzr = (180 / 255, 95 / 255, 6 / 255)

for i, (phi_heat, phi_imp) in enumerate(
    zip([3e6, 5e6, 6e6, 7e6], [1e21, 1e21, 1e21, 1e21])
):

    plt.sca(axs[0][i])

    title = "{:.1f} MW".format(phi_heat / 1e6)

    plt.gca().title.set_text(title)

    plt.plot(*get_inventory_chemical(phi_heat, phi_imp))
    plt.plot(*get_inventory_concentration(phi_heat, phi_imp), linestyle="dashed")
    plt.gca().spines.right.set_visible(False)
    plt.gca().spines.top.set_visible(False)
    if i == 0:
        plt.ylabel("Inventory (H/m)")

    if i == 3:
        plt.annotate(
            "Chemical pot. \n continuity", (2e4, 1e19), fontsize=9, color="tab:blue"
        )
        plt.annotate(
            "Concentration. \n continuity", (1e5, 5e16), fontsize=9, color="tab:orange"
        )

    plt.yscale("log")
    plt.xscale("log")

    plt.sca(axs[1][i])
    plt.plot(*get_absolute_difference(phi_heat, phi_imp))
    plt.ylim(0, 60)
    if i == 0:
        plt.ylabel("Difference (%)")
    plt.gca().spines.right.set_visible(False)
    plt.gca().spines.top.set_visible(False)

    plt.sca(axs[2][i])
    plot_inventory_contributions(phi_heat, phi_imp)
    plt.ylim(0, 100)
    plt.xlabel("Time (s)")
    plt.gca().spines.right.set_visible(False)
    plt.gca().spines.top.set_visible(False)
    if i == 0:
        plt.ylabel("Inventory contributions (%)")
    if i == 3:
        plt.annotate("W", (3e7, 10), fontsize=13, color="tab:grey")
        plt.annotate("mobile", (3e7, 60), fontsize=13, color="tab:blue")
        plt.annotate("CuCrZr", (3e7, 95), fontsize=13, color=orange_cucrzr)


plt.show()
