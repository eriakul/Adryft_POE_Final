%% Tentacle Motion Profile Analysis
% Jonathan Zerez
% Fall 2018

clear all
close all
LEG_MOUNT = [0; 0];         %m; m
LEG_LENGTH = 1.3;           %m
SMA_LENGTH_INITIAL = 0.96;  %m
SMA_DELTA_LENGTH = 0.05;    %percent
MOUNT_ANGLE = deg2rad(-75); %rad
SMA_MOUNT = [-0.1; -0.4];   %m; m
LEG_CENTER_ANGLE = pi/2 + MOUNT_ANGLE;    %rad

figure
sma_lengths = linspace(SMA_LENGTH_INITIAL, SMA_LENGTH_INITIAL * (1 - SMA_DELTA_LENGTH), 50);
for sma_length = sma_lengths
   leg_radius = calc_leg_radius(sma_length, SMA_MOUNT, LEG_LENGTH, LEG_CENTER_ANGLE, 500, 0)
   [x, y] = pol2cart(LEG_CENTER_ANGLE, -leg_radius);
   leg_center = [x; y];
   
   leg_theta = LEG_LENGTH / leg_radius;
   thetas = linspace(0, leg_theta, 20);
   leg_points = zeros(2, length(thetas));
   for index = 1:length(thetas)
       [x, y] = pol2cart(LEG_CENTER_ANGLE - thetas(index), leg_radius);
       leg_points(:, index)= [x; y] + leg_center;
   end
   
   clf
   hold on
   axis equal
   scatter(leg_points(1, :), leg_points(2, :))
   plot([-2, 2], [-2*tan(MOUNT_ANGLE), 2*tan(MOUNT_ANGLE)], 'k:')
   plot([-8, 8], [-8*tan(LEG_CENTER_ANGLE), 8*tan(LEG_CENTER_ANGLE)], 'k--')
   plot(SMA_MOUNT(1), SMA_MOUNT(2), 'rs')
   plot([SMA_MOUNT(1), leg_points(1, end)], [SMA_MOUNT(2), leg_points(2, end)], 'r--')
   ylim([-2, 1])
   xlim([-1, 1])
   drawnow
   pause(0.01)
end

%%Functions
function radius = calc_leg_radius(R_desired, O, s, theta, steps, debug)
    r_min = s / (pi / 2);
    r_max = s / (pi / 500);
    rs = linspace(r_min, r_max, steps);
    error = zeros(size(rs));
    
    for index = 1:length(rs)
        r = rs(index);
        phi = theta - (s / r);
        [center_x, center_y] = pol2cart(theta, -r);
        endpoint = [cos(phi) * r; sin(phi) * r] + [center_x; center_y];
        if debug
            plot(center_x, center_y, 'b*')
            plot(endpoint(1), endpoint(2), 'k*', 'MarkerSize', 10)
            viscircles([center_x, center_y], r)
        end
        R_calc = norm(O - endpoint);
        error(index) = R_calc - R_desired;
    end
    [minimum, ind] = min(abs(error));
    radius = rs(ind);
    
end