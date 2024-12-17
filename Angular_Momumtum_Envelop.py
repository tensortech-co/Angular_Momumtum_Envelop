""" import """
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from Angular_Momumtum_Envelop_Toolkit import add_boundary_to_plane, close_figure, dia_calculator, profile_forming

# Simulation Setup
calculation = profile_forming()
points, x, y, z = calculation.simulation()

# Max. Dimension of the Angular Momemtum Envelop
xdim = np.max(x)
ydim = np.max(y)
zdim = np.max(z)

# Print enevelop dimension
print('')
print(f"X-axis Size for the Angular Momentum Envelope: {xdim:.4e}")
print(f"Y-axis Size for the Angular Momentum Envelope: {ydim:.4e}")
print(f"Z-axis Size for the Angular Momentum Envelope: {zdim:.4e}")
print('')

# Calculate the diameter of the envelop
dia_cal = dia_calculator()
radius = dia_cal.process_point_cloud(points)

# Define Sliced Parts
x_sliced = np.where(x > 0, x, np.nan) # Only keep points where x > 0
y_sliced = np.where(y > 0, y, np.nan) # Only keep points where y > 0
z_sliced = np.where(z > 0, z, np.nan) # Only keep points where z > 0

# ========== Main Plot ==========
fig0 = plt.figure(0, figsize=(10, 8)) # Increase figure size for better spacing

# Compute the distance of each point from the origin
distances = np.sqrt(x**2 + y**2 + z**2)

# Plot Settings
ax0 = fig0.add_subplot(111, projection='3d')
scatter = ax0.scatter(x, y, z, c=distances, cmap='coolwarm', edgecolor='none', alpha=0.6)
ax0.set_title("Angular Momentum Envelope", fontsize=14, pad=20) # Add padding to the title

# Set axes labels with additional padding
ax0.set_xlabel('X-axis (Nms)', fontsize=12, labelpad=20)
ax0.set_ylabel('Y-axis (Nms)', fontsize=12, labelpad=20)
ax0.set_zlabel('Z-axis (Nms)', fontsize=12, labelpad=20)

# Configure axes to use scientific notation
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)     # Enable scientific notation
formatter.set_powerlimits((-2, 2)) # Adjust range for scientific notation

ax0.xaxis.set_major_formatter(formatter)
ax0.yaxis.set_major_formatter(formatter)
ax0.zaxis.set_major_formatter(formatter)

# Keep the scales for three axes to be 1:1:1
max_range = np.max([xdim, ydim, zdim])
ax0.set_xlim(-max_range, max_range)
ax0.set_ylim(-max_range, max_range)
ax0.set_zlim(-max_range, max_range)
ax0.set_aspect('equal')

# Add colorbar to show the distance mapping and adjust its position
colorbar = fig0.colorbar(scatter, ax=ax0, shrink=0.5, aspect=10, pad=0.2) # Increase `pad` for separation
colorbar.set_label('Distance to Origin (Nms)', fontsize=12, labelpad=10)

# Configure colorbar ticks with scientific notation
colorbar.formatter = formatter
colorbar.update_ticks()

# Adjust the subplot margins to prevent overlaps
fig0.subplots_adjust(left=0.2, right=0.8, top=0.85, bottom=0.15)

# Show the plot
plt.gcf().canvas.mpl_connect('key_press_event', close_figure)

# ========== Plot_x ==========
figx = plt.figure(1, figsize=(10, 8)) # Increase figure size for better spacing

# Mask and flatten arrays
valid_mask_x = ~np.isnan(x_sliced) # Mask valid points in z_sliced
x_valid = x_sliced[valid_mask_x]
y_valid = y[valid_mask_x]
z_valid = z[valid_mask_x]

# Compute distances for valid points only
distances_valid = np.sqrt(x_valid**2 + y_valid**2 + z_valid**2)

# Plot Settings
axx = figx.add_subplot(111, projection='3d')
scatter = axx.scatter(x_valid, y_valid, z_valid, c=distances_valid, cmap='coolwarm', edgecolor='none', alpha=0.6)
axx.set_title("3D Surface Plot with Slicing on X=0", fontsize=14, pad=20) # Add padding to the title

# Set axes labels with padding
axx.set_xlabel('X-axis (Nms)', fontsize=12, labelpad=20)
axx.set_ylabel('Y-axis (Nms)', fontsize=12, labelpad=20)
axx.set_zlabel('Z-axis (Nms)', fontsize=12, labelpad=20)

# Set axes limits and appearance
axx.view_init(10, 135) # Adjust the viewing angle

# Configure axes to auto-adjust limits and use scientific notation for ticks
axx.xaxis.set_major_formatter(formatter)
axx.yaxis.set_major_formatter(formatter)
axx.zaxis.set_major_formatter(formatter)

# Keep the scales for three axes to be 1:1:1
axx.set_xlim(-max_range, max_range)
axx.set_ylim(-max_range, max_range)
axx.set_zlim(-max_range, max_range)
axx.set_aspect('equal')

# Add colorbar with adjusted padding
colorbar = figx.colorbar(scatter, ax=axx, shrink=0.5, aspect=10, pad=0.2)
colorbar.set_label('Distance to Origin (Nms)', fontsize=12, labelpad=10)

