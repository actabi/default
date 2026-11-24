"""Porte-rouleau de papier toilette mural, à bras ouvert — génère porte_papier.stl
Le rouleau s'enfile par le côté libre du bras, sans rien démonter.
Impression : dans le sens d'utilisation (dessous sur le plateau), sans supports ;
les couches suivent le L platine-bras, donc le bras ne peut pas se délaminer à la racine.
Modifier les paramètres puis : python3 porte_papier.py"""
import numpy as np, manifold3d as m3, trimesh

# ---------------- paramètres (mm) ----------------
L_ROULEAU = 100.0  # largeur du rouleau
R_ROULEAU = 65.0   # rayon maxi du rouleau (rouleaux « maxi » ≈ 60-65)
T         = 12.0   # épaisseur du bras et de l'entretoise
H         = 22.0   # hauteur du bras
ERGOT     = 7.0    # hauteur de l'ergot anti-chute en bout de bras
PLATINE   = (70.0, 72.0, 6.0)   # largeur, hauteur, épaisseur de la platine murale
D_VIS     = 4.6    # passage des vis (vis de 4 mm à tête fraisée)
D_TETE    = 9.0    # diamètre de la fraisure
BRAS_A_DROITE = False  # False : face au mur, le bras part vers la gauche ; True : version miroir
# -------------------------------------------------
PW, PH, PT = PLATINE
y_axe = PT + R_ROULEAU + 14 - T/2          # le rouleau plein reste à 14 mm du mur
y0, y1 = y_axe - T/2, y_axe + T/2          # bras : y0..y1 (y = distance au mur)
x_fin = T + 8 + L_ROULEAU + 6 + 10         # entretoise + marge + rouleau + marge + ergot

def rect(x0, x1, ya, yb):
    return m3.CrossSection([[(x0,ya),(x1,ya),(x1,yb),(x0,yb)]])
def box(x0, x1, ya, yb, z0, z1):
    return m3.Manifold.cube((x1-x0, yb-ya, z1-z0)).translate((x0, ya, z0))
def arrondi(cs, r):                        # arrondit angles saillants puis rentrants
    J = m3.JoinType.Round
    return cs.offset(-r, J, 2.0, 64).offset(2*r, J, 2.0, 64).offset(-r, J, 2.0, 64)

plan = arrondi(rect(0, T, -8, y1) + rect(0, x_fin, y0, y1), T/2 - 0.5)   # L vu de dessus
plan = plan - rect(-50, 300, -50, 0)                                    # coupe nette au mur
# profil du bras (y,z) à dessus arrondi, extrudé le long de x
def profil(h, n=24):
    a = np.linspace(0, np.pi, n)
    return [(y0, 0), (y1, 0)] + [(y_axe + T/2*np.cos(t), h - T/2 + T/2*np.sin(t)) for t in a]
def barre(h, xa, xb):
    return m3.Manifold.extrude(m3.CrossSection([profil(h)]), xb-xa).rotate((90,0,0)).rotate((0,0,90)).translate((xa,0,0))
bras = box(0, T+6, -1, y1+1, 0, H) + barre(H, T+6, x_fin)               # dessus plat à la racine, arrondi ensuite
rampe = m3.Manifold.batch_hull([barre(H, x_fin-19, x_fin-18.9), barre(H+ERGOT, x_fin-10, x_fin-9.9)])
bras += rampe + barre(H+ERGOT, x_fin-10, x_fin)
corps = m3.Manifold.extrude(plan, H+ERGOT+1) ^ bras                     # ^ = intersection

# platine murale, coins hauts arrondis
r = 10
pp = [(0,0),(PW,0),(PW,PH-r)] + [(PW-r+r*np.cos(t), PH-r+r*np.sin(t)) for t in np.linspace(0,np.pi/2,16)] \
   + [(r+r*np.cos(t), PH-r+r*np.sin(t)) for t in np.linspace(np.pi/2,np.pi,16)] + [(0,PH-r)]
platine = m3.Manifold.extrude(m3.CrossSection([pp]), PT).rotate((90,0,0)).translate((0,PT,0))
# gousset à 45° entre platine et entretoise
g = [(PT-0.5, H-0.5), (PT+38, H-0.5), (PT-0.5, H+38)]
gousset = m3.Manifold.extrude(m3.CrossSection([g]), T).rotate((90,0,0)).rotate((0,0,90))
corps += platine + gousset

# deux vis fraisées, au-dessus du bras pour laisser passer le tournevis
def vis(x, z):
    trou = m3.Manifold.cylinder(PT+2, D_VIS/2, D_VIS/2, 40).translate((0,0,-1))
    fraise = m3.Manifold.cylinder((D_TETE-D_VIS)/2+0.01, D_VIS/2, D_TETE/2, 40).translate((0,0,PT-(D_TETE-D_VIS)/2))
    return (trou + fraise).rotate((-90,0,0)).translate((x, 0, z))
VIS = [(30.0, 60.0), (56.0, 38.0)]
for x, z in VIS: corps -= vis(x, z)
if BRAS_A_DROITE: corps = corps.mirror((1,0,0))
mesh = corps.to_mesh()
tm = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
tm.export("porte_papier.stl")
if __name__ == "__main__":
    print("étanche:", tm.is_watertight, "| corps:", len(tm.split()), "| bornes:", tm.bounds.round(1).tolist(), "| volume cm3:", round(tm.volume/1000,1))
    print(f"axe du bras à {y_axe:.0f} mm du mur | longueur utile {L_ROULEAU+14:.0f} mm")
