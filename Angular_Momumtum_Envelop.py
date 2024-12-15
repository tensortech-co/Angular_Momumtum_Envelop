""" import """
from Angular_Momumtum_Envelop_Toolkit import profile_forming, dia_calculator,close_figure,add_boundary_to_plane
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Simulation Setup
calculation = profile_forming()
points,x,y,z = calculation.simulation()

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
radius = dia_calculator(points)

# Define Sliced Parts
x_sliced = np.where(x > 0, x, np.nan) # Only keep points where x > 0
y_sliced = np.where(y > 0, y, np.nan) # Only keep points where y > 0
z_sliced = np.where(z > 0, z, np.nan) # Only keep points where z > 0

# ========== Main Plot ==========
fig0 = plt.figure(0)

# Compute the distance of each point from the origin
distances = np.sqrt(x**2 + y**2 + z**2)

# Plot Settings
ax0 = fig0.add_subplot(111, projection='3d')
scatter = ax0.scatter(x, y, z, c=distances, cmap='coolwarm', edgecolor='none', alpha=0.7)
ax0.set_title("Angular Momentum Envelope", fontsize=14)

# Set axes labels
ax0.set_xlabel('X-axis (Nms)', fontsize=12)
ax0.set_ylabel('Y-axis (Nms)', fontsize=12)
ax0.set_zlabel('Z-axis (Nms)', fontsize=12)

# Configure axes to auto-adjust limits and use scientific notation for ticks
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)  # Enable scientific notation
formatter.set_powerlimits((-2, 2))  # Adjust range for scientific notation

ax0.xaxis.set_major_formatter(formatter)
ax0.yaxis.set_major_formatter(formatter)
ax0.zaxis.set_major_formatter(formatter)

# Add colorbar to show the distance mapping
colorbar = fig0.colorbar(scatter, ax=ax0, shrink=0.5, aspect=10)
colorbar.set_label('Distance to Origin (Nms)')

# Configure colorbar ticks with scientific notation
colorbar.formatter = formatter
colorbar.update_ticks()

# Adjust axis limits to enforce true 1:1:1 visual scaling
ax0.axis('equal')

plt.gcf().canvas.mpl_connect('key_press_event', close_figure)

# ========== Plot_x ==========
figx = plt.figure(1)

# Mask and flatten arrays
valid_mask_x = ~np.isnan(x_sliced) # Mask valid points in z_sliced
x_valid = x_sliced[valid_mask_x]
y_valid = y[valid_mask_x]
z_valid = z[valid_mask_x]

# Compute distances for valid points only
distances_valid = np.sqrt(x_valid**2 + y_valid**2 + z_valid**2)

# Plot Settings
axx = figx.add_subplot(111, projection='3d')
scatter = axx.scatter(x_valid, y_valid, z_valid, c=distances_valid, cmap='coolwarm', edgecolor='none', alpha=0.7)
axx.set_title("3D Surface Plot with Slicing on X=0", fontsize=14)

# Set axes labels
axx.set_xlabel('X-axis (Nms)', fontsize=12)
axx.set_ylabel('Y-axis (Nms)', fontsize=12)
axx.set_zlabel('Z-axis (Nms)', fontsize=12)

# Set axes limits and appearance
axx.view_init(10, 135) # view(37.5, 30) in MATLAB

# Configure axes to auto-adjust limits and use scientific notation for ticks
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)  # Enable scientific notation
formatter.set_powerlimits((-2, 2))  # Adjust range for scientific notation

axx.xaxis.set_major_formatter(formatter)
axx.yaxis.set_major_formatter(formatter)
axx.zaxis.set_major_formatter(formatter)

# Add colorbar to show the distance mapping
colorbar = figx.colorbar(scatter, ax=axx, shrink=0.5, aspect=10)
colorbar.set_label('Distance to Origin (Nms)')

# Configure colorbar ticks with scientific notation
colorbar.formatter = formatter
colorbar.update_ticks()

# Add the circle to the YZ plane
add_boundary_to_plane(axx, radius, ydim*2, zdim*2, 'x')

# Add a legend to identify the circle
axx.legend()

# Adjust axis limits to enforce true 1:1:1 visual scaling
axx.axis('equal')

