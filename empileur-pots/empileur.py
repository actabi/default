"""Bague d'empilage pour pots de yaourt en verre (type La Laitière) — génère empileur_pots.stl
Réversible : un cône reçoit le fond d'un pot, l'autre reçoit le bord (col) de l'autre pot.
Modifier les paramètres puis : python3 empileur.py"""
import numpy as np, manifold3d as m3, trimesh

# ---------------- paramètres (mm) ----------------
D_COL   = 58.0   # diamètre extérieur du bord (col) du pot   <-- estimé, à mesurer
D_FOND  = 44.0   # diamètre du fond plat du pot              <-- estimé, à mesurer
MARGE   = 4.0    # tolérance : chaque cône accepte ±MARGE autour de la mesure
H_FOND  = 8.0    # hauteur du cône côté fond
H_COL   = 6.0    # hauteur du cône côté col
BOMBE   = 1.0    # relief de l'anneau extérieur
# -------------------------------------------------
H = H_FOND + H_COL
r_trou = D_FOND/2 - 1.0                 # trou central (le fond ne passe pas à travers)
r_f0   = r_trou + H_FOND - 1.2                # cône fond : 45°, s'ouvre vers le bas
r_c0   = D_COL/2 - MARGE                # cône col : 45°, s'ouvre vers le haut
r_c1   = r_c0 + H_COL
r_ext  = max(r_f0, r_c1) + 2.0

inner = [(r_f0, 0), (r_trou, H_FOND-1.2), (r_trou, H_FOND), (r_c0, H_FOND), (r_c1, H)]
outer = [(r_ext + BOMBE*np.sin(np.pi*z/H), z) for z in np.linspace(H, 0, 40)]
ring = m3.Manifold.revolve(m3.CrossSection([(inner + outer)[::-1]]), 160)
mesh = ring.to_mesh()
tm = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
if tm.volume < 0: tm.invert()
tm.export("empileur_pots.stl")
print("étanche:", tm.is_watertight, "| dimensions:", tm.extents.round(1), "| volume cm3:", round(tm.volume/1000, 1))
print(f"cône fond: Ø{2*r_trou:.0f}→Ø{2*r_f0:.0f} | cône col: Ø{2*r_c0:.0f}→Ø{2*r_c1:.0f}")
