"""Capuchon à clipser sur un pot de yaourt en verre (La Laitière) — génère capuchon_pot.stl
Un bourrelet intérieur passe sous la lèvre du pot et retient le capuchon.
Impression : à l'envers, le dessus du capuchon sur le plateau, sans supports.
Modifier les paramètres puis : python3 capuchon.py"""
import numpy as np, manifold3d as m3, trimesh

# ---------------- cotes mesurées du pot (mm) ----------------
A_BORD  = 55.60   # diamètre extérieur de la lèvre
C_LEVRE = 3.85    # hauteur de la lèvre
D_COL   = 51.00   # diamètre du col sous la lèvre
# ---------------- réglages ----------------
JEU     = 0.25    # jeu radial entre la jupe et la lèvre
SERRAGE = 0.45    # dépassement radial du bourrelet sous la lèvre (force du clip)
PAROI   = 1.2     # épaisseur de la jupe (plus fin = plus souple)
DESSUS  = 1.6     # épaisseur du dessus
LANGUETTE = 9.0   # longueur de la languette d'ouverture (0 = aucune)
# -------------------------------------------
r_i = A_BORD/2 + JEU
r_o = r_i + PAROI
b   = JEU + SERRAGE                       # saillie du bourrelet
zb  = DESSUS + C_LEVRE + 0.3              # début du bourrelet, juste sous la lèvre
zt  = zb + 2*b + 0.6                      # bas de la jupe
assert r_i - b > D_COL/2, "le bourrelet toucherait le col"
prof = [(0,0), (r_o-0.4,0), (r_o,0.4), (r_o,zt), (r_i+0.3,zt), (r_i-b,zb+b+0.3), (r_i-b,zb+b), (r_i,zb), (r_i,DESSUS), (0,DESSUS)]
cap = m3.Manifold.revolve(m3.CrossSection([prof]), 200)
if LANGUETTE > 0:
    c = m3.CrossSection.circle(6, 48)
    tab = m3.CrossSection.batch_hull([c.translate((r_o-4, 0)), c.translate((r_o+LANGUETTE-6, 0))])
    cap += m3.Manifold.extrude(tab, DESSUS)
mesh = cap.to_mesh()
tm = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
tm.export("capuchon_pot.stl")
if __name__ == "__main__":
    print("étanche:", tm.is_watertight, "| corps:", len(tm.split()), "| dimensions:", tm.extents.round(1), "| volume cm3:", round(tm.volume/1000,1))
    print(f"jupe Ø int. {2*r_i:.2f} | bourrelet Ø {2*(r_i-b):.2f} (lèvre {A_BORD}) | hauteur {zt:.2f}")
