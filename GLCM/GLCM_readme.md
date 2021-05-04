Before import library, you need to install cv2. In Jupyter, input '!pip install opencv-python'.
1. 
cv2.imread(filename), convert image into grey matrix
The function imread loads an image from the specified file and returns it. If the image cannot be
read (because of missing file, improper permissions, unsupported or invalid format), the function
returns an empty matrix ( Mat::data==NULL ).
   
Currently, the following file formats are supported:
-   Windows bitmaps - \*.bmp, \*.dib (always supported)
-   JPEG files - \*.jpeg, \*.jpg, \*.jpe (see the *Note* section)
-   JPEG 2000 files - \*.jp2 (see the *Note* section)
-   Portable Network Graphics - \*.png (see the *Note* section)
-   WebP - \*.webp (see the *Note* section)
-   Portable image format - \*.pbm, \*.pgm, \*.ppm \*.pxm, \*.pnm (always supported)
-   PFM files - \*.pfm (see the *Note* section)
-   Sun rasters - \*.sr, \*.ras (always supported)
-   TIFF files - \*.tiff, \*.tif (see the *Note* section)
-   OpenEXR Image files - \*.exr (see the *Note* section)
-   Radiance HDR - \*.hdr, \*.pic (always supported)
-   Raster and Vector geospatial data supported by GDAL (see the *Note* section)

2.
greycomatrix(image, distances, angles, levels=None, symmetric=False, normed=False,)
Calculate the grey-level co-occurrence matrix.

A grey level co-occurrence matrix is a histogram of co-occurring
greyscale values at a given offset over an image.

Parameters
----------
image : array_like
    Integer typed input image. Only positive valued images are supported.
    If type is other than uint8, the argument `levels` needs to be set.
distances : array_like
    List of pixel pair distance offsets.
angles : array_like
    List of pixel pair angles in radians.
levels : int, optional
    The input image should contain integers in [0, `levels`-1],
    where levels indicate the number of grey-levels counted
    (typically 256 for an 8-bit image). This argument is required for
    16-bit images or higher and is typically the maximum of the image.
    As the output matrix is at least `levels` x `levels`, it might
    be preferable to use binning of the input image rather than
    large values for `levels`.
symmetric : bool, optional
    If True, the output matrix `P[:, :, d, theta]` is symmetric. This
    is accomplished by ignoring the order of value pairs, so both
    (i, j) and (j, i) are accumulated when (i, j) is encountered
    for a given offset. The default is False.
normed : bool, optional
    If True, normalize each matrix `P[:, :, d, theta]` by dividing
    by the total number of accumulated co-occurrences for the given
    offset. The elements of the resulting matrix sum to 1. The
    default is False.

3.
Use the following functions to get feature matrix, parameter is a grey-level co-occurrence matrix. 
contrast_feature(matrix_coocurrence),  
dissimilarity_feature(matrix_coocurrence), 
homogeneity_feature(matrix_coocurrence), 
energy_feature(matrix_coocurrence), 
correlation_feature(matrix_coocurrence), 
secondmoment_feature(matrix_coocurrence),
mean_feature(matrix_coocurrence),
variance_feature(matrix_coocurrence),
entropy_feature(matrix_coocurrence),