plt.gcf().canvas.mpl_connect('key_press_event', close_figure)

# ========== Plot_y ==========
figy = plt.figure(2)

# Mask and flatten arrays
valid_mask_y = ~np.isnan(y_sliced) # Mask valid points in z_sliced
x_valid = x[valid_mask_y]
y_valid = y_sliced[valid_mask_y]
z_valid = z[valid_mask_y]

# Compute distances for valid points only
distances_valid = np.sqrt(x_valid**2 + y_valid**2 + z_valid**2)

# Plot Settings
axy = figy.add_subplot(111, projection='3d')
scatter = axy.scatter(x_valid, y_valid, z_valid, c=distances_valid, cmap='coolwarm', edgecolor='none', alpha=0.7)
axy.set_title("3D Surface Plot with Slicing on Y=0", fontsize=14)

# Set axes labels
axy.set_xlabel('X-axis (Nms)', fontsize=12)
axy.set_ylabel('Y-axis (Nms)', fontsize=12)
axy.set_zlabel('Z-axis (Nms)', fontsize=12)

# Set axes limits and appearance
axy.view_init(10, -45)

# Configure axes to auto-adjust limits and use scientific notation for ticks
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)  # Enable scientific notation
formatter.set_powerlimits((-2, 2))  # Adjust range for scientific notation

axy.xaxis.set_major_formatter(formatter)
axy.yaxis.set_major_formatter(formatter)
axy.zaxis.set_major_formatter(formatter)

# Add colorbar to show the distance mapping
colorbar = figy.colorbar(scatter, ax=axy, shrink=0.5, aspect=10)
colorbar.set_label('Distance to Origin (Nms)')

# Configure colorbar ticks with scientific notation
colorbar.formatter = formatter
colorbar.update_ticks()

# Add the circle to the XZ plane
add_boundary_to_plane(axy, radius, zdim*2, xdim*2, 'y')

# Add a legend to identify the circle
axy.legend()

# Adjust axis limits to enforce true 1:1:1 visual scaling
axy.axis('equal')

plt.gcf().canvas.mpl_connect('key_press_event', close_figure)

# ========== Plot_z ==========
figz = plt.figure(3)

# Mask and flatten arrays
valid_mask_z = ~np.isnan(z_sliced) # Mask valid points in z_sliced
x_valid = x[valid_mask_z]
y_valid = y[valid_mask_z]
z_valid = z_sliced[valid_mask_z]

# Compute distances for valid points only
distances_valid = np.sqrt(x_valid**2 + y_valid**2 + z_valid**2)

# Plot Settings
axz = figz.add_subplot(111, projection='3d')
scatter = axz.scatter(x_valid, y_valid, z_valid, c=distances_valid, cmap='coolwarm', edgecolor='none', alpha=0.7)
axz.set_title("3D Surface Plot with Slicing on Z=0", fontsize=14)

# Set axes labels
axz.set_xlabel('X-axis (Nms)', fontsize=12)
axz.set_ylabel('Y-axis (Nms)', fontsize=12)
axz.set_zlabel('Z-axis (Nms)', fontsize=12)

# Set axes limits and appearance
axz.view_init(-45, 10)

# Configure axes to auto-adjust limits and use scientific notation for ticks
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)  # Enable scientific notation
formatter.set_powerlimits((-2, 2))  # Adjust range for scientific notation

axz.xaxis.set_major_formatter(formatter)
axz.yaxis.set_major_formatter(formatter)
axz.zaxis.set_major_formatter(formatter)

# Add colorbar to show the distance mapping
colorbar = figz.colorbar(scatter, ax=axz, shrink=0.5, aspect=10)
colorbar.set_label('Distance to Origin (Nms)')

# Configure colorbar ticks with scientific notation
colorbar.formatter = formatter
colorbar.update_ticks()

# Add the circle to the XY plane
add_boundary_to_plane(axz, radius, xdim*2, ydim*2, 'z')

# Add a legend to identify the circle
axz.legend()

# Adjust axis limits to enforce true 1:1:1 visual scaling
axz.axis('equal')

plt.gcf().canvas.mpl_connect('key_press_event', close_figure)

plt.show()
