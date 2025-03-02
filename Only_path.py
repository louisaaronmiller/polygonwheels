import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_trail(frames: int, total_translation: int, polygon_sides: int, radius: float):
    """Plots the trail with the polygon's point downwards and properly aligned with the trail."""

    # Parameters
    theta_max = 2 * np.pi
    dtheta = theta_max / frames

    # Function to create a regular polygon
    def create_polygon(sides, radius):
        angle = 2 * np.pi / sides
        vertices = np.array([[radius * np.cos(i * angle), radius * np.sin(i * angle)] for i in range(sides)])
        return vertices

    # Create the figure
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(-0.35, 3.1)
    ax.set_ylim(-0.6, -0.2)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.5)

    # Dashed horizontal line (baseline)
    line_x = np.linspace(-1, total_translation + 1, 100)
    line_y = np.zeros_like(line_x)
    ax.plot(line_x, line_y, 'k--', lw=0.8)

    # Create polygon
    poly = create_polygon(polygon_sides, radius)

    # Road function (trail storage)
    trail_x, trail_y = [], []
    cumulative_translation = 0

    # Compute trail
    for frame in range(frames):
        theta = frame * dtheta
        R = np.array([[-np.cos(theta), np.sin(theta)], 
                      [np.sin(theta), np.cos(theta)]])
        tpoly = np.dot(poly, R.T) + [cumulative_translation, 0]

        # Find lowest two points
        sorted_vertices = tpoly[np.argsort(tpoly[:, 1])]
        bottom1, bottom2 = sorted_vertices[:2]
        x1, y1 = bottom1
        x2, y2 = bottom2

        if x1 == x2:
            rim_y = min(y1, y2)
        else:
            slope = (y2 - y1) / (x2 - x1)
            rim_y = y1 + slope * (cumulative_translation - x1)

        # Update translation
        r = abs(rim_y)
        dx = r * dtheta
        cumulative_translation += dx

        # Store trail
        trail_x.append(cumulative_translation)
        trail_y.append(rim_y)

    # Plot the trail
    ax.plot(trail_x, trail_y, 'go', markersize=1.5, label="Trail")

    # Place the polygon at a specific position
    index = len(trail_x) // 2  # Choose any index to place the polygon
    poly_at_trail = poly + [trail_x[index], trail_y[index]]

    # Rotate the polygon so that the point is downward
    angle = np.pi / 2  # Rotate 90 degrees counterclockwise to point down
    R = np.array([[np.cos(angle), -np.sin(angle)], 
                  [np.sin(angle), np.cos(angle)]])
    rotated_poly = np.dot(poly_at_trail, R.T)

    # Draw the polygon
    plt.show()

# Call the function
plot_trail(frames=700, total_translation=5, polygon_sides=3, radius=0.5)
