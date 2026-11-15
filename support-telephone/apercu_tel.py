"""Aperçu du support avec un Galaxy S26+ en coque posé dessus (image seulement)."""
import trimesh, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import support as S
TEL = (161.0, 78.5, 11.6)                      # hauteur, largeur, épaisseur avec coque
up = [[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]] # profil (x,y)+largeur z -> debout
st = trimesh.load("support_telephone.stl"); st = trimesh.Trimesh(*trimesh.remesh.subdivide_to_size(st.vertices, st.faces, 6)); st.apply_transform(up); st.invert()
o = S.P0 + S.r*S.v + S.r*S.u                   # coin bas-arrière du téléphone
box = trimesh.creation.box(extents=(TEL[2], TEL[0], TEL[1]))
box = trimesh.Trimesh(*trimesh.remesh.subdivide_to_size(box.vertices, box.faces, 6))
box.apply_translation((TEL[2]/2, TEL[0]/2, S.LARGEUR/2))
M = np.eye(4); M[:2,0] = S.v; M[:2,1] = S.u; M[:2,3] = o
box.apply_transform(M); box.apply_transform(up); box.invert()
ecran = box.face_normals @ np.array([S.v[0], 0, S.v[1]]) > 0.99
fig = plt.figure(figsize=(12,6.5), dpi=160)
L = np.array([-0.4,-0.5,0.75]); L/=np.linalg.norm(L)
for k,(el,az) in enumerate([(18,-128),(0,-90)]):
    ax = fig.add_subplot(1,2,k+1, projection="3d")
    cam=np.array([np.cos(np.radians(el))*np.cos(np.radians(az)),np.cos(np.radians(el))*np.sin(np.radians(az)),np.sin(np.radians(el))])
    tris, cols = [], []
    for m, base in ((st,(0.25,0.75,0.35)), (box,(0.30,0.32,0.36))):
        keep = m.face_normals@cam > 0
        sh = np.clip(m.face_normals@L,0,1)*0.7+0.3
        c = np.outer(sh, base)
        if m is box: c[ecran] = (0.08,0.09,0.12)
        tris.append(m.triangles[keep]); cols.append(c[keep])
    tris=np.vstack(tris); cols=np.c_[np.vstack(cols),np.ones(len(tris))]
    ax.add_collection3d(Poly3DCollection(tris,facecolors=cols,edgecolors=cols,linewidths=0.1))
    ax.set_xlim(-30,150);ax.set_ylim(-55,125);ax.set_zlim(0,180);ax.set_box_aspect((1,1,1));ax.view_init(el,az);ax.set_axis_off()
plt.subplots_adjust(0,0,1,1,0,0); plt.savefig("apercu_avec_telephone.png")
