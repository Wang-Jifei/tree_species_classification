# -*- coding: utf-8 -*-

# Import Python packages
import laspy
import numpy as np
import datetime as dt
from PIL import Image
###############################################################################
## Read point cloud file
# set input file path
strPath = r"D:\NanNan\NUS\Semester2\GE5219 Spatial Programming\GroupProject\Data\LasData\off-ground points.las"
inFile = laspy.file.File(strPath)    # open point cloud file to inFile
# set output file path
outputPath = r"D:\NanNan\NUS\Semester2\GE5219 Spatial Programming\GroupProject\Data\KNNData"

# View the point format of the point cloud: Point Format 2
print('Point Of Data Format: ', inFile.header.data_format_id) 

# View the number of points
print('Number of point records: ', inFile.header.records_count)

# View the record length of point cloud
print('data_record_length: ', inFile.header.data_record_length)

# View point cloud field name:
# X, Y, Z, intensity, flag_byte, raw_classification, scan_angle_rank, user_data,
# pt_src_id, red, green, blue, C2M_signed_distances
print("Examining Point Format:")
for spec in inFile.point_format:    # loop to print the field name of point cloud file
    print(spec.name)
    
# View the maximum of XYZ：[364233.2715187073, 151727.42303085327, 80.09705112457276]
print('Max (X, Y, Z):\n', inFile.header.max)
max_X = inFile.header.max[0]    # put maximum of X in max_X
max_Y = inFile.header.max[1]    # put maximum of Y in max_Y
max_Z = inFile.header.max[2]    # put maximum of Z in max_Z

# View the minimum of XYZ：[364146.38441848755, 151604.0986289978, 52.82545135498047]
print('Min (X, Y, Z):\n', inFile.header.min)
min_X = inFile.header.min[0]    # put minimum of X in min_X
min_Y = inFile.header.min[1]    # put minimum of Y in min_Y
min_Z = inFile.header.min[2]    # put minimum of Z in min_Z

# Place the point cloud data in the array XYZ
X = inFile.X * inFile.header.scale[0] + inFile.header.offset[0]    # calculate X
Y = inFile.Y * inFile.header.scale[1] + inFile.header.offset[1]    # calculate Y
Z = inFile.Z * inFile.header.scale[2] + inFile.header.offset[2]    # calculate Z
red = inFile.red    # put red message in red
green = inFile.green    # put green message in green
blue = inFile.blue    # put blue message in blue
XYZ = np.zeros((len(X),6))    # initialize a new array XYZ for the point data
for i in range(0,len(X)):    # loop
    XYZ[i][0] = X[i]    # put X in array XYZ
    XYZ[i][1] = Y[i]    # put Y in array XYZ
    XYZ[i][2] = Z[i]    # put Z in array XYZ
    XYZ[i][3] = red[i]    # put red in array XYZ
    XYZ[i][4] = green[i]    # put green in array XYZ
    XYZ[i][5] = blue[i]    # put blue in array XYZ
    
