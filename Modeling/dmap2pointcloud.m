function [p2d, p3d, vmap] = dmap2pointcloud(dmap, calib, ratio)

    % dmap is H*W array that contained depth value
    % calib is a struct specify the camera matrix:
    %       calib.K is 3*3 intrinsic,
    %       calib.R is 3*3 world rotation matrix,
    %       calib.t is 3*1 world translation vector
    % ratio is physical(in mm) to geometric depth value ratio
    % p2d is n*3 array, p3d is n*3 array
    
    if nargin < 3
        scale = 1;
    else
        scale = ratio / 1000;
    end
    
    [rows, cols, vals] = find(dmap);
    nPoint = length(rows);
    vals = vals * scale;
    
    p2d = zeros(nPoint, 3);
    p2d(:, 1) = cols-1;
    p2d(:, 2) = rows-1;
    p2d(:, 3) = vals;
    
    p3d = P2dtoP3d(p2d, calib);
    
    if nargout > 2
        vmap = CalDmap2Vmap(dmap, p3d);
    end
    
end