import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
tm = trimesh.load("etui_trepied.stl")
sub = trimesh.Trimesh(*trimesh.remesh.subdivide_to_size(tm.vertices, tm.faces, 4))
fig = plt.figure(figsize=(13,6.5), dpi=160)
L = np.array([0.3,-0.6,0.7]); L/=np.linalg.norm(L)
for k,(el,az,t) in enumerate([(25,-70,"Vue avant"),(20,65,"Vue arrière : filetages dessous et côté")]):
    ax = fig.add_subplot(1,2,k+1, projection="3d")
    cam=np.array([np.cos(np.radians(el))*np.cos(np.radians(az)),np.cos(np.radians(el))*np.sin(np.radians(az)),np.sin(np.radians(el))])
    Lk = L if k==0 else np.array([0.3,0.6,0.7])/np.linalg.norm([0.3,0.6,0.7])
    keep=sub.face_normals@cam>0; sh=np.clip(sub.face_normals@Lk,0,1)*0.7+0.3
    col=np.c_[np.outer(sh,[0.25,0.75,0.35]),np.ones(len(sh))][keep]
    ax.add_collection3d(Poly3DCollection(sub.triangles[keep],facecolors=col,edgecolors=col,linewidths=0.1))
    ax.set_xlim(-8,92);ax.set_ylim(-40,60);ax.set_zlim(-8,92);ax.set_box_aspect((1,1,1));ax.view_init(el,az);ax.set_axis_off();ax.set_title(t)
plt.subplots_adjust(0,0,1,0.95,0,0); plt.savefig("apercu_etui.png")
