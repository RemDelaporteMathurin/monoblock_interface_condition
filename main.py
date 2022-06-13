import FESTIM as F

id_w = 8
id_cu = 7
id_cucrzr = 6

id_top_surf = 9
id_coolant_surf = 10
id_left_surf = 11


model = F.Simulation()


# materials


def thermal_cond_W(T):
    return -7.84154e-9 * T**3 + 5.03006e-5 * T**2 - 1.07335e-1 * T + 1.75214e2


def thermal_cond_Cu(T):
    return -3.93153e-08 * T**3 + 3.76147e-05 * T**2 - 7.88669e-02 * T + 4.02301e02


def thermal_cond_CuCrZr(T):
    return 5.25780e-7 * T**3 - 6.45110e-4 * T**2 + 2.57678e-01 * T + 3.12969e2


# atom_density  =  density(g/m3)*Na(/mol)/M(g/mol)
atom_density_W = 6.28e28  # 6.3222e28  # atomic density m^-3
atom_density_Cu = 8.43e28  # 8.4912e28  # atomic density m^-3
atom_density_CuCrZr = 2.6096e28  # atomic density m^-3

tungsten = F.Material(
    id=id_w, D_0=1.9e-7, E_D=0.2, S_0=1.87e24, E_S=1.04, thermal_cond=thermal_cond_W
)
cu = F.Material(
    id=id_cu, D_0=6.6e-7, E_D=0.39, S_0=3.14e24, E_S=0.57, thermal_cond=thermal_cond_Cu
)
cucrzr = F.Material(
    id=id_cucrzr,
    D_0=3.9e-7,
    E_D=0.42,
    S_0=4.28e23,
    E_S=0.39,
    thermal_cond=thermal_cond_CuCrZr,
)

model.materials = F.Materials([tungsten, cu, cucrzr])

# traps

# trap_w1 = F.Trap(
#     8.96e-17, 0.2, 1e13, 0.87, materials=tungsten, density=1.1e-3 * atom_density_W
# )
trap_w2 = F.Trap(
    8.96e-17, 0.2, 1e13, 1, materials=tungsten, density=4e-4 * atom_density_W
)
# trap_cu = F.Trap(
#     6.0e-17, 0.39, 8.0e13, 0.50, materials=cu, density=5.0e-5 * atom_density_Cu
# )
# trap_cucrzr = F.Trap(
#     1.2e-16, 0.42, 8.0e13, 0.85, materials=cucrzr, density=5.0e-5 * atom_density_CuCrZr
# )

trap_conglo = F.Trap(
    k_0=[8.96e-17, 6.0e-17, 1.2e-16],
    E_k=[0.2, 0.39, 0.42],
    p_0=[1e13, 8e13, 8e13],
    E_p=[0.87, 0.5, 0.85],
    materials=[tungsten, cu, cucrzr],
    density=[
        1.1e-3 * atom_density_W,
        5.0e-5 * atom_density_Cu,
        5.0e-5 * atom_density_CuCrZr,
    ],
)

# model.traps = F.Traps([trap_w1, trap_w2, trap_cu, trap_cucrzr])
model.traps = F.Traps([trap_conglo, trap_w2])

# mesh

model.mesh = F.MeshFromXDMF("mesh/mesh_domains.xdmf", "mesh/mesh_boundaries.xdmf")

# boundary conditions

top_H_exposure = F.ImplantationDirichlet(
    surfaces=id_top_surf, phi=1.6e22, R_p=1e-9, D_0=tungsten.D_0, E_D=tungsten.E_D
)
top_heat_flux = F.FluxBC(id_top_surf, 10e6, field="T")

instant_recomb_left = F.DirichletBC(surfaces=id_left_surf, value=0, field=0)

coolant_recomb = F.RecombinationFlux(
    Kr_0=2.9e-14, E_Kr=1.92, order=2, surfaces=id_coolant_surf
)

# the sign in the convective flux is wrong!! need v0.10 to fix it
coolant_convection = F.ConvectiveFlux(h_coeff=-7e4, T_ext=323, surfaces=id_coolant_surf)

heat_transfer_bcs = [top_heat_flux, coolant_convection]
h_transport_bcs = [top_H_exposure, coolant_recomb, instant_recomb_left]

model.boundary_conditions = h_transport_bcs + heat_transfer_bcs


# temperature

model.T = F.HeatTransferProblem(transient=False)

# settings

model.settings = F.Settings(
    absolute_tolerance=1e8,
    relative_tolerance=1e-10,
    final_time=2e7,
    chemical_pot=True,
    traps_element_type="DG",
)


model.dt = F.Stepsize(initial_value=1e4, stepsize_change_ratio=1.1, dt_min=1e2)

# exports
derived_quantities = F.DerivedQuantities(
    [
        F.TotalVolume(field, mat.id)
        for field in ["retention", "solute"]
        for mat in [tungsten, cu, cucrzr]
    ]
    + [F.TotalVolume("2", tungsten.id)]
    + [F.TotalVolume("1", mat.id) for mat in [tungsten, cu, cucrzr]]
    + [F.SurfaceFlux(field="solute", surface=id_coolant_surf)]
)

if __name__ == "__main__":
    model.initialise()
    model.run()
