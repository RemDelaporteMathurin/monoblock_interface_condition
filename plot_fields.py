import fenics as f
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def scientificNotation(value, pos=0):
    if value == 0:
        return "0"
    else:
        e = np.log10(np.abs(value))
        m = np.sign(value) * 10 ** (e - int(e))
        return r"${:.1f} \times 10^{{{:d}}}$".format(m, int(e))


fmt_labels = scientificNotation
fmt_colorbar = ticker.FuncFormatter(scientificNotation)


def load_mesh(meshfile):
    """Loads mesh

    Args:
        meshfile (str): path of the meshfile

    Returns:
        fenics.mesh: the mesh of the solution
    """
    mesh = f.Mesh()
    f.XDMFFile(meshfile).read(mesh)
    return mesh


def load_field(mesh, fieldfile, field, counter=-1):
    V = f.FunctionSpace(mesh, "DG", 1)
    u = f.Function(V)

    f.XDMFFile(fieldfile).read_checkpoint(u, field, counter)
    return u


def save(filename, ext, transparent=True):
    """Saves active figure

    Args:
        filename (str): path of the file (without extension)
        ext (str, list): extension(s) of the output file(s)
        (ex: "pdf", "svg", ["png", "pdf"])
        transparent (bool, optional): Sets the background transparent.
        Defaults to True.
    """
    if not isinstance(ext, list):
        ext = [ext]
    for e in ext:
        plt.savefig(filename + "." + e, transparent=transparent)
    return


def make_figure(function, max=None, min=None):
    fig = plt.figure(figsize=(4.8, 4.8))
    if (min, max) == (None, None):
        levels = 1000
        cb_ticks = np.linspace(0, function.vector().max(), endpoint=True, num=10)

    else:
        levels = np.linspace(min, max, endpoint=True, num=1000)
        cb_ticks = np.linspace(0, max, endpoint=True, num=10)

    CS = f.plot(function, levels=levels, extend="min", vmin=0)
    cb = fig.colorbar(CS, ticks=cb_ticks, format=fmt_colorbar, extendfrac=0)
    cb.ax.set_title(r"m$^{-3}$")

    for c in CS.collections:  # for avoiding white lines in pdf
        c.set_edgecolor("face")
    fig.patch.set_visible(False)
    plt.axis("off")
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    phi_heat, phi_imp = 7e6, 1e21
    mesh = load_mesh("mesh/mesh_domains.xdmf")
    folder = "results/phi_heat={:.1e}_phi_imp={:.1e}".format(phi_heat, phi_imp)
    retention_chemical_pot = load_field(
        mesh,
        fieldfile=folder + "/chemical_potential_continuity/retention.xdmf",
        field="retention",
    )
    retention_concentration = load_field(
        mesh,
        fieldfile=folder + "/concentration_continuity/retention.xdmf",
        field="retention",
    )

    mobile_chemical_pot = load_field(
        mesh,
        fieldfile=folder + "/chemical_potential_continuity/mobile.xdmf",
        field="mobile_concentration",
    )

    mobile_concentration = load_field(
        mesh,
        fieldfile=folder + "/concentration_continuity/mobile.xdmf",
        field="mobile_concentration",
    )

    max_retention = max(
        retention_concentration.vector().max(), retention_chemical_pot.vector().max()
    )
    max_mobile = max(
        mobile_concentration.vector().max(), mobile_chemical_pot.vector().max()
    )
    make_figure(retention_chemical_pot, min=0, max=max_retention)
    plt.savefig("retention_chemical_pot.pdf")

    make_figure(retention_concentration, min=0, max=max_retention)
    plt.savefig("retention_concentration.pdf")

    make_figure(mobile_chemical_pot, min=0, max=max_mobile)
    plt.savefig("mobile_chemical_pot.pdf")

    make_figure(mobile_concentration, min=0, max=max_mobile)
    plt.savefig("mobile_concentration.pdf")

    make_figure(mobile_concentration)
    plt.savefig("mobile_concentration_real_colourbar.pdf")

    retention_chemical_pot_small_t = load_field(
        mesh,
        fieldfile=folder + "/chemical_potential_continuity/retention.xdmf",
        field="retention",
        counter=4,
    )
    retention_concentration_small_t = load_field(
        mesh,
        fieldfile=folder + "/concentration_continuity/retention.xdmf",
        field="retention",
        counter=4,
    )

    make_figure(retention_chemical_pot_small_t)
    plt.savefig("retention_chemical_pot_short_exposure.pdf")

    make_figure(retention_concentration_small_t)
    plt.savefig("retention_concentration_short_exposure.pdf")
