import json

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull
from tqdm import tqdm


class ang_vec:

    def __init__(self, style, skew):

        # Selecting the style of the CMG cluster to be "Conventional Type or Hanspeter's Type"
        # Torque axis to horizon is skew angle
        if style == 'conv':
            self.beta = skew # unit: deg

        # Gimbal axis to horizon is skew angle
        elif style == 'hans':
            self.beta = 90 - skew # unit: deg

        # Pre-calculating the variables required in angular momemtum matrix
        self.cb = np.cos(np.deg2rad(self.beta))
        self.sb = np.sin(np.deg2rad(self.beta))

    def adj_ang_vec(self, state):

        d1, h1, d4, h4 = state

        c1 = np.cos(np.deg2rad(d1))
        s1 = np.sin(np.deg2rad(d1))
        c4 = np.cos(np.deg2rad(d4))
        s4 = np.sin(np.deg2rad(d4))

        h1 = h1 * np.array([-self.cb * s1, c1, self.sb * s1])
        h4 = h4 * np.array([c4, self.cb * s4, self.sb * s4])

        h_total = h1 + h4

        return h_total

    def pyr_ang_vec(self, state):

        d1, h1, d2, h2, d3, h3, d4, h4 = state

        c1 = np.cos(np.deg2rad(d1))
        s1 = np.sin(np.deg2rad(d1))
        c2 = np.cos(np.deg2rad(d2))
        s2 = np.sin(np.deg2rad(d2))
        c3 = np.cos(np.deg2rad(d3))
        s3 = np.sin(np.deg2rad(d3))
        c4 = np.cos(np.deg2rad(d4))
        s4 = np.sin(np.deg2rad(d4))

        h1 = h1 * np.array([-self.cb * s1, c1, self.sb * s1])
        h2 = h2 * np.array([-c2, -self.cb * s2, self.sb * s2])
        h3 = h3 * np.array([self.cb * s3, -c3, self.sb * s3])
        h4 = h4 * np.array([c4, self.cb * s4, self.sb * s4])

        h_total = h1 + h2 + h3 + h4

        return h_total


def tri_ang_vec(state):

    h1, h2, h3 = state

    h1 = h1 * np.array([1, 0, 0])
    h2 = h2 * np.array([0, 1, 0])
    h3 = h3 * np.array([0, 0, 1])

    h_total = h1 + h2 + h3

    return h_total


class dia_calculator:

    def __init__(self):

        # Initialize parameters
        self.settings = settings_from_json()

        # User-defined step sizes for theta and phi
        self.theta_step = np.pi / self.settings['Wrap Shape N_theta'] # Step size for theta (10 degrees)
        self.phi_step = 2 * np.pi / self.settings['Wrap Shape N_phi'] # Step size for phi (10 degrees)

    def cartesian_to_spherical(self, x, y, z, epsilon=1e-8):
        """
        Convert Cartesian coordinates (x, y, z) to spherical coordinates (r, theta, phi),
        with a check for very short vectors that may cause errors.

        Parameters:
        - x, y, z: Cartesian coordinates
        - epsilon: Small threshold to identify near-zero vectors.

        Returns:
        - r: Radial distance
        - theta: Polar angle [0, pi]
        - phi: Azimuthal angle [0, 2*pi]
        - valid_mask: Boolean array indicating valid (non-zero length) vectors.
        """
        r = np.sqrt(x**2 + y**2 + z**2) # Radial distance
        valid_mask = r > epsilon        # Mask for vectors with valid lengths

        # Initialize theta and phi
        theta = np.zeros_like(r)
        phi = np.zeros_like(r)

        # Only compute theta and phi for valid points
        theta[valid_mask] = np.arccos(z[valid_mask] / r[valid_mask]) # Polar angle
        phi[valid_mask] = np.arctan2(y[valid_mask], x[valid_mask])   # Azimuthal angle

        # Ensure phi is in the range [0, 2*pi]
        phi[valid_mask] = np.where(phi[valid_mask] < 0, phi[valid_mask] + 2 * np.pi, phi[valid_mask])

        return r, theta, phi

    def process_point_cloud(self, points):
        """
        Process a 3D point cloud to find the longest 'r' for each (theta, phi) step
        and return the shortest 'r' among the R set.

        Parameters:
        - points: 3xN numpy array (3D Cartesian coordinates)
        - theta_step: step size for theta (polar angle)
        - phi_step: step size for phi (azimuthal angle)

        Returns:
        - R_set: 2D array storing the longest r for each (theta, phi) bin
        - shortest_r: The shortest r in the R set
        """
        # Convert to spherical coordinates
        x, y, z = points[0], points[1], points[2]
        r_values, theta_values, phi_values = self.cartesian_to_spherical(x, y, z)

        # Define theta and phi bins
        theta_bins = np.arange(0, np.pi + self.theta_step, self.theta_step) # [0, pi]
        phi_bins = np.arange(0, 2 * np.pi + self.phi_step, self.phi_step)   # [0, 2*pi]

        # Initialize R_set as a 2D array
        R_set = np.full((len(theta_bins) - 1, len(phi_bins) - 1), -np.inf)

        # Sweep through the data points using two-layer loops for theta and phi bins
        for i in range(len(theta_bins) - 1):
            for j in range(len(phi_bins) - 1):
                # Find the points that fall within the current theta and phi bin
                in_bin = (theta_values >= theta_bins[i]) & (theta_values < theta_bins[i+1]) & \
                        (phi_values >= phi_bins[j]) & (phi_values < phi_bins[j+1])

                if np.any(in_bin):                         # If there are points in the bin
                    R_set[i, j] = np.max(r_values[in_bin]) # Store the longest r in the bin

        # Find the shortest r in the R set (excluding -inf entries)
        valid_r = R_set[R_set > -np.inf]
        shortest_r = np.min(valid_r)

        print(f"Radius of the inscribed sphere: {shortest_r:.4e}")
        print('')

        return shortest_r


