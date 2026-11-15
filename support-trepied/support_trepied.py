"""Berceau de téléphone à visser sur un trépied (vis photo 1/4"-20, ex. Manfrotto PIXI)
Génère support_trepied.stl — imprimer debout, base sur le plateau, sans supports.
Modifier les paramètres puis : python3 support_trepied.py"""
import numpy as np, manifold3d as m3, trimesh

# ---------------- paramètres (mm) ----------------
EP_TEL   = 11.6   # épaisseur téléphone + coque
JEU      = 0.8    # jeu total dans la rainure
LARGEUR  = 80.0   # longueur du berceau
H_DOS    = 60.0   # hauteur de la paroi arrière au-dessus du fond
H_AVANT  = 12.0   # hauteur du rebord avant
BASE     = 10.0   # épaisseur de la base (contient le filetage)
PROF_B   = 30.0   # profondeur de la base (appui sur la platine du trépied)
JEU_FIL  = 0.30   # jeu radial du filetage imprimé
PROF_FIL = 8.5    # profondeur du filetage
# -------------------------------------------------
s = EP_TEL + JEU
x0 = (PROF_B - s)/2; x1 = x0 + s            # rainure centrée sur la vis
av, ar = 4.0, 5.0                           # épaisseurs des parois
prof = [(0,0),(PROF_B,0),(PROF_B,BASE-3),(x1+ar,BASE+1),(x1+ar,BASE+H_DOS-2),(x1+ar-2,BASE+H_DOS),
        (x1+1,BASE+H_DOS),(x1,BASE+H_DOS-1),(x1,BASE),(x0,BASE),(x0,BASE+H_AVANT-1),(x0-1,BASE+H_AVANT),
        (x0-av+1,BASE+H_AVANT),(x0-av,BASE+H_AVANT-1),(x0-av,BASE+1),(0,BASE-3)]
body = m3.Manifold.extrude(m3.CrossSection([prof]), LARGEUR)            # profil (x,z) extrudé selon y
body = body.rotate((90,0,0)).translate((0,LARGEUR,0))                   # -> debout : x profondeur, y longueur, z haut

# filetage intérieur 1/4"-20 UNC, pas à droite : cercle excentré extrudé en hélice
PAS = 25.4/20
r_max, r_min = 6.35/2 + JEU_FIL, 5.1/2 + JEU_FIL
rc, e = (r_max+r_min)/2, (r_max-r_min)/2
tours = PROF_FIL/PAS
tap = m3.Manifold.extrude(m3.CrossSection.circle(rc, 48).translate((e,0)), PROF_FIL, int(tours*36), 360*tours)
entree = m3.Manifold.cylinder(1.2, r_max+0.8, r_max-0.4, 48)            # chanfrein d'entrée
res = body - (tap + entree).translate((PROF_B/2, LARGEUR/2, -0.001))
mesh = res.to_mesh()
tm = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
tm.export("support_trepied.stl")
if __name__ == "__main__":
    print("étanche:", tm.is_watertight, "| corps:", len(tm.split()), "| dimensions:", tm.extents.round(1), "| volume cm3:", round(tm.volume/1000,1))
    print(f"rainure {s:.1f} mm | filetage Ø{2*r_min:.2f}–{2*r_max:.2f}, pas {PAS:.2f}")
