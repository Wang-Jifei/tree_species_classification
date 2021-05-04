KNN_Georeference：存放的是原始的点云经过插补之后的结果
	其中XYZ.tif和RGB.tif是没插补之前的栅格数据，分别3个波段，存放了点云降维后的XYZ信息和RGB信息；
	KNN_XYZ.tif和KNN_RGB.tif是经过第一次插补之后的栅格数据，同样各有3各波段，分别存放XYZ和RGB的信息；
	KNN_XYZ87.tif和KNN_RGB87.tif是经过87次插补之后范围内缺失值全部填满的数据，格式同上。

Z_Metrics：存放的是高程Z轴的6个特征，经过插补后的数据计算得到，计算的滤波窗口为33，窗口边长大致约0.5m
	max
	mean
	per90: percentile90
	per70: percentile70
	per5: percentile5
	etp: entropy