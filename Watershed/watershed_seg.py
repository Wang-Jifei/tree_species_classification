import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('./data/r.tif')
#im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
im = img
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage.segmentation import watershed
from skimage.feature import peak_local_max
import time
# Generate an initial image with two overlapping circles
# image_max is the dilation of im with a 20*20 structuring element
# It is used within peak_local_max function
image_max = ndi.maximum_filter(im, size=100, mode='constant')

# Comparison between image_max and im to find the coordinates of local maxima
coordinates = peak_local_max(im, min_distance=300)

# display results
fig, axes = plt.subplots(1, 3, figsize=(8, 3), sharex=True, sharey=True)
ax = axes.ravel()
ax[0].imshow(im, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('Original')

ax[1].imshow(image_max, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('Maximum filter')

ax[2].imshow(im, cmap=plt.cm.gray)
ax[2].autoscale(False)
ax[2].plot(coordinates[:, 1], coordinates[:, 0], 'r.')
ax[2].axis('off')
ax[2].set_title('Peak local max')

fig.tight_layout()

plt.show()
import numpy as np
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from skimage import measure
from skimage.segmentation import random_walker
import matplotlib.pyplot as plt
from scipy import ndimage
import skimage
from PIL import Image
# Generate the markers as local maxima of the distance
# to the background
distance = ndimage.distance_transform_edt(im)
start_treetop=time.time()
local_maxi = peak_local_max(im, min_distance=400, indices=True, footprint=np.ones((3, 3)), labels=im)
coords = peak_local_max(im, min_distance=300)
end_treetop=time.time()
print("treetop time",end_treetop-start_treetop)

print("Calculate local maxima")
mask = np.zeros(im.shape, dtype=bool)
mask[tuple(coords.T)] = True
markers, _ = ndi.label(mask)
print("Calsulate local markers")
labels = watershed(-im, markers, mask=im, connectivity=4)

print("Watershed segmentation...")
im_label = Image.fromarray(labels)
im_label.save("label.tif")
fig, axes = plt.subplots(ncols=3, figsize=(9, 3), sharex=True, sharey=True)
ax = axes.ravel()

ax[0].imshow(im, cmap=plt.cm.gray)
ax[0].set_title('Overlapping objects')
ax[1].imshow(-distance, cmap=plt.cm.gray)
ax[1].set_title('Distances')
ax[2].imshow(labels, cmap=plt.cm.nipy_spectral)
ax[2].set_title('Separated objects')
from scipy.ndimage import binary_dilation
for a in ax:
    a.set_axis_off()

fig.tight_layout()
plt.show()

canny = skimage.feature. canny(labels. astype(float))
fig, ax = plt.subplots(figsize=(20,40))
ax.axis('off')
ax.imshow(labels, cmap='Greens')
ax.imshow(binary_dilation(canny, iterations=10,structure=np. ones ((5,5))),cmap ='gray',alpha =0.5)
fig.show()
fig.savefig("out.png")
