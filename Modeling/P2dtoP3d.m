function p3d = P2dtoP3d(p2d, calib)
    %Cast 2d point to 3d point

    nPoint = size(p2d, 1);
    
    p2d1 = zeros(nPoint, 3);
    p2d1(:, 1) = p2d(:, 1).*p2d(:, 3); % col
    p2d1(:, 2) = p2d(:, 2).*p2d(:, 3); % row
    p2d1(:, 3) = p2d(:, 3);
    
    p3d = bsxfun(@minus, calib.K\p2d1', calib.t);
    p3d = calib.R\p3d;
    p3d = p3d';

end