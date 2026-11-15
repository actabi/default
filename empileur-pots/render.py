import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
tm = trimesh.load("empileur_pots.stl")
fig = plt.figure(figsize=(12,5), dpi=160)
L = np.array([0.3,-0.5,0.8]); L/=np.linalg.norm(L)
ax = fig.add_subplot(1,2,1, projection="3d"); el,az=35,-60
cam=np.array([np.cos(np.radians(el))*np.cos(np.radians(az)),np.cos(np.radians(el))*np.sin(np.radians(az)),np.sin(np.radians(el))])
keep=tm.face_normals@cam>0
sh=np.clip(tm.face_normals@L,0,1)*0.75+0.25
col=np.c_[np.outer(sh,[0.25,0.75,0.35]),np.ones(len(sh))][keep]
ax.add_collection3d(Poly3DCollection(tm.triangles[keep],facecolors=col,edgecolors=col,linewidths=0.1))
ax.set_xlim(-36,36);ax.set_ylim(-36,36);ax.set_zlim(-29,43);ax.set_box_aspect((1,1,1));ax.view_init(el,az);ax.set_axis_off()
ax2 = fig.add_subplot(1,2,2)
sec = tm.section(plane_origin=[0,0,0], plane_normal=[0,1,0])
for e in sec.discrete: ax2.fill(e[:,0], e[:,2], color=(0.25,0.75,0.35))
ax2.set_aspect("equal"); ax2.set_title("Coupe (mm) — bas : côté fond du pot / haut : côté col"); ax2.grid(alpha=.3)
plt.tight_layout(); plt.savefig("apercu.png")
