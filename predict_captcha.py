import pickle
import numpy as np
from numba import jit
from PIL import Image
from sklearn.cluster import AgglomerativeClustering
# from itertools import product

with open('img_dict.pkl', 'rb') as f:
    IMG_DICT = pickle.load(f)
    
MIN = min(list(map(lambda i: np.array(i).sum(), list(IMG_DICT.values()))))

def gaussian_weight(h, w, sigma=0.8):
    x, y = np.meshgrid(np.linspace(-1, 1, w), np.linspace(-1, 1, h))
    d = np.sqrt(x*x+y*y)
    mu = 0.0
    g = np.exp(-((d-mu)**2 / (2.0 * sigma**2)))
    return g


def transform(img):
    array2D = np.array(img)
    array2D[array2D > 0] = 255
    return Image.fromarray((255 - array2D))


#def scan(img, img_c):
#    mx1 = 255 - np.array(transform(img), dtype=float)
#    mx2 = 255 - np.array(img_c, dtype=float)
#    h1, w1 = mx1.shape
#    h2, w2 = mx2.shape
#    wt = gaussian_weight(h2, w2)   
#    
#    d_min = np.inf
#    d_w = 0
#    for h in range(h1 - h2):
#        for w in range(w1 - w2):
#            abs_d = np.abs(mx1[h:h+h2, w:w+w2] - mx2)
#            d = (abs_d*wt).mean()
#            if d < d_min:
#                d_min = d
#                d_w = w
#    return d_min, d_w


def mx(img, img_c):
    mx1 = 255 - np.array(transform(img), dtype=float)
    mx2 = 255 - np.array(img_c, dtype=float)
    h2, w2 = mx2.shape
    wt = gaussian_weight(h2, w2)
    return mx1, mx2, wt


@jit(nopython=True)
def scan_jit(mx1, mx2, wt):
    h1, w1 = mx1.shape
    h2, w2 = mx2.shape 
    d_min = np.inf
    d_w = 0
    for h in range(h1 - h2):
        for w in range(w1 - w2):
            mx1_sub = mx1[h:h+h2, w:w+w2]
            if mx1_sub.sum() < 2 / 3 * MIN: 
                continue
            abs_d = np.abs(mx1_sub - mx2)
            d = (abs_d*wt).mean()
            if d < d_min:
                d_min = d
                d_w = w
    return d_min, d_w


def scan(img, img_c):
    mx1, mx2, wt = mx(img, img_c)
    d_min, d_w = scan_jit(mx1, mx2, wt)
    return d_min, d_w


# def predict(img):
#     img1 = img.rotate(20, expand=True)
#     img2 = img.rotate(-20, expand=True)
#     keys = np.array(list(IMG_DICT.keys()))
#     a1 = np.array([scan(img1, IMG_DICT[key]) for key in keys])
#     a2 = np.array([scan(img2, IMG_DICT[key]) for key in keys])
#     r1 = np.argsort(a1[:, 0])
#     r2 = np.argsort(a2[:, 0])
#     d = np.concatenate([a1[:, 0][r1][:4], a2[:, 0][r2][:4]])
#     k = np.concatenate([keys[r1][:4], keys[r2][:4]])
#     p = np.concatenate([a1[:, 1][r1][:4], a2[:, 1][r2][:4]])
#     prd = k[np.argsort(d)][:4][np.argsort(p[np.argsort(d)][:4])]
#     return ''.join(prd)

def predict(img):
    img1 = img.rotate(20, expand=True)
    img2 = img.rotate(-20, expand=True)
    keys = np.array(list(IMG_DICT.keys()))
    a1 = np.array([scan(img1, IMG_DICT[key]) for key in keys])
    a2 = np.array([scan(img2, IMG_DICT[key]) for key in keys])
    r1 = np.argsort(a1[:, 0])
    r2 = np.argsort(a2[:, 0])
    d = np.concatenate([a1[:, 0][r1], a2[:, 0][r2]])
    k = np.concatenate([keys[r1], keys[r2]])
    p = np.concatenate([a1[:, 1][r1], a2[:, 1][r2]])
    r = np.argsort(p)
    d, k, p = d[r], k[r], p[r]
    prd = []
    hc = AgglomerativeClustering(n_clusters=4).fit(p.reshape(-1, 1))
    _, pos = np.unique(hc.labels_, return_index=True)
    cluster_label = hc.labels_[np.sort(pos)]
    for label in cluster_label:
        d_cluster = d[hc.labels_==label]
        k_cluster = k[hc.labels_==label]
        prd.append(k_cluster[np.argsort(d_cluster)][0])
    return ''.join(prd)

