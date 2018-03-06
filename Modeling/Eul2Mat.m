function rotMat = Eul2Mat(angle, order)
    % ROTATIONMATRIX Compute the rotation matrix for an angle in each direction.
    % Here we assume we rotate z, then x then y.
    if nargin<2
        order='zyx';
    end
    c1 = cos(angle(1)); % The x angle
    c2 = cos(angle(2)); % The y angle
    c3 = cos(angle(3)); % The z angle
    s1 = sin(angle(1));
    s2 = sin(angle(2));
    s3 = sin(angle(3));

    rotMat = eye(3);
    for i = 1:length(order)
        switch order(i)
        case 'x'
            rotMat = [1 0 0; 0  c1 s1; 0 -s1 c1]*rotMat;
        case 'y'
            rotMat = [c2 0 -s2; 0 1 0;  s2 0 c2]*rotMat;
        case 'z' 
            rotMat = [c3 s3 0; -s3 c3 0; 0 0 1]*rotMat;
        end 
    end
    rotMat = rotMat';
    
end