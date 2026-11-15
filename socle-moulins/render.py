import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
tm = trimesh.load("socle_moulins.stl")
fig = plt.figure(figsize=(12,6), dpi=160)
L = np.array([0.3,-0.5,0.8]); L/=np.linalg.norm(L)
for k,(el,az) in enumerate([(38,-62),(89,-90)]):
    ax = fig.add_subplot(1,2,k+1, projection="3d")
    cam=np.array([np.cos(np.radians(el))*np.cos(np.radians(az)),np.cos(np.radians(el))*np.sin(np.radians(az)),np.sin(np.radians(el))])
    keep=tm.face_normals@cam>0
    sh = np.clip(tm.face_normals@L,0,1)*0.75+0.25
    col = np.outer(sh,[0.25,0.75,0.35]); col=np.c_[col,np.ones(len(col))][keep]
    ax.add_collection3d(Poly3DCollection(tm.triangles[keep], facecolors=col, edgecolors=col, linewidths=0.1))
    e = tm.bounds; ax.set_xlim(e[0,0],e[1,0]); ax.set_ylim(-65,65); ax.set_zlim(-40,60)
    ax.set_box_aspect((e[1,0]-e[0,0],130,100)); ax.view_init(el,az); ax.set_axis_off()
plt.subplots_adjust(0,0,1,1,0,0); plt.savefig("apercu.png")
