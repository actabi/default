"""Support de téléphone (Galaxy S26+ ou autre) — génère support_telephone.stl
Imprimer couché sur le flanc (profil à plat sur le plateau), sans supports.
Modifier les paramètres puis : python3 support.py"""
import numpy as np, manifold3d as m3, trimesh

# ---------------- paramètres (mm) ----------------
EP_TEL   = 13.0   # épaisseur max acceptée (téléphone + coque) ; S26+ nu ≈ 7,3
ANGLE    = 70.0   # inclinaison de l'écran par rapport à la table (degrés)
LARGEUR  = 70.0   # largeur du support
T        = 6.0    # épaisseur des montants
H_BERCEAU= 30.0   # hauteur du bas du téléphone (place pour la prise USB-C)
DOSSIER  = 90.0   # longueur du dossier
LEVRE    = 12.0   # hauteur du rebord avant
ENCOCHE  = 18.0   # largeur du passage de câble
# -------------------------------------------------
a = np.radians(ANGLE)
u = np.array([np.cos(a), np.sin(a)])          # le long du téléphone, vers le haut
v = np.array([-np.sin(a), np.cos(a)])         # vers l'avant, perpendiculaire à l'écran
r = T/2
P0 = np.array([32.0, H_BERCEAU])              # angle dossier / fond du berceau
P1 = P0 + DOSSIER*u                           # haut du dossier
P2 = P0 + (EP_TEL + 1 + T)*v                  # angle fond / rebord
P3 = P2 + LEVRE*u                             # haut du rebord
x_ar = P1[0] + 32                             # pied arrière
segs = [(P0, P1), (P0, P2), (P2, P3),                       # dossier, fond, rebord
        ((P2[0]-3, r), (x_ar, r)),                          # semelle
        (P2, (P2[0]-3, r)), (P0, (P0[0]+2, r)),             # jambes avant
        (P1, (x_ar, r))]                                    # jambe arrière
def stroke(p, q):
    c = m3.CrossSection.circle(r, 48)
    return m3.CrossSection.batch_hull([c.translate(tuple(map(float, p))), c.translate(tuple(map(float, q)))])
prof = stroke(*segs[0])
for s in segs[1:]: prof = prof + stroke(*s)
body = m3.Manifold.extrude(prof, LARGEUR)

# passage de câble : fente dans l'axe de la prise, au milieu de la largeur
M = (P0 + P2)/2
w = EP_TEL/2 + 0.5
quad = [M + 6*u - w*v, M + 6*u + w*v, M - 60*u + w*v, M - 60*u - w*v]
cs = m3.CrossSection([[tuple(map(float, p)) for p in quad]])
if cs.area() <= 0: cs = m3.CrossSection([[tuple(map(float, p)) for p in quad][::-1]])
cut = m3.Manifold.extrude(cs, ENCOCHE).translate((0, 0, (LARGEUR-ENCOCHE)/2))
res = body - cut
mesh = res.to_mesh()
tm = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
tm.export("support_telephone.stl")
print("étanche:", tm.is_watertight, "| corps:", len(tm.split()), "| dimensions:", tm.extents.round(1), "| volume cm3:", round(tm.volume/1000, 1))
