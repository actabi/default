"""Étui de téléphone pour trépied (vis photo 1/4"-20), usage en paysage :
le téléphone se glisse dans l'étui par le côté et reste tenu sur 5 côtés.
Un seul filetage, sur le chant gauche du téléphone (le dessous en paysage), centré sous lui.
Génère etui_trepied.stl — imprimer debout, butée (fond) sur le plateau, sans supports."""
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
JEU_FIL  = 0.35   # jeu radial du filetage imprimé (axe horizontal à l'impression)
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
# bossage fileté sur le chant gauche (côté sans boutons) : c'est le dessous en paysage
EPB = 9.0                                   # surépaisseur du bossage
zc = top - 13                               # vis placée près du centre de gravité du téléphone
pts = [(-COTE+0.01, zc-13-EPB), (-COTE+0.01, zc+13), (-COTE-EPB, zc+13), (-COTE-EPB, zc-13)]   # dessous à 45°
cs = m3.CrossSection([pts])
if cs.area() <= 0: cs = m3.CrossSection([pts[::-1]])
Ly = s + DOS + AVANT
body += m3.Manifold.extrude(cs, Ly).rotate((90,0,0)).translate((0, s+DOS, 0))

PAS = 25.4/20
r_max, r_min = 6.35/2 + JEU_FIL, 5.1/2 + JEU_FIL
rc, e = (r_max+r_min)/2, (r_max-r_min)/2
tours = PROF_FIL/PAS
tap = m3.Manifold.extrude(m3.CrossSection.circle(rc, 48).translate((e,0)), PROF_FIL, int(tours*36), 360*tours)
tap += m3.Manifold.cylinder(1.2, r_max+0.8, r_max-0.4, 48)
body -= tap.rotate((0,90,0)).translate((-COTE-EPB-0.001, s/2, zc))     # filetage centré sous le téléphone
mesh = body.to_mesh()
tm = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
tm.export("etui_trepied.stl")
if __name__ == "__main__":
    print("étanche:", tm.is_watertight, "| corps:", len(tm.split()), "| bornes:", tm.bounds.round(1).tolist(), "| volume cm3:", round(tm.volume/1000,1))
