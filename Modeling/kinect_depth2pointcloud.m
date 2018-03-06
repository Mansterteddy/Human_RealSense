% Convert Kinect Depth Map to 3D Point Cloud
clc; clear;
addpath('/Users/manster/Desktop/Human_RealSense/Modeling/opcodemesh/matlab/');
addpath('/Users/manster/Desktop/Human_RealSense/Modeling/MyDoc/VisualizeToolBox/');
addpath('/Users/manster/Desktop/Human_RealSense/Modeling/MyDoc/GPLVM_TOOLBOX/MOCAPTOOLBOX/AFM/');
addpath('/Users/manster/Desktop/Human_RealSense/Modeling/MyDoc/GPLVM_TOOLBOX/MOCAP0p136/');
addpath('/Users/manster/Desktop/Human_RealSense/Modeling/MyDoc/GPLVM_TOOLBOX/NDLUTIL0p162/');
addpath('/Users/manster/Desktop/Human_RealSense/Modeling/MyDoc/GPLVM_TOOLBOX/MOCAPTOOLBOX/quaternions/');

%% Define camera parameters
iH = 512
iW = 424

calib.R = Eul2Mat([0 pi pi]);
calib.t = 0;
calib.K = [367.7, 0, 258.6; 0, 365.4, 207.3; 0, 0, 1];

mask = ones(iH, iW);
kine.ratio = 1;
[from, ray] = CalProjLines(calib, mask);
camera = CameraCompr(mask, calib, from, ray);

%% Get 3d depth point cloud
fname = '/Users/manster/Desktop/Human_RealSense/Modeling/img/03200.png';
observe.dmap = double(imread(fname))/1e3;
[observe.dimg, observe.simg] = dmap2dimg(observe.dmap, kine.ratio);
[observe.p2d, observe.p3d, vmap] = dmap2pointcloud(observe.dmap, calib);
observe.nl = CalDptNrms(vmap);
observe.ratio = 1;
figure; hold on; grid on; axis equal;
PlotRelativeDepthMap(observe.p3d);
