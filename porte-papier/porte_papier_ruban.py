"""Porte-rouleau « ruban » : une seule bande continue qui part du mur, se retourne
en courbe douce et devient le bras. Vis cachées derrière le rouleau.
Génère deux fichiers miroir (bout ouvert à gauche ou à droite) — imprimer dans le sens d'utilisation, sans supports.
Modifier les paramètres puis : python3 porte_papier_ruban.py"""
import numpy as np, manifold3d as m3, trimesh

# ---------------- paramètres (mm) ----------------
L_ROULEAU = 100.0  # largeur du rouleau
R_ROULEAU = 65.0   # rayon maxi du rouleau
T         = 10.0   # épaisseur du ruban
H         = 32.0   # hauteur du ruban
CONGE     = 4.5    # arrondi des arêtes du dessus
ERGOT     = 6.0    # relevé en bout de bras (anti-chute)
N_SQ      = 2.6    # forme de la courbe : 2 = demi-cercle, plus = « squircle »
D_VIS, D_TETE, D_ACCES = 4.6, 9.0, 7.5   # vis de 4 fraisées ; trous d'accès tournevis dans le bras
# -------------------------------------------------
J = m3.JoinType.Round
b = (T + R_ROULEAU + 3 + T) / 2            # demi-profondeur : un rouleau plein passe devant la patte murale
a = b                                       # demi-axe de la courbe le long du mur
x_r0 = a + 4                                # début du rouleau
x_fin = x_r0 + L_ROULEAU + 6 + 10           # bout du bras
x_pat = a + 105                             # bout de la patte murale
def rect(x0, x1, y0, y1): return m3.CrossSection([[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]])
sp = lambda v, e: np.sign(v)*abs(v)**e
th = np.linspace(np.pi/2, 3*np.pi/2, 160)
courbe = [(a + a*sp(np.cos(t), 2/N_SQ), b + b*sp(np.sin(t), 2/N_SQ)) for t in th]
plein = m3.CrossSection([courbe[::-1]]) 
if plein.area() <= 0: plein = m3.CrossSection([courbe])
plein = plein + rect(a-0.01, x_fin, 0, 2*b)
creux = plein.offset(-T, J, 2.0, 96) + rect(a, x_fin+20, T, 2*b-T)
ruban = plein - creux - rect(x_pat, x_fin+20, -1, b)             # patte murale plus courte que le bras
r = T/2 - 0.6
ruban = ruban.offset(-r, J, 2.0, 64).offset(r, J, 2.0, 64)       # bouts arrondis

def volume(masque, h):
    """Extrusion à arêtes hautes arrondies et petit chanfrein au sol, limitée au masque."""
    niv = [(0, 0.5, 0.5), (0.5, h-CONGE, 0.0)]
    zs = np.linspace(0, np.pi/2, 13)
    for t0, t1 in zip(zs[:-1], zs[1:]):
        niv.append((h-CONGE+CONGE*np.sin(t0), h-CONGE+CONGE*np.sin(t1), CONGE*(1-np.cos((t0+t1)/2))))
    out = m3.Manifold()
    for z0, z1, d in niv:
        cs = (ruban.offset(-d, J, 2.0, 48) if d > 0 else ruban) ^ masque
        out += m3.Manifold.extrude(cs, z1-z0).translate((0, 0, z0))
    return out
xa, xb = x_fin-24, x_fin-11                                      # rampe douce vers l'ergot
corps = volume(rect(-5, xa, -5, 2*b+5), H)
n = 26
for k in range(n):
    u = (k+0.5)/n; s = u*u*(3-2*u)
    corps += volume(rect(xa+(xb-xa)*k/n, xa+(xb-xa)*(k+1)/n, b, 2*b+5), H+ERGOT*s)
corps += volume(rect(xb, x_fin+5, b, 2*b+5), H+ERGOT)

def cyl(d, y0, y1, x, z):
    return m3.Manifold.cylinder(y1-y0, d/2, d/2, 48).rotate((-90,0,0)).translate((x, y0, z))
for x in (a+22, a+86):
    z = H/2
    corps -= cyl(D_VIS, -1, T+1, x, z)
    k = (D_TETE-D_VIS)/2
    corps -= m3.Manifold.cylinder(k+0.02, D_VIS/2, D_TETE/2+0.02, 48).rotate((-90,0,0)).translate((x, T-k, z))
    corps -= cyl(D_ACCES, 2*b-T-1, 2*b+1, x, z)                  # passage du tournevis à travers le bras
def exporte(m, nom):
    mesh = m.to_mesh()
    t = trimesh.Trimesh(mesh.vert_properties[:, :3], mesh.tri_verts)
    t.export(nom); return t
# deux fichiers : face au mur, le bout ouvert (et son relevé anti-chute) à gauche ou à droite
tm = exporte(corps, "porte_papier_ruban_ouvert_a_gauche.stl")
tm_d = exporte(corps.mirror((1,0,0)), "porte_papier_ruban_ouvert_a_droite.stl")
y_axe = 2*b - T/2
if __name__ == "__main__":
    print("droite étanche:", tm_d.is_watertight, "| volume:", round(tm_d.volume/1000,1))
    print("étanche:", tm.is_watertight, "| corps:", len(tm.split()), "| bornes:", tm.bounds.round(1).tolist(), "| volume cm3:", round(tm.volume/1000,1))