###############################################################################
## Reduce 3D point cloud data to 2D raster (Expected to run 1h25mins)
xyz_row_temp = XYZ[np.argsort(XYZ[:,1]),:]    # XYZ is sorted by y from smallest to largest
xyz_column_temp = XYZ[np.argsort(XYZ[:,0]),:]    # XYZ is sorted by x from smallest to largest
# Build a Raster with 1.5cm resolution
cell_size = 0.015    # set the cell size to be 1.5cm
dx = xyz_column_temp[len(xyz_column_temp) - 1,0] - xyz_column_temp[0,0]    # calculate the difference of x
dy = xyz_row_temp[len(xyz_row_temp) - 1,1] - xyz_row_temp[0,1]    # calculate the difference of y
row = int(dy / cell_size) + 1    # calculate the number of row
column = int(dx / cell_size) + 1    # calculate the number of column
Raster = np.zeros(((row,column,6)))    # initialize a Raster with 1.5cm resolution
# Loop the raster (Expected to run 35mins)
win_num = 1    # define the window of filter (win_num = 1 means to take the average of points in one cell directly)
start_y = xyz_row_temp[0,1]    # set the beginning of y
start_x = xyz_column_temp[0,0]    # set the beginning of x
cell_y = start_y    # set y of the loop cell 
start_time = dt.datetime.now().strftime('%F %T')    # record the start running time
for i in range(0,row):    # loop
    win_left_y = cell_y - cell_size * (win_num - 1) / 2    # calcualte the left y of window
    win_right_y = win_left_y + cell_size * win_num    # calculate the right y of window
    # find the points from win_left_y to win_right_y
    xyz_column_temp = filter(lambda x: x[1] >= win_left_y and x[1] < win_right_y , xyz_row_temp)
    xyz_column_temp = np.array(list(xyz_column_temp))    # convert the selected points to array
    if len(xyz_column_temp) != 0:    # make sure xyz_column_temp is not empty
        xyz_column_temp = xyz_column_temp[np.argsort(xyz_column_temp[:,0]),:]    # sorted by x from smallest to largest
        cell_x = start_x    # set x of the loop cell
        for j in range(0,column):    # loop
            cell_points = []    # initialize cell_points
            win_left_x = cell_x - cell_size * (win_num - 1) / 2    # calcualte the left x of window
            win_right_x = win_left_x + cell_size * win_num    # calculate the right x of window
            # find the points from win_left_x to win_right_x
            cell_points = filter(lambda x: x[0] >= win_left_x and x[0] < win_right_x, xyz_column_temp)
            cell_points = np.array(list(cell_points))    # convert the selected points to array
            if len(cell_points) != 0:    # make sure cell_points is not empty
                Raster[i][j][0] = np.mean(cell_points[:,0])    # put the mean of x in Raster
                Raster[i][j][1] = np.mean(cell_points[:,1])    # put the mean of y in Raster
                Raster[i][j][2] = np.mean(cell_points[:,2])    # put the mean of z in Raster
                Raster[i][j][3] = np.mean(cell_points[:,3])    # put the mean of red in Raster
                Raster[i][j][4] = np.mean(cell_points[:,4])    # put the mean of green in Raster
                Raster[i][j][5] = np.mean(cell_points[:,5])    # put the mean of blue in Raster
            cell_x = cell_x + cell_size    # update cell_x
    print("Processing: {:.2f}%. Finished {} rows. Rows in total: {}.".format(i / row * 100, i, row))    # to observe the progress of the operation
    cell_y = cell_y + cell_size    # update cell_y
end_time = dt.datetime.now().strftime('%F %T')    # record the ending running time
print('Start time: ' + start_time)    # print start time
print('End time: ' + end_time)    # print end time

# Since the previous loop ends and the image is inverted, we flip the image back to normal
Raster2 = Raster    # Copy a new raster for temp
Raster = np.zeros(((row,column,6)))    # initialize the previous raster
for i in range(0,row):    # loop
    Raster[row-1-i] = Raster2[i]    # flip the image
print("Raster.shape = " + str(Raster.shape))    # view the shape of raster result

# Save the image
im = Image.fromarray(np.uint8(Raster[:,:,:3]))    # convert XYZ to image
im.save(outputPath + "\XYZ.tiff")    # save XYZ as tiff
im = Image.fromarray(np.uint8(Raster[:,:,-3:]))    # convert RGB to image
im.save(outputPath + "\RGB.tiff")    # save RGB as tiff

# Save txt
np.savetxt(outputPath + "\\X.txt", Raster[:,:,0])    # save X as txt
np.savetxt(outputPath + "\\Y.txt", Raster[:,:,1])    # save Y as txt
np.savetxt(outputPath + "\\Z.txt", Raster[:,:,2])    # save Z as txt
np.savetxt(outputPath + "\\Red.txt", Raster[:,:,3])    # save Red as txt
np.savetxt(outputPath + "\\Green.txt", Raster[:,:,4])    # save Green as txt
np.savetxt(outputPath + "\\Blue.txt", Raster[:,:,5])    # save Blue as txt

