import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

def create_cog(num_teeth=8, inner_radius=0.6, outer_radius=1):
    theta = np.linspace(0, 2 * np.pi, num_teeth * 4, endpoint=False)  # 4 points per tooth
    r = np.array([(inner_radius if i % 4 == 0 or i % 4 == 3 else outer_radius) for i in range(len(theta))]) # This is to create teeth in the cogs
    x = r * np.cos(theta) # Polar -> cartesian
    y = r * np.sin(theta)
    return x, y

def plot_stationary_cog(num_teeth=8, inner_radius=0.6, outer_radius=1, centre_x=0, centre_y=0):
    # Getting a cog
    cog_x, cog_y = create_cog(num_teeth, inner_radius, outer_radius)

    # Figure configurations
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-outer_radius - 1, outer_radius + 1)
    ax.set_ylim(-outer_radius - 1, outer_radius + 1)
    ax.set_aspect('equal')
    ax.axis('off')

    # Creating a cog in the animation and putting in the centre
    cog_patch = patches.Polygon(np.column_stack((cog_x + centre_x, cog_y + centre_y)), closed=True, color='gray', ec='black', lw=2)
    ax.add_patch(cog_patch)

    plt.show()

def animate_single_cog(num_teeth=8, inner_radius=0.6, outer_radius=1, orbit_radius=3, angular_velocity=0.1, orbit_speed=0.05):
    # Getting cog shape
    cog_x, cog_y = create_cog(num_teeth, inner_radius, outer_radius)

    # Figure configuration
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(-orbit_radius - 2, orbit_radius + 2)
    ax.set_ylim(-orbit_radius - 2, orbit_radius + 2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Putting the cog in the animation
    cog_patch = patches.Polygon(np.column_stack((cog_x, cog_y)), closed=True, color='gray', edgecolor='black', lw=2)
    ax.add_patch(cog_patch)

    # Function to each frame
    def update(frame):
        # Calculating new angle for orbit
        orbit_angle = frame * orbit_speed  
        cog_centre_x = orbit_radius * np.cos(orbit_angle)
        cog_centre_y = orbit_radius * np.sin(orbit_angle)

        # Rotation of the cog
        rotation_angle = frame * angular_velocity
        rotated_x = cog_x * np.cos(rotation_angle) - cog_y * np.sin(rotation_angle)
        rotated_y = cog_x * np.sin(rotation_angle) + cog_y * np.cos(rotation_angle)

        # Translating the cog to follow the circumference of a circle
        cog_patch.set_xy(np.column_stack((rotated_x + cog_centre_x, rotated_y + cog_centre_y)))

        return cog_patch,

    # Animation
    ani = animation.FuncAnimation(fig, update, frames=360, interval=30, blit=True)

    # SAVE HERE

    plt.show()

def animate_cogs(num_teeth=8, inner_radius=0.6, outer_radius=1, orbit_radius=3, angular_velocity=0.1, orbit_speed=0.05, num_cogs=28):

    # Compute total frames for one full orbit
    total_frames = int((2 * np.pi) / orbit_speed)  # Ensures it completes a full circle

    # Get cog shape
    cog_x, cog_y = create_cog(num_teeth, inner_radius, outer_radius)

    # Figure config doo daa
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(-orbit_radius - 2, orbit_radius + 2)
    ax.set_ylim(-orbit_radius - 2, orbit_radius + 2)

    # To show its an approximation
    # ax.set_xlim(1.75, 2.75)
    # ax.set_ylim(-0.70, 0.70)

    ax.set_aspect('equal')
    ax.axis('off')

    # Storing positions 
    past_cogs = []

    # Function to update each frame
    def update(frame):

        # Calculating angle for orbit
        orbit_angle = frame * orbit_speed  

        # Clearing previous cogs to stop overlapping
        for patch in past_cogs:
            patch.remove()
        past_cogs.clear()

        # Drawing cogs around the circle at different angles
        for i in range(num_cogs):
            # Each cog follows a circular path with slight angular offset
            offset_angle = (orbit_angle + (i * 2 * np.pi / num_cogs))  # Spread cogs around the circle
            cog_centre_x = orbit_radius * np.cos(offset_angle)
            cog_centre_y = orbit_radius * np.sin(offset_angle)

            # Compute rotation of the cog (same for all)
            rotation_angle = frame * angular_velocity
            rotated_x = cog_x * np.cos(rotation_angle) - cog_y * np.sin(rotation_angle)
            rotated_y = cog_x * np.sin(rotation_angle) + cog_y * np.cos(rotation_angle)

            # Translate the cog to follow the circular path
            new_cog = patches.Polygon(np.column_stack((rotated_x + cog_centre_x, rotated_y + cog_centre_y)), 
                                      closed=True, color='gray', edgecolor='black', lw=1.5)

            past_cogs.append(new_cog)  # Store cogs
            ax.add_patch(new_cog)  # Adding cogs to fig

        return past_cogs  # Return all past cogs so they persist

    # Animation 
    ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=30, blit=False)
    #SAVE HERE

    plt.show()

'''
Calling the functions below will give (in order: top to bottom),

1: A stationary cog

2: A single cog tracing the circumference of a circle whilst spinning.

3: Multiple cogs spinning at the same cycle as eachother. This creates a "envelope" where the cog that is cog created can go around "perfectly".

In each function, there is a place at the bottom before plt.show() that you can paste a function to save each animation as a gif.
To save these gifs paste -> ani.save(filename="/____FILE_DIRECTORY____/____FILE_NAME____.gif", writer="pillow",fps =30) -> where it says #SAVE HERE in the functions.

To change variables, change them within the place where you call the functions.
Finally, comment out every function not intended for viewing, and uncomment the function desired.

'''

#plot_stationary_cog(num_teeth=8, inner_radius=0.6, outer_radius=1)

#animate_single_cog(num_teeth=8, inner_radius=0.6, outer_radius=1, orbit_radius=3, angular_velocity=0.1, orbit_speed=0.05)

#animate_cogs(num_teeth=8, inner_radius=0.6, outer_radius=1, orbit_radius=3, angular_velocity=0.1, orbit_speed=0.05, num_cogs=28)

