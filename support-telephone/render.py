import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
tm = trimesh.load("support_telephone.stl")
tm.apply_transform([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]); tm.invert()   # remettre debout
fig = plt.figure(figsize=(12,6), dpi=160)
L = np.array([-0.4,-0.5,0.75]); L/=np.linalg.norm(L)
for k,(el,az) in enumerate([(22,-125),(0,-90)]):
    ax = fig.add_subplot(1,2,k+1, projection="3d")
    cam=np.array([np.cos(np.radians(el))*np.cos(np.radians(az)),np.cos(np.radians(el))*np.sin(np.radians(az)),np.sin(np.radians(el))])
    keep=tm.face_normals@cam>0
    sh=np.clip(tm.face_normals@L,0,1)*0.7+0.3
    col=np.c_[np.outer(sh,[0.25,0.75,0.35]),np.ones(len(sh))][keep]
    ax.add_collection3d(Poly3DCollection(tm.triangles[keep],facecolors=col,edgecolors=col,linewidths=0.1))
    ax.set_xlim(-10,110);ax.set_ylim(-25,95);ax.set_zlim(0,120);ax.set_box_aspect((1,1,1));ax.view_init(el,az);ax.set_axis_off()
plt.subplots_adjust(0,0,1,1,0,0); plt.savefig("apercu.png")
