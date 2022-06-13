from main import model, derived_quantities, top_H_exposure, top_heat_flux
import FESTIM as F


top_H_exposure.phi = 1e21  # H/m2/s
top_heat_flux.value = 5e6  # W/m2

folder_1 = "results/phi_heat={:.1e}_phi_imp={:.1e}".format(
    top_heat_flux.value, top_H_exposure.phi
)

# chemical pot
folder = folder_1 + "/chemical_potential_continuity"

xdmf_exports = [
    F.XDMFExport("T", filename=folder + "/T.xdmf", mode="last"),
    F.XDMFExport("retention", filename=folder + "/retention.xdmf", mode=2),
    *[
        F.XDMFExport(
            str(i + 1), filename=folder + "/trap_{}.xdmf".format(i + 1), mode=2
        )
        for i in range(len(model.traps.traps))
    ],
    F.XDMFExport("solute", filename=folder + "/mobile.xdmf", mode=2),
]
derived_quantities.filename = folder + "/derived_quantities.csv"
model.exports = F.Exports([derived_quantities, *xdmf_exports])
model.t = 0  # for version <0.10 we need to manually reset t to zero
model.dt = F.Stepsize(initial_value=1e4, stepsize_change_ratio=1.1, dt_min=1e2)
model.initialise()
model.run()

# concentration continuity
for mat in model.materials.materials:
    mat.S_0 = None
    mat.E_S = None

model.t = 0  # for version <0.10 we need to manually reset t to zero
model.dt = F.Stepsize(initial_value=1e4, stepsize_change_ratio=1.1, dt_min=1e2)

model.settings.chemical_pot = False
folder = folder_1 + "/concentration_continuity"
xdmf_exports = [
    F.XDMFExport("T", filename=folder + "/T.xdmf", mode="last"),
    F.XDMFExport("retention", filename=folder + "/retention.xdmf", mode=2),
    *[
        F.XDMFExport(
            str(i + 1), filename=folder + "/trap_{}.xdmf".format(i + 1), mode=2
        )
        for i in range(len(model.traps.traps))
    ],
    F.XDMFExport("solute", filename=folder + "/mobile.xdmf", mode=2),
]
derived_quantities.filename = folder + "/derived_quantities.csv"
model.exports = F.Exports([derived_quantities, *xdmf_exports])
model.initialise()
model.run()
