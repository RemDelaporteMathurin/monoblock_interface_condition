from main import model, derived_quantities
import FESTIM as F


folder = "results/chemical_potential_continuity"

xdmf_exports = [
    F.XDMFExport("T", filename=folder + "/T.xdmf", mode="last"),
    F.XDMFExport("retention", filename=folder + "/retention.xdmf", mode=2),
    F.XDMFExport("1", filename=folder + "/trap_1.xdmf", mode=2),
    F.XDMFExport("2", filename=folder + "/trap_2.xdmf", mode=2),
    F.XDMFExport("3", filename=folder + "/trap_3.xdmf", mode=2),
    F.XDMFExport("4", filename=folder + "/trap_4.xdmf", mode=2),
    F.XDMFExport("solute", filename=folder + "/mobile.xdmf", mode=2),
]
derived_quantities.filename = folder + "/derived_quantities.csv"
model.exports = F.Exports([derived_quantities, *xdmf_exports])

if __name__ == "__main__":
    model.initialise()
    model.run()