# Configure colorbar ticks with scientific notation
colorbar.formatter = formatter
colorbar.update_ticks()

# Add the circle to the YZ plane
add_boundary_to_plane(axx, radius, ydim * 2, zdim * 2, 'x')

# Add a legend to identify the circle
axx.legend(loc='upper left')

# Adjust subplot margins to prevent overlaps
figx.subplots_adjust(left=0.2, right=0.8, top=0.85, bottom=0.15)

plt.gcf().canvas.mpl_connect('key_press_event', close_figure)

# ========== Plot_y ==========
figy = plt.figure(2, figsize=(10, 8))

# Mask and flatten arrays
valid_mask_y = ~np.isnan(y_sliced) # Mask valid points in z_sliced
x_valid = x[valid_mask_y]
y_valid = y_sliced[valid_mask_y]
z_valid = z[valid_mask_y]

# Compute distances for valid points only
distances_valid = np.sqrt(x_valid**2 + y_valid**2 + z_valid**2)

# Plot Settings
axy = figy.add_subplot(111, projection='3d')
scatter = axy.scatter(x_valid, y_valid, z_valid, c=distances_valid, cmap='coolwarm', edgecolor='none', alpha=0.6)
axy.set_title("3D Surface Plot with Slicing on Y=0", fontsize=14, pad=20)

# Set axes labels with padding
axy.set_xlabel('X-axis (Nms)', fontsize=12, labelpad=20)
axy.set_ylabel('Y-axis (Nms)', fontsize=12, labelpad=20)
axy.set_zlabel('Z-axis (Nms)', fontsize=12, labelpad=20)

# Set axes limits and appearance
axy.view_init(10, -45)

# Configure axes to auto-adjust limits and use scientific notation for ticks
axy.xaxis.set_major_formatter(formatter)
axy.yaxis.set_major_formatter(formatter)
axy.zaxis.set_major_formatter(formatter)

# Keep the scales for three axes to be 1:1:1
axy.set_xlim(-max_range, max_range)
axy.set_ylim(-max_range, max_range)
axy.set_zlim(-max_range, max_range)
axy.set_aspect('equal')

# Add colorbar with adjusted padding
colorbar = figy.colorbar(scatter, ax=axy, shrink=0.5, aspect=10, pad=0.2)
colorbar.set_label('Distance to Origin (Nms)', fontsize=12, labelpad=10)

# Configure colorbar ticks with scientific notation
colorbar.formatter = formatter
colorbar.update_ticks()

# Add the circle to the XZ plane
add_boundary_to_plane(axy, radius, zdim * 2, xdim * 2, 'y')

# Add a legend to identify the circle
axy.legend(loc='upper left')

# Adjust subplot margins to prevent overlaps
figy.subplots_adjust(left=0.2, right=0.8, top=0.85, bottom=0.15)

plt.gcf().canvas.mpl_connect('key_press_event', close_figure)

# ========== Plot_z ==========
figz = plt.figure(3, figsize=(10, 8))

# Mask and flatten arrays
valid_mask_z = ~np.isnan(z_sliced) # Mask valid points in z_sliced
x_valid = x[valid_mask_z]
y_valid = y[valid_mask_z]
z_valid = z_sliced[valid_mask_z]

# Compute distances for valid points only
distances_valid = np.sqrt(x_valid**2 + y_valid**2 + z_valid**2)

# Plot Settings
axz = figz.add_subplot(111, projection='3d')
scatter = axz.scatter(x_valid, y_valid, z_valid, c=distances_valid, cmap='coolwarm', edgecolor='none', alpha=0.6)
axz.set_title("3D Surface Plot with Slicing on Z=0", fontsize=14, pad=20)

# Set axes labels with padding
axz.set_xlabel('X-axis (Nms)', fontsize=12, labelpad=20)
axz.set_ylabel('Y-axis (Nms)', fontsize=12, labelpad=20)
axz.set_zlabel('Z-axis (Nms)', fontsize=12, labelpad=20)

# Set axes limits and appearance
axz.view_init(190, 135)

# Configure axes to auto-adjust limits and use scientific notation for ticks
axz.xaxis.set_major_formatter(formatter)
axz.yaxis.set_major_formatter(formatter)
axz.zaxis.set_major_formatter(formatter)

# Keep the scales for three axes to be 1:1:1
axz.set_xlim(-max_range, max_range)
axz.set_ylim(-max_range, max_range)
axz.set_zlim(-max_range, max_range)
axz.set_aspect('equal')

# Add colorbar with adjusted padding
colorbar = figz.colorbar(scatter, ax=axz, shrink=0.5, aspect=10, pad=0.2)
colorbar.set_label('Distance to Origin (Nms)', fontsize=12, labelpad=10)

# Configure colorbar ticks with scientific notation
colorbar.formatter = formatter
colorbar.update_ticks()

# Add the circle to the XY plane
add_boundary_to_plane(axz, radius, xdim * 2, ydim * 2, 'z')

# Add a legend to identify the circle
axz.legend(loc='upper left')

# Adjust subplot margins to prevent overlaps
figz.subplots_adjust(left=0.2, right=0.8, top=0.85, bottom=0.15)

plt.gcf().canvas.mpl_connect('key_press_event', close_figure)
plt.show()
