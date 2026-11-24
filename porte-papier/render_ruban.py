import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import porte_papier_ruban as P
tm = trimesh.load("porte_papier_ruban_ouvert_a_gauche.stl")
sub = trimesh.Trimesh(*trimesh.remesh.subdivide_to_size(tm.vertices, tm.faces, 5))
rc, R, L = 20.0, 55.0, P.L_ROULEAU
roll = trimesh.creation.annulus(rc, R, L, sections=64)
roll.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0,1,0]))
roll.apply_translation((P.x_r0+L/2, P.y_axe, P.H-rc))
roll = trimesh.Trimesh(*trimesh.remesh.subdivide_to_size(roll.vertices, roll.faces, 5))
fig = plt.figure(figsize=(15,5.6), dpi=160)
vues = [(28,60,"Vue de trois quarts",False),(89.9,90,"Vue de dessus (mur en haut)",False),(18,52,"Avec un rouleau",True)]
for k,(el,az,t,avec) in enumerate(vues):
    ax = fig.add_subplot(1,3,k+1, projection="3d")
    cam=np.array([np.cos(np.radians(el))*np.cos(np.radians(az)),np.cos(np.radians(el))*np.sin(np.radians(az)),np.sin(np.radians(el))])
    L_=np.array([0.45,0.45,0.77]); L_/=np.linalg.norm(L_)
    tris, cols = [], []
    for m, base in [(sub,(0.93,0.93,0.94))] + ([(roll,(0.99,0.97,0.90))] if avec else []):
        keep=m.face_normals@cam>0; sh=np.clip(m.face_normals@L_,0,1)*0.55+0.42
        tris.append(m.triangles[keep]); cols.append(np.outer(sh,base)[keep])
    tris=np.vstack(tris); cols=np.c_[np.vstack(cols),np.ones(len(tris))]
    ax.add_collection3d(Poly3DCollection(tris,facecolors=cols,edgecolors=cols,linewidths=0.1))
    ax.set_xlim(-5,175);ax.set_ylim(-45,135);ax.set_zlim(-75,105);ax.set_box_aspect((1,1,1));ax.view_init(el,az);ax.set_axis_off();ax.set_title(t)
    ax.set_facecolor((0.32,0.34,0.38))
fig.patch.set_facecolor((0.32,0.34,0.38))
for a_ in fig.axes: a_.title.set_color("white")
plt.subplots_adjust(0,0,1,0.93,0,0); plt.savefig("apercu_ruban.png", facecolor=fig.get_facecolor())
