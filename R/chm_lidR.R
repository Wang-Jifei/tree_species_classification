library(lidR)

# Display 3D data
las0 <- readLAS("chestnut.las")

plot(las, size = 3,bg = "white",axis = TRUE,legend=TRUE) # Plot point cloud data

hist(las0$Z, breaks = seq(45, 85, 0.2), main = "Histogram of poind cloud height distribution", xlab = "Elevation")

las1 <- readLAS("off-ground points.las")

# Histogram of point cloud height distribution
hist(las1$Z, breaks = seq(40, 90, 0.2), main = "Histogram of poind cloud height distribution", xlab = "Elevation")

las0 <- classify_ground(las0, algorithm = csf())
plot_crossection(las0, p1 = p1, p2 = p2, colour_by = factor(Classification))


# Pit-tree CHM generation
tic<- Sys.time()
chm <- grid_canopy(las, res = 0.015, pitfree(thresholds = c(0, 10, 20), max_edge = c(0, 0.5)))
toc<- Sys.time()
print(toc-tic)
col <- height.colors(50)
plot(chm, col = col)

chm_c <- grid_canopy(las, res = 0.5, pitfree(subcircle = 0.15))
plot(chm_c, col = col)

# Tin CHM generation
chm_tin <- grid_canopy(las, res = 0.015, p2r(0.1, na.fill = tin()))
plot(chm_tin, col = col)


tic<- Sys.time()
print("START...")
# Triangular CHM generation
chm_trian <- grid_canopy(las, res = 0.015, algorithm = dsmtin())
plot(chm_trian, col = col)
print("...END")
toc<- Sys.time()
print(toc-tic)
# Pit-tree CHM post processing
fill.na <- function(x, i=5) { if (is.na(x)[i]) { return(mean(x, na.rm = TRUE)) } else { return(x[i]) }}
w <- matrix(1, 3, 3)

chm <- grid_canopy(las, res = 0.015, pitfree(thresholds = c(0, 10, 20), max_edge = c(0, 0.5)))
filled <- focal(chm, w, fun = fill.na)
smoothed <- focal(chm, w, fun = mean, na.rm = TRUE)

chms <- stack(chm, filled, smoothed)
names(chms) <- c("Base", "Filled", "Smoothed")
plot(chms, col = col)


# Individual Tree Detection
ttops <- find_trees(las, lmf(ws = 5))

plot(chm, col = height.colors(50))
plot(ttops, add = TRUE)

# visualize in 3D
x <- plot(las, bg = "white", size = 4)
add_treetops3d(x, ttops)
# tree detection use different window size
tic<- Sys.time()
ttops_5m <- find_trees(las, lmf(ws = 5))
toc<- Sys.time()
print(toc-tic)
ttops_11m <- find_trees(las, lmf(ws = 11))

par(mfrow=c(1,2))
plot(chm, col = height.colors(50))
plot(ttops_5m, add = TRUE)
plot(chm, col = height.colors(50))
plot(ttops_11m, add = TRUE)

# Local Maxima
f <- function(x) {x * 0.1 + 3}

heights <- seq(0,30,5)
ws <- f(heights)
plot(heights, ws, type = "l", ylim = c(0,6))

ttops <- find_trees(las, lmf(f))

plot(chm, col = height.colors(50))
plot(ttops, add = TRUE)

f <- function(x) {
  y <- 2.6 * (-(exp(-0.08*(x-2)) - 1)) + 3
  y[x < 2] <- 3
  y[x > 20] <- 5
  return(y)
}

heights <- seq(-5,30,0.5)
ws <- f(heights)
plot(heights, ws, type = "l",  ylim = c(0,5))
ttops <- find_trees(las, lmf(f))

plot(chm, col = height.colors(50))
plot(ttops, add = TRUE)
writeRaster(chm, "chm", format = "GTiff") # save chm to disk
#####Segmentation

# Point-to-raster 2 resolutions
chm_p2r_05 <- grid_canopy(las, 0.015, p2r(subcircle = 0.2))
chm_p2r_1 <- grid_canopy(las, 0.05, p2r(subcircle = 0.2))

# Pitfree with and without subcircle tweak
chm_pitfree_05_1 <- grid_canopy(las, 0.015, pitfree())
chm_pitfree_05_2 <- grid_canopy(las, 0.015, pitfree(subcircle = 0.2))

# Post-processing median filter
kernel <- matrix(1,3,3)
chm_p2r_05_smoothed <- raster::focal(chm_p2r_05, w = kernel, fun = median, na.rm = TRUE)
chm_p2r_1_smoothed <- raster::focal(chm_p2r_1, w = kernel, fun = median, na.rm = TRUE)

# Tree detection
ttops_chm_p2r_015 <- find_trees(chm_p2r_015, lmf(5))
ttops_chm_p2r_05 <- find_trees(chm_p2r_05, lmf(5))
ttops_chm_pitfree_05_1 <- find_trees(chm_pitfree_015_1, lmf(f))
ttops_chm_pitfree_05_2 <- find_trees(chm_pitfree_015_2, lmf(f))
ttops_chm_p2r_05_smoothed <- find_trees(chm_p2r_05_smoothed, lmf(f))
ttops_chm_p2r_1_smoothed <- find_trees(chm_p2r_1_smoothed, lmf(f))
# Display ITD results
par(mfrow=c(3,2))
col <- height.colors(50)
plot(chm_p2r_05, main = "CHM P2R 0.5", col = col); plot(ttops_chm_p2r_05, add = T)
plot(chm_p2r_1, main = "CHM P2R 1", col = col); plot(ttops_chm_p2r_1, add = T)
plot(chm_p2r_05_smoothed, main = "CHM P2R 0.5 smoothed", col = col); plot(ttops_chm_p2r_05_smoothed, add = T)
plot(chm_p2r_1_smoothed, main = "CHM P2R 1 smoothed", col = col); plot(ttops_chm_p2r_1_smoothed, add = T)
plot(chm_pitfree_05_1, main = "CHM PITFREE 1", col = col); plot(ttops_chm_pitfree_05_1, add = T)
plot(chm_pitfree_05_2, main = "CHM PITFREE 2", col = col); plot(ttops_chm_pitfree_05_2, add = T)