###############################################################################
## Interpolate point cloud data (cost much time)
'''
# Skip the previous steps and load txt data directly (Expect to load for 10mins)
Raster = np.zeros(((row,column,6)))    # initialize Raster array
Raster[:,:,0] = np.loadtxt(outputPath + "\X.txt")    # load x
Raster[:,:,1] = np.loadtxt(outputPath + "\Y.txt")    # load y
Raster[:,:,2] = np.loadtxt(outputPath + "\Z.txt")    # load z
Raster[:,:,3] = np.loadtxt(outputPath + "\Red.txt")    # load red
Raster[:,:,4] = np.loadtxt(outputPath + "\Green.txt")    # load green
Raster[:,:,5] = np.loadtxt(outputPath + "\Blue.txt")    # load blue
'''
# Window pane interpolation of missing data 
# (It is expected to loop once for 1h in the early period and 30mins in the latter period)
# (First: 1h, Second: 1.5h, Third: 1h, Fourth: 58mins, Fifth: 53mins)
# (T6-T15: 6h20m, T16: 30mins, T16-T25: 5h20m, T26-D35: 5h32min; T36-55: 8h26m;)
# (T56-65: 4h49m, T66-75: 4h9m, T64-85: 7h21m, T85-87：25min, Times 87 Finished)
win_num = 11     # set 11*11 window for loop, which is nearly 16.5cm side length
edge = int((win_num - 1) / 2)    # edge define the beginning of the loop
knn = 5    # set the least number of neighbours
times = 87    # loop 87 times to fill
old_Raster = Raster    # copy the raster array
start_time = dt.datetime.now().strftime('%F %T')    # record the start running time
for t in range(0,times):    # loop
    KNN_Raster = []    # create a new raster to put the imputation result
    KNN_Raster = np.zeros(((row, column, 6)))    # initialize the result array
    for i in range(edge, row - edge):    # loop
        for j in range(edge, column - edge):    # loop
            if old_Raster[i,j,0] == 0:    # if the cell do not have data
                win_array = []    # create a list to put the neighbours data
                for k in range(i - edge, i + edge):    # loop within window
                    for w in range(j - edge, j + edge):    # loop within window
                        if old_Raster[k,w,0] != 0:    # if the cell in window has data
                            win_array.append(old_Raster[k,w])    # append the cell to win_array
                if len(win_array) >= knn:    # make sure win_array is not empty
                    win_array = np.array(win_array)    # convert list to array
                    KNN_Raster[i,j,0] = np.mean(win_array[:,0])    # put the mean of x in result array
                    KNN_Raster[i,j,1] = np.mean(win_array[:,1])    # put the mean of y in result array
                    KNN_Raster[i,j,2] = np.mean(win_array[:,2])    # put the mean of z in result array
                    KNN_Raster[i,j,3] = np.mean(win_array[:,3])    # put the mean of red in result array
                    KNN_Raster[i,j,4] = np.mean(win_array[:,4])    # put the mean of green in result array
                    KNN_Raster[i,j,5] = np.mean(win_array[:,5])    # put the mean of blue in result array
            else:    # if the cell has data
                KNN_Raster[i,j,0] = old_Raster[i,j,0]    # put x in the result array directly
                KNN_Raster[i,j,1] = old_Raster[i,j,1]    # put y in the result array directly
                KNN_Raster[i,j,2] = old_Raster[i,j,2]    # put z in the result array directly
                KNN_Raster[i,j,3] = old_Raster[i,j,3]    # put red in the result array directly
                KNN_Raster[i,j,4] = old_Raster[i,j,4]    # put green in the result array directly
                KNN_Raster[i,j,5] = old_Raster[i,j,5]    # put blue in the result array directly
        print("Times {}/{} processing: {:.2f}%. Finished {}/{} rows.".format(t + 1, times, i / (row - edge) * 100, i, row - edge))    # to observe the progress of the operation
    old_Raster=[]    # create a new old Raster
    old_Raster = KNN_Raster    # copy the reslut interpolation raster
    ## The following is to save the result of each interpolation
    #im = Image.fromarray(np.uint8(KNN_Raster[:,:,:3]))    # convert XYZ to image
    #im.save(outputPath + "\KNN_XYZ" + str(t + 1) +".tiff")    # save XYZ as tiff
    #im = Image.fromarray(np.uint8(KNN_Raster[:,:,-3:]))    # convert RGB to image
    #im.save(outputPath + "\KNN_RGB" + str(t + 1) +".tiff")    # save RGB to tiff
