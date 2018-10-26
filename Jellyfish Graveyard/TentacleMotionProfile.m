%% Tentacle Motion Profile Analysis
% Jonathan Zerez
% Fall 2018

clear all
close all
TOTAL_TIME = 1;             %s
POSITIONS = 20;             %unitless
DRAG_COEF = 2;              %unitless
NUM_LEG_POINTS = 50;        %unitless
PAPER_DENSITY = 250;        %kg/m3
PAPER_THICKNESS = 0.0001;   %m
NUM_LEGS = 6;               %unitless
LEG_MOUNT = [0; 0];         %m; m
LEG_LENGTH = 1.3;           %m
SMA_LENGTH_INITIAL = 1.121; %m
SMA_DELTA_LENGTH = 0.05;    %percent
MOUNT_ANGLE = deg2rad(-60); %rad
SMA_MOUNT = [-0.05; -0.25];   %m; m
LEG_CENTER_ANGLE = pi/2 + MOUNT_ANGLE;    %rad

section_length = LEG_LENGTH / NUM_LEG_POINTS;
CROSS_SECTION = linspace(0.05, .95, NUM_LEG_POINTS);       %m


figure
sma_lengths = linspace(SMA_LENGTH_INITIAL, SMA_LENGTH_INITIAL * (1 - SMA_DELTA_LENGTH), POSITIONS);
thetas = linspace(0, LEG_LENGTH / 999999, NUM_LEG_POINTS);
leg_profile = CROSS_SECTION .* ones(size(thetas));
dt = TOTAL_TIME / POSITIONS;
[leg_points, leg_angles] = calc_leg_points(999999, thetas, LEG_CENTER_ANGLE);
prev_leg_points = leg_points;
thrusts = zeros([2, NUM_LEG_POINTS, POSITIONS]);


h = figure;
filename = 'animation.gif';

for index = 1:length(sma_lengths)
   sma_length = sma_lengths(index);
   leg_radius = calc_leg_radius(sma_length, SMA_MOUNT, LEG_LENGTH, LEG_CENTER_ANGLE, 100000, 0);
   leg_theta = LEG_LENGTH / leg_radius;
   thetas = linspace(0, leg_theta, NUM_LEG_POINTS);
   [leg_points, leg_angles] = calc_leg_points(leg_radius, thetas, LEG_CENTER_ANGLE);
   velocities = (leg_points - prev_leg_points) / dt;
   drag_vectors = calc_drag_force(leg_angles, velocities, leg_profile, section_length, DRAG_COEF);
   thrusts(:, :, index) = drag_vectors;
   prev_leg_points = leg_points;
   clf
   hold on
   axis equal
   scatter(leg_points(1, :), leg_points(2, :))
   plot([-2, 2], [-2*tan(MOUNT_ANGLE), 2*tan(MOUNT_ANGLE)], 'k:')
   plot([-8, 8], [-8*tan(LEG_CENTER_ANGLE), 8*tan(LEG_CENTER_ANGLE)], 'k--')
   plot(SMA_MOUNT(1), SMA_MOUNT(2), 'rs')
   plot([SMA_MOUNT(1), leg_points(1, end)], [SMA_MOUNT(2), leg_points(2, end)], 'r--')
   quiver(leg_points(1, :), leg_points(2, :), drag_vectors(1,:), drag_vectors(2,:))
   quiver(leg_points(1, :), leg_points(2, :), velocities(1,:), velocities(2,:))
   ylim([-2, 1])
   xlim([-1, 1])
   drawnow
   
   frame = getframe(h); 
   im = frame2im(frame); 
   [imind,cm] = rgb2ind(im,256); 
   % Write to the GIF File 
   if index == 1 
       imwrite(imind,cm,filename,'gif', 'Loopcount',inf); 
   else 
       imwrite(imind,cm,filename,'gif','WriteMode','append'); 
   end 
end

figure
total_thrusts = NUM_LEGS * squeeze(sum(sum(thrusts.^2).^0.5, 2));
vertical_thrusts = NUM_LEGS * squeeze(sum(thrusts(2, :, :), 2));
plot(dt:dt:TOTAL_TIME, total_thrusts)
title('Total Thrust vs. Time');
ylabel('Thrust (N)')
xlabel('Time (s)')

figure
plot(dt:dt:TOTAL_TIME, vertical_thrusts)
title('Vertical Thrust vs. Time');
ylabel('Thrust (N)')
xlabel('Time (s)')

Average_Vertical_Thrust = mean(vertical_thrusts)
Added_Weight_Grams = Average_Vertical_Thrust / 9.8 * 1000
leg_weight = sum(NUM_LEGS * leg_profile * CROSS_SECTION * PAPER_THICKNESS * PAPER_DENSITY)


%% Functions
function radius = calc_leg_radius(R_desired, O, s, theta, steps, debug)
    r_min = s / (pi / 3);
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


function [points, angles] = calc_leg_points(radius, thetas, center_angle)
    points = zeros(2, length(thetas));
    angles = zeros(size(1:length(thetas)));
    [x, y] = pol2cart(center_angle, -radius);
    center = [x; y];
    for index = 1:length(thetas)
        theta = center_angle - thetas(index);
        [x, y] = pol2cart(theta, radius);
        points(:, index)= [x; y] + center;
        angles(index) = theta;
    end
end

function forces = calc_drag_force(angles, velocities, cross_section, section_length, Cd)
    rho = 1.225;     %kg/m3;
    v = vecnorm(velocities);
    Fs = 0.5*Cd*rho*(v.^2).*(cross_section*section_length);
    forces = [Fs .* cos(angles); Fs .* sin(angles)];
end