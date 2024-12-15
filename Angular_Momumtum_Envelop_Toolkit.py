from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
from tqdm import tqdm
import numpy as np
import json


class ang_vec:

    def __init__(self,style,skew):

        # Selecting the style of the CMG cluster to be "Conventional Type or Hanspeter's Type"
        # Torque axis to horizon is skew angle
        if style == 'conv':
            self.beta = skew    # unit: deg
        
        # Gimbal axis to horizon is skew angle
        elif style == 'hans':
            self.beta = 90-skew    # unit: deg

        # Pre-calculating the variables required in angular momemtum matrix
        self.cb = np.cos(np.deg2rad(self.beta))
        self.sb = np.sin(np.deg2rad(self.beta))

    def adj_ang_vec(self,state):

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

def dia_calculator(points):

    points = points.T

    # Compute the convex hull
    hull = ConvexHull(points)

    # Get the vertices of the convex hull
    hull_points = points[hull.vertices]

    # Find the minimum distance for all points to the convex hull
    min_distances = [np.linalg.norm(point) for point in hull_points]
    radius = min(min_distances)

    print(f"Radius of the inscribed sphere: {radius:.4e}")
    print('')

    return radius

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
        self.skew_angle = self.settings["Skew Angle"]    # unit: deg
        self.max_H = self.settings["Max. Angular Momemtum per CMG"]    # unit: Nms
        self.d_H = self.settings["Delta H for Simulation"]    # a scale factor ranging from 0 to 1
        self.d_theta = self.settings["Delta Theta for Simulation"]    # unit: deg
        self.clu_comb = self.settings['Cluster Combination']
        self.clu_styl = self.settings['Cluster Style']
        self.clu_spd = self.settings['Speed Type']
    
    def simulation(self):

        # Parameters Setup
        self.theta = np.arange(0, 360 + self.d_theta, self.d_theta)[:-1]
        self.h = np.arange(0, self.max_H, self.max_H * self.d_H)[:-1]
        self.N_theta = len(self.theta)
        self.N_h = len(self.h)
        self.config = {'Cluster Combination':self.clu_comb,    # could be adjacant pair 'adj' or pyramiad cluster 'pyr'
                  'Cluster Style':self.clu_styl,    # could be Conventional Type 'conv' or Hanspeter's Type 'hans'
                  'Speed Type':self.clu_spd}    # could be Constant-speed 'CS' or Variable-speed 'VS'
        
        print('')

        # Selection of simulator
        if self.config['Cluster Combination'] == 'adj':

            if self.config['Speed Type'] == 'CS':
                points,x,y,z = self.adj_CS()

            elif self.config['Speed Type'] == 'VS':
                points,x,y,z = self.adj_VS()

            else:
                print('Setting Error. Please select a proper speed type for the inner rotor of the CMG')
        
        elif self.config['Cluster Combination'] == 'pyr':

            if self.config['Speed Type'] == 'CS':
                points,x,y,z = self.pyr_CS()

            elif self.config['Speed Type'] == 'VS':
                points,x,y,z = self.pyr_VS()

            else:
                print('Setting Error. Please select a proper speed type for the inner rotor of the CMG')

        else:

            print('Setting Error. Please select a proper Cluster Style.')

        return points,x,y,z
    
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

        return points,x,y,z

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

        return points,x,y,z
    
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

        return points,x,y,z

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
        x = points[0, :].reshape((self.N_theta**2)*(self.N_h**2), (self.N_theta**2)*(self.N_h**2)).T
        y = points[1, :].reshape((self.N_theta**2)*(self.N_h**2), (self.N_theta**2)*(self.N_h**2)).T
        z = points[2, :].reshape((self.N_theta**2)*(self.N_h**2), (self.N_theta**2)*(self.N_h**2)).T

        return points,x,y,z
    
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
        x_circle = np.zeros_like(theta)  # Circle lies in the YZ plane (X=0)

        # Rectangular
        # Define the corners of the rectangle
        y_rect = [
             - width / 2,  # Bottom left
            width / 2,  # Bottom right
            width / 2,  # Top right
             - width / 2,  # Top left
             - width / 2  # Close the rectangle
        ]
        z_rect = [
             - length / 2,  # Bottom left
             - length / 2,  # Bottom right
            length / 2,  # Top right
            length / 2,  # Top left
             - length / 2  # Close the rectangle
        ]
        x_rect = np.zeros_like(y_rect)  # Rectangle lies in the YZ plane (X=0)

        # Plot the rectangle
        ax.plot(x_rect, y_rect, z_rect, color='red', linewidth=2, label=f'Max. Boundary (Ydim={width:.2e}, Zdim={length:.2e})')

    elif axis == 'y':

        # Circle
        z_circle = radius * np.cos(theta)
        x_circle = radius * np.sin(theta)
        y_circle = np.zeros_like(theta)  # Circle lies in the XZ plane (Y=0) 

        # Rectangular
        # Define the corners of the rectangle
        z_rect = [
             - width / 2,  # Bottom left
            width / 2,  # Bottom right
            width / 2,  # Top right
             - width / 2,  # Top left
             - width / 2  # Close the rectangle
        ]
        x_rect = [
             - length / 2,  # Bottom left
             - length / 2,  # Bottom right
            length / 2,  # Top right
            length / 2,  # Top left
             - length / 2  # Close the rectangle
        ]
        y_rect = np.zeros_like(z_rect)  # Rectangle lies in the XZ plane (Y=0)

        # Plot the rectangle
        ax.plot(x_rect, y_rect, z_rect, color='red', linewidth=2, label=f'Max. Boundary (Zdim={width:.2e}, Xdim={length:.2e})')

    elif axis == 'z':

        # Circle
        x_circle = radius * np.cos(theta)
        y_circle = radius * np.sin(theta)
        z_circle = np.zeros_like(theta)  # Circle lies in the XY plane (Z=0)

        # Rectangular
        # Define the corners of the rectangle
        x_rect = [
             - width / 2,  # Bottom left
            width / 2,  # Bottom right
            width / 2,  # Top right
             - width / 2,  # Top left
             - width / 2  # Close the rectangle
        ]
        y_rect = [
             - length / 2,  # Bottom left
             - length / 2,  # Bottom right
            length / 2,  # Top right
            length / 2,  # Top left
             - length / 2  # Close the rectangle
        ]
        z_rect = np.zeros_like(x_rect)  # Rectangle lies in the XY plane (Z=0)

        # Plot the rectangle
        ax.plot(x_rect, y_rect, z_rect, color='red', linewidth=2, label=f'Max. Boundary (Xdim={width:.2e}, Ydim={length:.2e}) Nms')

    else:
        print('Wrong input axis for the inscribed sphere.')

    # Plot the circle
    ax.plot(x_circle, y_circle, z_circle, color='green', linewidth=2, label=f'Inscribed Sphere (radius={radius:.2e}) Nms')