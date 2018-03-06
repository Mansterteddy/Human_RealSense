function [dimg, simg, ind] = dmap2dimg(dmap, ratio)

    % dmap is H*W depth map, which stores physical depth value(in mm)
    % dimg is H*W gray scale depth image
    
    if nargin < 2
        ratio = 1;
    end
    
    [iH, iW] = size(dmap);
    
    % Get Depth Image
    ind = abs(dmap) > 0;
    mdmap = zeros(iH, iW); % physical depth values
    mdmap(ind) = dmap(ind) / ratio; % geometric to physical depth value
    ind = abs(mdmap) > 0;
    fg = mdmap(ind); % foreground pixels
    dmin = min(fg) - 0.1;
    dmax = max(fg);
    ddiff = dmax - dmin;
    dimg = zeros(iH, iW); % grey scale depth image
    dimg(ind) = (mdmap(ind) - dmin) / ddiff;
    
    if nargout > 1
        % Get Binary Silhouette Depth Image
        simg = zeros(iH, iW);
        simg(ind) = 1; % non-edge
%         bw = zeros(iH, iW);
%         bw(ind) = 1;
%         bw = edge(bw, 'canny'); % edge
%         simg(bw) = 1;
        
%         img = zeros(iH, iW, 3);
%         [row, col, ~] = find(dmap > 0);
%         for i = 1:length(row)
%             img(row(i), col(i), :) = [0.5 0.5 0.5];
%         end
%         [row, col, ~] = find(simg > 0);
%         for i = 1:length(row)
%             img(row(i), col(i), :) = [1 1 1];
%         end
%         figure; imshow(img);
    end

end