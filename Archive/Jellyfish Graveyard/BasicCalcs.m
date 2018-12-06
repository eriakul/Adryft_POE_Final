clear all
close all


AIR_DENSITY = 1.225;        %kg/m^3
HELIUM_DENSITY = 0.179;     %kg/m^3
num_legs = 1;               %unitless
radius = 0.5;               %m
skirt_height = radius / 2;  %m
servo_mass = 0.009;         %kg

% This is the linear density of paper mache, assuming 50-50 split between
% paper and glue, and an area of 0.005m by 0.025m
skirt_lin_density = 0.0916; %kg/m
g = -9.8;                   %m/s^2

figure
radii = linspace(0.1, 0.8, 100);
res = zeros(size(radii));
volumes = zeros(size(radii));
for index = 1:length(radii)
    radius = radii(index);
    skirt_height = radius / 2;
    volume = radius^3 * 4 * pi / 3;
    f_bouy = volume * AIR_DENSITY * -g;
    f_lift = f_bouy - (volume * HELIUM_DENSITY * -g);
    max_mass = f_lift / -g;
    skirt_radius = sqrt(radius^2 - (radius - skirt_height)^2);
    skirt_mass = skirt_radius * skirt_lin_density;
    servos_mass = servo_mass * num_legs;
    available_mass = max_mass - skirt_mass - servos_mass;
    mass_per_leg = available_mass / num_legs;
    res(index) = mass_per_leg * 1000;
    volumes(index) = volume;
end
[hAx, leg_info, volume_info] = plotyy(radii, res, radii, volumes);
ylabel(hAx(1), 'Leg Mass (g)');
ylabel(hAx(2), 'Volume (m^3)');
title('Payload Mass and Volume of Helium vs. Balloon Radius')
xlabel('Balloon Radius (m)')