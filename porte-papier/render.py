import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import porte_papier as P
tm = trimesh.load("porte_papier.stl")
sub = trimesh.Trimesh(*trimesh.remesh.subdivide_to_size(tm.vertices, tm.faces, 5))
# rouleau fantôme : mandrin posé sur le dessus du bras
rc, R, L = 20.0, 55.0, P.L_ROULEAU
roll = trimesh.creation.annulus(rc, R, L, sections=64)
roll.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0,1,0]))
roll.apply_translation((P.T+8+L/2, P.y_axe, P.H-rc))
roll = trimesh.Trimesh(*trimesh.remesh.subdivide_to_size(roll.vertices, roll.faces, 5))
fig = plt.figure(figsize=(13,6.5), dpi=160)
for k,(el,az,t,avec) in enumerate([(24,62,"Porte-rouleau seul (sens d'impression)",False),(20,55,"Avec un rouleau",True)]):
    ax = fig.add_subplot(1,2,k+1, projection="3d")
    cam=np.array([np.cos(np.radians(el))*np.cos(np.radians(az)),np.cos(np.radians(el))*np.sin(np.radians(az)),np.sin(np.radians(el))])
    L_=np.array([0.5,0.4,0.75]); L_/=np.linalg.norm(L_)
    tris, cols = [], []
    for m, base in [(sub,(0.25,0.75,0.35))] + ([(roll,(0.93,0.93,0.90))] if avec else []):
        keep=m.face_normals@cam>0; sh=np.clip(m.face_normals@L_,0,1)*0.7+0.3
        tris.append(m.triangles[keep]); cols.append(np.outer(sh,base)[keep])
    tris=np.vstack(tris); cols=np.c_[np.vstack(cols),np.ones(len(tris))]
    ax.add_collection3d(Poly3DCollection(tris,facecolors=cols,edgecolors=cols,linewidths=0.1))
    ax.set_xlim(-10,150);ax.set_ylim(-40,120);ax.set_zlim(-75,85);ax.set_box_aspect((1,1,1));ax.view_init(el,az);ax.set_axis_off();ax.set_title(t)
plt.subplots_adjust(0,0,1,0.95,0,0); plt.savefig("apercu.png")