end_time = dt.datetime.now().strftime('%F %T')    # record the ending running time
print('Start time: ' + start_time)    # print start time
print('End time: ' + end_time)    # print end time
# save the result of the final interpolation
im = Image.fromarray(np.uint8(KNN_Raster[:,:,:3]))    # convert interpolation result XYZ to image
im.save(outputPath + "\KNN_XYZ" + str(t + 1) +".tiff")    # save XYZ as tiff
im = Image.fromarray(np.uint8(KNN_Raster[:,:,-3:]))    # convert interpolation result RGB to image
im.save(outputPath + "\KNN_RGB" + str(t + 1) +".tiff")    # save RGB as tiff
np.savetxt(outputPath + "\\X87.txt", KNN_Raster[:,:,0])    # save X as txt
np.savetxt(outputPath + "\\Y87.txt", KNN_Raster[:,:,1])    # save Y as txt
np.savetxt(outputPath + "\\Z87.txt", KNN_Raster[:,:,2])    # save Z as txt
np.savetxt(outputPath + "\\Red87.txt", KNN_Raster[:,:,3])    # save red as txt
np.savetxt(outputPath + "\\Green87.txt", KNN_Raster[:,:,4])    # save green as txt
np.savetxt(outputPath + "\\Blue87.txt", KNN_Raster[:,:,5])    # save blue as txt

###############################################################################
## Calculate height's metrics
'''
# Skip the above interpolation process directly, load the result of the interpolation
# (Expect to load for 10mins)
KNN_Raster = []    # create a raster
KNN_Raster = np.zeros(((row,column,6)))    # initialize the raster
KNN_Raster[:,:,0] = np.loadtxt(outputPath + "\X87.txt")    # load x interpolation
KNN_Raster[:,:,1] = np.loadtxt(outputPath + "\Y87.txt")    # load y interpolation
KNN_Raster[:,:,2] = np.loadtxt(outputPath + "\Z87.txt")    # load z interpolation
KNN_Raster[:,:,3] = np.loadtxt(outputPath + "\Red87.txt")    # load red interpolation
KNN_Raster[:,:,4] = np.loadtxt(outputPath + "\Green87.txt")    # load green interpolation
KNN_Raster[:,:,5] = np.loadtxt(outputPath + "\Blue87.txt")    # load blue interpolation
'''
# Import entropy form python package scipy.stats
from scipy.stats import entropy
# Extract z-axis data
Height = []    # create a new variable to put height data
Height = np.zeros((row, column))    # initialize the Height array
Height = KNN_Raster[:,:,2]    # put Z data in Height
win_num = 33    # set 33*33 window for loop, which is nearly 49.5cm side length (expect to run for 10h)
edge = int((win_num - 1) / 2)    # edge define the beginning of the loop
Metrics = []    # create a new variable to put metrics of height
Metrics = np.zeros(((row, column,6)))    # initialize Metrics array
start_time = dt.datetime.now().strftime('%F %T')    # record start time
for i in range(edge, row - edge):    # loop
    for j in range(edge, column - edge):    # loop
        if Height[i,j] != 0:    # if the cell of Height has data
            win_array = []    # creat a list to put height data within window
            for k in range(i - edge, i + edge):    # loop
                for w in range(j - edge, j + edge):    # loop
                    if Height[k,w] != 0:    # if the cell has height data
                        win_array.append(Height[k,w])    # append the data to win_array
            win_array = np.array(win_array)    # convert list to array
            Metrics[i,j,0] = np.max(win_array)   # calculate the maximum
            Metrics[i,j,1] = np.mean(win_array)    # calculate the average
            Metrics[i,j,2] = np.percentile(win_array, 90)    # calculate 90 percentile
            Metrics[i,j,3] = np.percentile(win_array, 70)    # calculate 70 percentile
            Metrics[i,j,4] = np.percentile(win_array, 5)    # calculate 5 percentile
            Metrics[i,j,5] = entropy(win_array.flatten())    # calculate the entropy
    print("Processing: {:.2f}%. Finished {}/{} rows.".format(i / (row - edge) * 100, i, row - edge))    # to observe the progress of the operation
