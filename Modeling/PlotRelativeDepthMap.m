function PlotRelativeDepthMap(p3d)

dmax = -1.5;
dmin = -3.5;
np = size(p3d, 1);
c = linspace(dmin, dmax, np);
[z, I] = sort(p3d(:, 3), 1);
x = p3d(I, 1);
y = p3d(I, 2);
scatter3(z, x, y, 4, -c, '.');
axis equal; view(120,15); % camlight;
xlabel 'z', ylabel 'x', zlabel 'y';

end