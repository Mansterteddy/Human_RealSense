function normals = CalDptNrms(vmap)
%
% Calculate normals for depth map pixels
%
% Input:
%        vmap: iH*iW*3 array, 3d depth point positions for each depth
%              pixel.
%
% Output:
%        normals: m*3 array, 3d normals of each depth pixel.
%
% Method:
%     Step 1. n(u)=(v(x+1,y)-v(x,y))¡Á(v(x,y+1)-v(x,y)), 叉乘
%     Step 2. n(u) = n(u)/|n(u)|.
%
% Reference:
%     S.Izadi et al., "KinectFusion: Real-time 3D Reconstruction and
%  Interaction Using a Moving Depth Camera", ISMAR 2013.
%

% get v1=v(x,y)
uu1 = squeeze(vmap(:,:,1));
vv1 = squeeze(vmap(:,:,2));
dd1 = squeeze(vmap(:,:,3));

% define extened vmap
[iH, iW] = size(uu1);
vmap_ext = zeros(iH+2, iW+2, 3);
vmap_ext(2:iH+1, 2:iW+1, :) = vmap;
vmap_ext(2:iH+1, 1, :) = vmap(:,1,:); % left column
vmap_ext(2:iH+1, iW+2, :) = vmap(:,iW,:); % right column
vmap_ext(1, 2:iW+1, :) = vmap(1, :, :); % top row
vmap_ext(iH+2, 2:iW+1, :) = vmap(iH, :, :); % bottom row

% get v2=v(x+1,y)
uu2 = squeeze(vmap_ext(3:iH+2, 2:iW+1, 1));
vv2 = squeeze(vmap_ext(3:iH+2, 2:iW+1, 2));
dd2 = squeeze(vmap_ext(3:iH+2, 2:iW+1, 3));

% calculate v21=v2-v1
uu21 = reshape((uu2-uu1)', 1, iH*iW)';
vv21 = reshape((vv2-vv1)', 1, iH*iW)';
dd21 = reshape((dd2-dd1)', 1, iH*iW)';

% get v3=v(x,y+1)
uu3 = squeeze(vmap_ext(2:iH+1, 3:iW+2, 1));
vv3 = squeeze(vmap_ext(2:iH+1, 3:iW+2, 2));
dd3 = squeeze(vmap_ext(2:iH+1, 3:iW+2, 3));

% calculate v31=v3-v1
uu31 = reshape((uu3-uu1)', 1, iH*iW)';
vv31 = reshape((vv3-vv1)', 1, iH*iW)';
dd31 = reshape((dd3-dd1)', 1, iH*iW)';

% calculate n(u)=v21¡Áv31
n1 = vv21.*dd31 - dd21.*vv31;
n2 = dd21.*uu31 - uu21.*dd31;
n3 = uu21.*vv31 - vv21.*uu31;

% calculate n(u) = n(u)/|n(u)|
crs_nrm = sqrt(n1.*n1+n2.*n2+n3.*n3);
n1 = reshape(n1./crs_nrm, iW, iH)';
n2 = reshape(n2./crs_nrm, iW, iH)';
n3 = reshape(n3./crs_nrm, iW, iH)';

% remove possible NaN
ind = isnan(n1);
n1(ind) = 0;
ind = isnan(n2);
n2(ind) = 0;
ind = isnan(n3);
n3(ind) = 0;

ind = find(abs(dd1) > 0);
normals(:,1) = n1(ind);
normals(:,2) = n2(ind);
normals(:,3) = n3(ind);

end






















