function vmap = CalDmap2Vmap(dmap, p3d)
%
% Calculate vertex map for depth pixel map
%

[iH, iW] = size(dmap);
ind = abs(dmap) > 0;

vmap = zeros(iH, iW, 3);

uu = zeros(iH, iW);
uu(ind) = p3d(:, 1);
vmap(:,:,1) = uu;

vv = zeros(iH, iW);
vv(ind) = p3d(:, 2);
vmap(:,:,2) = vv;

dd = zeros(iH, iW);
dd(ind) = p3d(:, 3);
vmap(:,:,3) = dd;

end