def settings_from_json():
    # Import simulation setting parameters from .json file
    try:
        with open('Settings.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

    except FileNotFoundError:
        print("File not found. Please check its path!")
        raise

    return data


class profile_forming:

    def __init__(self):

        # Initialize parameters
        self.settings = settings_from_json()

        # Extract the setting data
        self.skew_angle = self.settings['Skew Angle']               # unit: deg
        self.max_H = self.settings['Max. Angular Momemtum per CMG'] # unit: Nms
        self.d_H = self.settings['No. of Delta H Segment']          # a scale factor ranging from 0 to 1
        self.d_theta = self.settings['No. of Delta Theta Segment']  # unit: deg
        self.clu_comb = self.settings['Cluster Combination']
        self.clu_styl = self.settings['Cluster Style']
        self.clu_spd = self.settings['Speed Type']

    def simulation(self):

        # Parameters Setup
        self.theta = np.linspace(0, 360 - 360 / self.d_theta, self.d_theta - 1)
        self.h = np.linspace(0, self.max_H, self.d_H)
        self.N_theta = len(self.theta)
        self.N_h = len(self.h)
        self.config = {
            'Cluster Combination': self.clu_comb, # could be adjacant pair 'adj' or pyramiad cluster 'pyr'
            'Cluster Style': self.clu_styl,       # could be Conventional Type 'conv' or Hanspeter's Type 'hans'
            'Speed Type': self.clu_spd
        }                                           # could be Constant-speed 'CS' or Variable-speed 'VS'

        print('')

        # Selection of simulator
        if self.config['Cluster Combination'] == 'adj':

            if self.config['Speed Type'] == 'CS':
                points, x, y, z = self.adj_CS()

            elif self.config['Speed Type'] == 'VS':
                points, x, y, z = self.adj_VS()

            else:
                print('Setting Error. Please select a proper speed type for the inner rotor of the CMG')

        elif self.config['Cluster Combination'] == 'pyr':

            if self.config['Speed Type'] == 'CS':
                points, x, y, z = self.pyr_CS()

            elif self.config['Speed Type'] == 'VS':
                points, x, y, z = self.pyr_VS()

            else:
                print('Setting Error. Please select a proper speed type for the inner rotor of the CMG')

        elif self.config['Cluster Combination'] == '3RW':

            points, x, y, z = self.tri_RW()

        elif self.config['Cluster Combination'] == '4RW':

            points, x, y, z = self.pyr_RW()

        else:

            print('Setting Error. Please select a proper Cluster Style.')

        return points, x, y, z

    def adj_CS(self):

        points = np.zeros((3, self.N_theta**2))
        index = 0

        # Compute angular momemtum vector points
        calculator = ang_vec(self.config['Cluster Style'], self.skew_angle)
        for it1 in tqdm(self.theta, desc="Processing it1 (adj)"):
            for it4 in self.theta:
                state = np.array([it1, self.max_H, it4, self.max_H])
                points[:, index] = calculator.adj_ang_vec(state)
                index += 1

        # Reshape points for surface plot
        x = points[0, :].reshape(self.N_theta, self.N_theta).T
        y = points[1, :].reshape(self.N_theta, self.N_theta).T
        z = points[2, :].reshape(self.N_theta, self.N_theta).T

        return points, x, y, z

    def adj_VS(self):

        points = np.zeros((3, (self.N_theta**2) * (self.N_h**2)))
        index = 0

        # Compute angular momemtum vector points
        calculator = ang_vec(self.config['Cluster Style'], self.skew_angle)
        for it1 in tqdm(self.theta, desc="Processing it1 (adj)"):
            for h1 in self.h:
                for it4 in self.theta:
                    for h4 in self.h:
                        state = np.array([it1, h1, it4, h4])
                        points[:, index] = calculator.adj_ang_vec(state)
                        index += 1

        # Reshape points for surface plot
        x = points[0, :].reshape(self.N_theta * self.N_h, self.N_theta * self.N_h).T
        y = points[1, :].reshape(self.N_theta * self.N_h, self.N_theta * self.N_h).T
        z = points[2, :].reshape(self.N_theta * self.N_h, self.N_theta * self.N_h).T

        return points, x, y, z

    def pyr_CS(self):

        points = np.zeros((3, self.N_theta**4))
        index = 0

        # Compute angular momemtum vector points
        calculator = ang_vec(self.config['Cluster Style'], self.skew_angle)
        for it1 in tqdm(self.theta, desc="Processing it1 (pyr)"):
            for it2 in self.theta:
                for it3 in self.theta:
                    for it4 in self.theta:
                        state = np.array([it1, self.max_H, it2, self.max_H, it3, self.max_H, it4, self.max_H])
                        points[:, index] = calculator.pyr_ang_vec(state)
                        index += 1

        # Reshape points for surface plot
        x = points[0, :].reshape(self.N_theta**2, self.N_theta**2).T
        y = points[1, :].reshape(self.N_theta**2, self.N_theta**2).T
        z = points[2, :].reshape(self.N_theta**2, self.N_theta**2).T

        return points, x, y, z

    def pyr_VS(self):

        points = np.zeros((3, (self.N_theta**4) * (self.N_h**4)))
        index = 0

        # Compute angular momemtum vector points
        calculator = ang_vec(self.config['Cluster Style'], self.skew_angle)
        for it1 in tqdm(self.theta, desc="Processing it1 (pyr)"):
            for h1 in tqdm(self.h, desc="Processing h1 (pyr)"):
                for it2 in self.theta:
                    for h2 in self.h:
                        for it3 in self.theta:
                            for h3 in self.h:
                                for it4 in self.theta:
                                    for h4 in self.h:
                                        state = np.array([it1, h1, it2, h2, it3, h3, it4, h4])
                                        points[:, index] = calculator.pyr_ang_vec(state)
                                        index += 1

        # Reshape points for surface plot
        x = points[0, :].reshape((self.N_theta**2) * (self.N_h**2), (self.N_theta**2) * (self.N_h**2)).T
        y = points[1, :].reshape((self.N_theta**2) * (self.N_h**2), (self.N_theta**2) * (self.N_h**2)).T
        z = points[2, :].reshape((self.N_theta**2) * (self.N_h**2), (self.N_theta**2) * (self.N_h**2)).T

        return points, x, y, z

    def tri_RW(self):

        self.N_h = 2 * self.N_h
        points = np.zeros((3, self.N_h**3))
        index = 0

        # Compute angular momentum vector points
        h_range = np.concatenate([-self.h, self.h]) # Combine negative and positive ranges

        for h1 in tqdm(h_range, desc="Processing h1 (pyr)"):
            for h2 in h_range:
                for h3 in h_range:
                    state = np.array([h1, h2, h3])
                    points[:, index] = tri_ang_vec(state)
                    index += 1

                # Extract x, y, z as 1D arrays
                x = points[0, :]
                y = points[1, :]
                z = points[2, :]

        return points, x, y, z

    def pyr_RW(self):

        self.N_h = 2 * self.N_h
        points = np.zeros((3, self.N_h**4))
        index = 0

        # Compute angular momentum vector points
        h_range = np.concatenate([-self.h, self.h]) # Combine negative and positive ranges

        # Compute angular momemtum vector points
        calculator = ang_vec('hans', self.skew_angle)
        for h1 in tqdm(h_range, desc="Processing h1 (pyr)"):
            for h2 in h_range:
                for h3 in h_range:
                    for h4 in h_range:
                        state = np.array([90, h1, 90, h2, 90, h3, 90, h4])
                        points[:, index] = calculator.pyr_ang_vec(state)
                        index += 1

        # Reshape points for surface plot
        x = points[0, :].reshape(self.N_h**2, self.N_h**2).T
        y = points[1, :].reshape(self.N_h**2, self.N_h**2).T
        z = points[2, :].reshape(self.N_h**2, self.N_h**2).T

        return points, x, y, z


# Plot closing function
def close_figure(event):
    if event.key == 'escape':
        plt.close(event.canvas.figure)


# Add circle to the one of the three planes
def add_boundary_to_plane(ax, radius, width, length, axis, num_points=100):
    """
    Draw a circle in the YZ/XZ/XY plane.

    Parameters:
        ax: The 3D axes to plot on.
        radius: Radius of the circle.
        num_points: Number of points used to draw the circle.
    """
    # Parametric equation for the circle in the YZ plane
    theta = np.linspace(0, 2 * np.pi, num_points)

    if axis == 'x':

        # Circle
        y_circle = radius * np.cos(theta)
        z_circle = radius * np.sin(theta)
        x_circle = np.zeros_like(theta) # Circle lies in the YZ plane (X=0)

        # Rectangular
        # Define the corners of the rectangle
        y_rect = [
            -width / 2,                # Bottom left
            width / 2,                 # Bottom right
            width / 2,                 # Top right
            -width / 2,                # Top left
            -width / 2                 # Close the rectangle
        ]
        z_rect = [
            -length / 2,               # Bottom left
            -length / 2,               # Bottom right
            length / 2,                # Top right
            length / 2,                # Top left
            -length / 2                # Close the rectangle
        ]
        x_rect = np.zeros_like(y_rect) # Rectangle lies in the YZ plane (X=0)

        # Plot the rectangle
        ax.plot(
            x_rect,
            y_rect,
            z_rect,
            color='red',
            linewidth=2,
            zorder=6,    # Even higher zorder than the circle
            label=f'Max. Boundary (Ydim={width:.2e}, Zdim={length:.2e})')

    elif axis == 'y':

        # Circle
        z_circle = radius * np.cos(theta)
        x_circle = radius * np.sin(theta)
        y_circle = np.zeros_like(theta) # Circle lies in the XZ plane (Y=0)

        # Rectangular
        # Define the corners of the rectangle
        z_rect = [
            -width / 2,                # Bottom left
            width / 2,                 # Bottom right
            width / 2,                 # Top right
            -width / 2,                # Top left
            -width / 2                 # Close the rectangle
        ]
        x_rect = [
            -length / 2,               # Bottom left
            -length / 2,               # Bottom right
            length / 2,                # Top right
            length / 2,                # Top left
            -length / 2                # Close the rectangle
        ]
        y_rect = np.zeros_like(z_rect) # Rectangle lies in the XZ plane (Y=0)

        # Plot the rectangle
        ax.plot(
            x_rect,
            y_rect,
            z_rect,
            color='red',
            linewidth=2,
            zorder=6,    # Even higher zorder than the circle
            label=f'Max. Boundary (Zdim={width:.2e}, Xdim={length:.2e})')

    elif axis == 'z':

        # Circle
        x_circle = radius * np.cos(theta)
        y_circle = radius * np.sin(theta)
        z_circle = np.zeros_like(theta) # Circle lies in the XY plane (Z=0)

        # Rectangular
        # Define the corners of the rectangle
        x_rect = [
            -width / 2,                # Bottom left
            width / 2,                 # Bottom right
            width / 2,                 # Top right
            -width / 2,                # Top left
            -width / 2                 # Close the rectangle
        ]
        y_rect = [
            -length / 2,               # Bottom left
            -length / 2,               # Bottom right
            length / 2,                # Top right
            length / 2,                # Top left
            -length / 2                # Close the rectangle
        ]
        z_rect = np.zeros_like(x_rect) # Rectangle lies in the XY plane (Z=0)

        # Plot the rectangle
        ax.plot(
            x_rect,
            y_rect,
            z_rect,
            color='red',
            linewidth=2,
            zorder=6,    # Even higher zorder than the circle
            label=f'Max. Boundary (Xdim={width:.2e}, Ydim={length:.2e}) Nms')

    else:
        print('Wrong input axis for the inscribed sphere.')

    # Plot the circle
    ax.plot(
        x_circle,
        y_circle,
        z_circle,
        color='green',
        linewidth=2,
        zorder=5,      # Higher zorder to show above scatter points
        label=f'Inscribed Sphere (radius={radius:.2e}) Nms')
