import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(13,5.6), dpi=160); bg=(0.32,0.34,0.38); fig.patch.set_facecolor(bg)
for k,(f,t,az) in enumerate([("porte_papier_ruban_ouvert_a_gauche.stl","Bout ouvert à gauche",60),("porte_papier_ruban_ouvert_a_droite.stl","Bout ouvert à droite",120)]):
    tm = trimesh.load(f); sub = trimesh.Trimesh(*trimesh.remesh.subdivide_to_size(tm.vertices, tm.faces, 5))
    ax = fig.add_subplot(1,2,k+1, projection="3d"); el=28
    cam=np.array([np.cos(np.radians(el))*np.cos(np.radians(az)),np.cos(np.radians(el))*np.sin(np.radians(az)),np.sin(np.radians(el))])
    L_=np.array([0.45 if k==0 else -0.45,0.45,0.77]); L_/=np.linalg.norm(L_)
    keep=sub.face_normals@cam>0; sh=np.clip(sub.face_normals@L_,0,1)*0.55+0.42
    col=np.c_[np.outer(sh,(0.93,0.93,0.94)),np.ones(len(sh))][keep]
    ax.add_collection3d(Poly3DCollection(sub.triangles[keep],facecolors=col,edgecolors=col,linewidths=0.1))
    c=tm.bounds.mean(0); ax.set_xlim(c[0]-90,c[0]+90);ax.set_ylim(-45,135);ax.set_zlim(-75,105);ax.set_box_aspect((1,1,1));ax.view_init(el,az);ax.set_axis_off()
    ax.set_title(t+" (vu face au mur)", color="white"); ax.set_facecolor(bg)
plt.subplots_adjust(0,0,1,0.93,0,0); plt.savefig("apercu_ruban_gauche_droite.png", facecolor=bg)
