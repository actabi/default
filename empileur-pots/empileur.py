"""Bague d'empilage pour pots de yaourt en verre (La Laitière) — génère empileur_pots.stl
Pots rangés retournés : le côté "logement fond" coiffe le fond du pot du bas,
le côté "logement bord" reçoit la lèvre du pot du haut.
Impression : logement bord sur le plateau, sans supports.
Modifier les paramètres puis : python3 empileur.py"""
import numpy as np, manifold3d as m3, trimesh

# ---------------- cotes mesurées du pot (mm) ----------------
A_BORD   = 55.60   # diamètre extérieur de la lèvre
C_LEVRE  = 3.85    # hauteur de la lèvre
E_VENTRE = 59.24   # diamètre maximal du ventre (à 13,8 mm du fond)
F_FOND   = 44.50   # diamètre du fond plat
# ---------------- réglages ----------------
JEU_BORD  = 0.7    # jeu radial autour de la lèvre
JEU_FOND  = 0.7    # jeu radial autour du fond
PROF_FOND = 11.0   # profondeur du logement qui coiffe le fond
PAROI     = 2.4    # épaisseur de paroi
BOMBE     = 1.0    # relief de l'anneau extérieur
# -------------------------------------------
r_b   = A_BORD/2 + JEU_BORD          # logement lèvre
h_b   = C_LEVRE - 0.85               # partie droite du logement lèvre
r_t   = F_FOND/2 - 3.25              # trou central (le fond plat repose autour)
z_pl  = h_b + (r_b - r_t) + 1.2    # toit conique à 45° + méplat de 1,2 mm
r_f   = E_VENTRE/2 + JEU_FOND        # logement fond
H     = z_pl + PROF_FOND
r_ext = r_f + PAROI

inner = [(r_b+0.6, 0), (r_b, 0.6), (r_b, h_b), (r_t, z_pl-1.2), (r_t, z_pl), (r_f, z_pl), (r_f, H-0.8), (r_f+0.8, H)]
outer = [(r_ext + BOMBE*np.sin(np.pi*z/H), z) for z in np.linspace(H, 0, 60)]
ring = m3.Manifold.revolve(m3.CrossSection([(inner + outer)[::-1]]), 180)
mesh = ring.to_mesh()
tm = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
tm.export("empileur_pots.stl")
print("étanche:", tm.is_watertight, "| dimensions:", tm.extents.round(1), "| volume cm3:", round(tm.volume/1000, 1))
print(f"logement lèvre Ø{2*r_b:.1f} | logement fond Ø{2*r_f:.1f} prof. {PROF_FOND} | trou Ø{2*r_t:.1f} | écart entre pots {z_pl:.1f} mm")
