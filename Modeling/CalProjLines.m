function [from, ray] = CalProjLines(calib, mask)
%计算ray

K = calib.K;

%将二维坐标转换为三维坐标
[I, J] = find(mask);
pts = [J I ones(length(I), 1)];
pts = K\pts';
%对数组A和B应用函数句柄fun指定的运算
pts = bsxfun(@rdivide, pts(1:2, :), pts(3, :));
pts = [pts; ones(1, size(pts, 2))];

from = zeros(3, size(pts, 2));
ray = pts - from;

end