end_time = dt.datetime.now().strftime('%F %T')    # record ending time
print('Start time: ' + start_time)    # print start time
print('End time: ' + end_time)    # print end time
# Save six metrics of height
im = Image.fromarray(np.uint8(Metrics[:,:,:3]))    # convert the first three metrics array to image
im.save(outputPath + "\Metrics" + str(win_num) +"_1.tiff")    # save the first three metrics to tiff
im = Image.fromarray(np.uint8(Metrics[:,:,-3:]))    # convert the last three metrics array to image
im.save(outputPath + "\Metrics" + str(win_num) +"_2.tiff")    # save the last three metrics to tiff
im = Image.fromarray(np.uint8(Metrics[:,:,0]))    # convert the max metrics to image
im.save(outputPath + "\Metrics" + str(win_num) +"_max.tiff")    # save max as tiff
im = Image.fromarray(np.uint8(Metrics[:,:,1]))    # convert the average to image
im.save(outputPath + "\Metrics" + str(win_num) +"_mean.tiff")    # save average to tiff
im = Image.fromarray(np.uint8(Metrics[:,:,2]))    # convert 90 percentile to image
im.save(outputPath + "\Metrics" + str(win_num) +"_per90.tiff")    # save 90 percentile to tiff
im = Image.fromarray(np.uint8(Metrics[:,:,3]))    # convert 70 percentile to image
im.save(outputPath + "\Metrics" + str(win_num) +"_per70.tiff")    # save 70 percentile to tiff
im = Image.fromarray(np.uint8(Metrics[:,:,4]))    # convert 5 percentile to image
im.save(outputPath + "\Metrics" + str(win_num) +"_per5.tiff")    # save 5 percentile to tiff
im = Image.fromarray(np.uint8(Metrics[:,:,5]))    # convert the entropy metrics to image
im.save(outputPath + "\Metrics" + str(win_num) +"_etp.tiff")    # save the entropy to tiff
# Save six metrics of height to txt
#np.savetxt(outputPath + "\Metrics" + str(win_num) +"_max.txt", Metrics[:,:,0])    # save max to txt
#np.savetxt(outputPath + "\Metrics" + str(win_num) +"_mean.txt", Metrics[:,:,1])    # save average to txt
#np.savetxt(outputPath + "\Metrics" + str(win_num) +"_per90.txt", Metrics[:,:,2])    # save 90 percentile to txt
#np.savetxt(outputPath + "\Metrics" + str(win_num) +"_per70.txt", Metrics[:,:,3])    # save 70 percentile to txt
#np.savetxt(outputPath + "\Metrics" + str(win_num) +"_per5.txt", Metrics[:,:,4])    # save 5 percentile to txt
#np.savetxt(outputPath + "\Metrics" + str(win_num) +"_etp.txt", Metrics[:,:,5])    # save entropy to txt
