% =========================================================================
% VISUALIZE_JOHN_ELLIPSOID_2D
% Compute and visualize the John's ellipsoid (maximum volume inscribed ellipsoid)
% for a 2D convex polygon using YALMIP and a semidefinite solver.
%
% Requirements:
% - YALMIP (https://yalmip.github.io/)
% - SeDuMi or SDPT3 solver
%
% Author: willweiao
% =========================================================================

clc; clear; close all;

%% Step 1: Generate random 2D points and compute convex hull
n_points = 20;
points = rand(n_points, 2);
hull_idx = convhull(points(:,1), points(:,2));

% Visualize the convex polygon
fill(points(hull_idx,1), points(hull_idx,2), [0.85 0.9 1], ...
    'EdgeColor','k','FaceAlpha',0.5); hold on;
plot(points(:,1), points(:,2), 'ko', 'MarkerFaceColor', 'k');
axis equal;
xlabel('x'); ylabel('y');
title('2D Convex Polygon and John''s Ellipsoid');

%% Step 2: Define YALMIP variables
yalmip('clear');
a = sdpvar(2,1);     % Center of ellipsoid
P = sdpvar(2,2);     % Shape matrix (positive definite)

