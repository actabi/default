"""Étui de téléphone pour trépied (vis photo 1/4"-20) : le téléphone se glisse par le haut
et reste tenu sur 5 côtés, trépied penché ou basculé à 90°.
Deux filetages : sous l'étui (portrait) et sur le côté (paysage).
Génère etui_trepied.stl — imprimer debout, fond sur le plateau, sans supports."""
import numpy as np, manifold3d as m3, trimesh

# ---------------- paramètres (mm) ----------------
L_TEL    = 82.27  # largeur du téléphone avec coque (mesurée)
EP_TEL   = 11.97  # épaisseur avec coque (mesurée)
JEU      = 0.8    # jeu total en largeur et en épaisseur
H_POCHE  = 86.0   # hauteur de l'étui : le bouton le plus bas commence à 92,65 mm
LEVRE    = 5.0    # recouvrement des bords de l'écran
H_BAS    = 6.0    # hauteur du rebord avant en bas
FOND, COTE, DOS, AVANT = 4.0, 3.0, 4.0, 3.0   # épaisseurs
CABLE    = 18.0   # passage de câble (fiche USB-C mesurée : 15,71)
JEU_FIL  = 0.30   # jeu radial des filetages imprimés
PROF_FIL = 8.5
# -------------------------------------------------
Wi, s, top = L_TEL + JEU, EP_TEL + JEU, FOND + H_POCHE
def box(x0, x1, y0, y1, z0, z1):
    return m3.Manifold.cube((x1-x0, y1-y0, z1-z0)).translate((x0, y0, z0))
# x : largeur, y : avant (-) -> arrière (+), z : haut
body = box(-COTE, Wi+COTE, -AVANT, s+DOS, 0, top)
body -= box(0, Wi, 0, s, FOND, top+1)                                 # poche
body -= box(LEVRE, Wi-LEVRE, -AVANT-1, 0.01, FOND+H_BAS, top+1)       # fenêtre écran
body -= box(Wi/2-CABLE/2, Wi/2+CABLE/2, -AVANT-1, s, -1, FOND+H_BAS+1)  # passage câble
yb = s + DOS
body += box(Wi/2-13, Wi/2+13, yb, yb+16, 0, 12)                       # bossage bas (portrait)
zc = FOND + H_POCHE/2
tri = [(yb-0.01, zc-12-16), (yb+16, zc-12), (yb+16, zc+12), (yb-0.01, zc+12)]   # dessous à 45°
cote = m3.Manifold.extrude(m3.CrossSection([tri]), 13)                # profil (y,z) extrudé
cote = cote.rotate((90,0,0)).rotate((0,0,90)).translate((Wi+COTE-13, 0, 0))   # -> le long de x, côté droit
body += cote

PAS = 25.4/20
r_max, r_min = 6.35/2 + JEU_FIL, 5.1/2 + JEU_FIL
rc, e = (r_max+r_min)/2, (r_max-r_min)/2
tours = PROF_FIL/PAS
tap = m3.Manifold.extrude(m3.CrossSection.circle(rc, 48).translate((e,0)), PROF_FIL, int(tours*36), 360*tours)
tap += m3.Manifold.cylinder(1.2, r_max+0.8, r_max-0.4, 48)
body -= tap.translate((Wi/2, yb+8, -0.001))                           # filetage dessous
body -= tap.rotate((0,-90,0)).translate((Wi+COTE+0.001, yb+8, zc))    # filetage côté
mesh = body.to_mesh()
tm = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
tm.export("etui_trepied.stl")
if __name__ == "__main__":
    print("étanche:", tm.is_watertight, "| corps:", len(tm.split()), "| bornes:", tm.bounds.round(1).tolist(), "| volume cm3:", round(tm.volume/1000,1))
