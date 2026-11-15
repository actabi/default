"""Socle pour moulin à sel + moulin à poivre — génère socle_moulins.stl
Modifier les paramètres ci-dessous puis : python3 socle.py"""
import numpy as np, manifold3d as m3, trimesh

# ---------------- paramètres (mm) ----------------
D_MOULIN   = 55.5   # diamètre max de la base des moulins (mesuré : 55,48)
JEU        = 1.25   # jeu radial autour du moulin
PAROI      = 4.0    # épaisseur paroi extérieure (hors anneaux)
ENTRE      = 5.0    # épaisseur entre les deux logements
FOND       = 4.0    # épaisseur du fond
PROF       = 14.0   # profondeur des logements
N_ANNEAUX  = 3      # nombre d'anneaux décoratifs
BOMBE      = 2.2    # relief des anneaux
CUVETTE_D  = 34.0   # diamètre de la cuvette récupératrice
CUVETTE_P  = 2.0    # profondeur de la cuvette
# -------------------------------------------------
Rc = D_MOULIN/2 + JEU
H  = FOND + PROF
dx = Rc + ENTRE/2            # demi-entraxe
R0 = Rc + PAROI              # rayon extérieur de base

def stadium(r, n=96):
    a = np.linspace(-np.pi/2, np.pi/2, n)
    right = np.c_[dx + r*np.cos(a), r*np.sin(a)]
    left  = np.c_[-dx - r*np.cos(a), -r*np.sin(a)]
    return np.r_[right, left]

# corps : empilement de contours, anneaux = arches de sinus (surplomb ~45°, sans supports)
hz = H / N_ANNEAUX
zs = np.linspace(0, H, N_ANNEAUX*40 + 1)
rings = [np.c_[stadium(R0 + BOMBE*abs(np.sin(np.pi*z/hz))), np.full(192, z)] for z in zs]
n = 192
V = np.vstack(rings + [[[0,0,0]], [[0,0,H]]])
F = []
for i in range(len(zs)-1):
    for j in range(n):
        a, b = i*n+j, i*n+(j+1)%n
        F += [[a, b, b+n], [a, b+n, a+n]]
cb, ct, top = len(zs)*n, len(zs)*n+1, (len(zs)-1)*n
for j in range(n):
    F += [[cb, (j+1)%n, j], [ct, top+j, top+(j+1)%n]]
body = m3.Manifold(m3.Mesh(V.astype(np.float32), np.array(F, dtype=np.uint32)))

# logement : profil de révolution (r, z)
def cup():
    p = [(0, H+1), (Rc+1.2, H+1), (Rc+1.2, H), (Rc, H-1.2)]           # chanfrein d'entrée
    f = 1.5                                                             # congé de fond
    p += [(Rc-f+f*np.cos(t), FOND+f-f*np.sin(t)) for t in np.linspace(0, np.pi/2, 10)]
    rc = CUVETTE_D/2; Rs = (rc**2 + CUVETTE_P**2)/(2*CUVETTE_P)        # cuvette sphérique
    t0 = np.arcsin(rc/Rs)
    p += [(Rs*np.sin(t), FOND+Rs-CUVETTE_P-Rs*np.cos(t)) for t in np.linspace(t0, 0.001, 24)]
    p += [(0, FOND-CUVETTE_P)]
    return m3.Manifold.revolve(m3.CrossSection([p[::-1]]), 128)

c = cup()
res = body - c.translate((dx,0,0)) - c.translate((-dx,0,0))
mesh = res.to_mesh()
tm = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
tm.export("socle_moulins.stl")
print("étanche:", tm.is_watertight, "| dimensions:", tm.extents.round(1), "| volume cm3:", round(tm.volume/1000,1))
