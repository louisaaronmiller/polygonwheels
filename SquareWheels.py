import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as ani
from scipy.optimize import curve_fit

def Project(frames: int, total_translation: int, polygon_sides: int, radius: float) -> ani.FuncAnimation:
    '''
    frames: How many iterations of each rotation and translation - frames is also related to speed of rotation [int].

    total_translation: Total translation along x axis that the polygon takes, also sorts limits for animation graph [int].

    polygon_sides: No. of verticies within desired polygon, i.e. 10 = Decagon [int].

    radius: "Radius" of the polygon, distance from centre of polygon to a flat [float].

    return: a matplotlib.pyplot animation of the polygon rotating and translating whilst plotting the perfect road for a "smooth ride", and an approximation for this perfect road.

    Packages required: numpy, matplotlib.pyplot, matplotlib.patches, matplotlib.animation, and curve_fit from scipy.optimize 
    '''
    # Parameters
    theta_max = 2 * np.pi  # Full rotation
    dtheta = theta_max / frames  # Small rotation step per frame (dx = r * dtheta)

    # Function to create a regular polygon
    def create_polygon(sides, radius):
        angle = 2 * np.pi / sides
        vertices = np.array([[radius * np.cos(i * angle), radius * np.sin(i * angle)] for i in range(sides)])
        return vertices

    # Figure stuff
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(-1, total_translation -1)
    ax.set_ylim(-0.75, 0.75)
    ax.set_aspect('equal')
    ax.axis('on')
    ax.grid(True, alpha=0.5)

    # Dashed horz line
    line_x = np.linspace(-1, total_translation + 1, 100)
    line_y = np.zeros_like(line_x)
    line, = ax.plot(line_x, line_y, 'k--', lw=0.8)

    # Creating polygon
    poly = create_polygon(polygon_sides, radius)
    polygon = patches.Polygon(poly, closed=True, fc=(0, 0, 1, 0.1), ec=(0, 0, 1, 1))
    ax.add_patch(polygon)

    # Line segment (vertical line from centre to vertex)
    line_segment = np.array([[0, 0], [0, -radius]])
    line_polygon = patches.Polygon(line_segment, closed=False, ec='red', lw=2)
    ax.add_patch(line_polygon)

    # Road function
    trail_x, trail_y = [], []
    trail_plot, = ax.plot([], [], 'go', markersize=1.5)

    # Cumulative translation tracker
    cumulative_translation = 0

    # Quadratic fitting function (approximation for road function)
    def model_function(x, a, b, c):
        return a * x**2 + b * x + c

    # Perform curve fitting
    def perform_curve_fit():
        if len(trail_y) < 3: 
            print("Not enough data to perform curve fitting.")
            return

        thing = trail_y[:39]  # Unique segment (like First Brillouin Zone)
        bob = trail_x[:len(thing)]  # Match x values

        if len(bob) < 3:
            print("Not enough unique data points.")
            return

        params, covariance = curve_fit(model_function, bob, thing)
        a_fit, b_fit, c_fit = params
        print(f"Fitted equation: y = {a_fit:.2f}x^2 + {b_fit:.2f}x + {c_fit:.2f}") # Truncating to two decimal places

    # Update function for animation
    def update(frame):
        """ Updates the polygon and road function for each animation frame """
        nonlocal cumulative_translation  # Use nonlocal to modify outer variable

        # Rotation per frame
        theta = frame * dtheta

        # Rotation Matrix
        R = np.array([[-np.cos(theta), np.sin(theta)], 
                      [np.sin(theta), np.cos(theta)]])

        # Rotate and translate polygon
        tpoly = np.dot(poly, R.T) + [cumulative_translation, 0]
        polygon.set_xy(tpoly)

        # Get the two lowest points after sorting by y-value
        sorted_vertices = tpoly[np.argsort(tpoly[:, 1])]
        bottom1, bottom2 = sorted_vertices[:2]

        # Solve for y at the center X of the polygon
        x1, y1 = bottom1
        x2, y2 = bottom2

        if x1 == x2:  # Special case where x1 and x2 are the same
            rim_y = min(y1, y2)
        else:  # Otherwise, compute the slope and find y at cumulative_translation
            slope = (y2 - y1) / (x2 - x1)
            rim_y = y1 + slope * (cumulative_translation - x1)

        # Update vertical line segment
        tline_segment = np.array([[cumulative_translation, 0], [cumulative_translation, rim_y]])
        line_polygon.set_xy(tline_segment)

        # Calculating incremental translation
        r = abs(rim_y)  # The vertical length of the red line
        dx = r * dtheta  # Translation is proportional to rotation and line length
        cumulative_translation += dx

        # Store trail
        trail_x.append(cumulative_translation)
        trail_y.append(rim_y)

        # Update trail plot
        trail_plot.set_data(trail_x, trail_y)

        # Perform curve fitting at the final frame
        if frame == frames - 1:
            perform_curve_fit()
            plt.pause(0.1)
            plt.close(fig)

        return polygon, line_polygon, line, trail_plot

    # Create and return the animation
    animation = ani.FuncAnimation(fig, update, frames=frames, interval=30, blit=False)
    return animation

'''
Get the animation by calling the function and to view the animation plt.show()

To view different polygons in the animation change -> polygon_sides -> to the desired integer, eg. 5

To save the animation as a gif paste -> animation.save(filename="/____FILE_DIRECTORY____/____FILE_NAME____.gif", writer="pillow",fps =30) -> above plt.show() and...
below calling project function.
'''

animation = Project(frames = 700, total_translation = 5, polygon_sides = 5, radius = 0.5)
# SAVE HERE
plt.show()
