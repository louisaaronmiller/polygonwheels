import numpy as np
import sympy as sy
import matplotlib.pyplot as plt

'''
I didn't have much time to write comments for this code, but what it does is calculate some sided polygons ranging between 4-153
in increments 10 then 30 then 50, then plots them on a graph to show that they approximate a straight line as you increase
the number of sides of the polygon
'''


def create_polygon(sides, radius):
    # Create dictionary to store results
    results = {}

    # Angle between each vertex
    angle = 2 * np.pi / sides

    # Generate the vertices of the polygon
    vertices = np.array([[radius * np.cos(i * angle), radius * np.sin(i * angle)] for i in range(sides)])

    # Calculate the lengths of the sides of the polygon
    side_lengths = []
    for i in range(sides):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % sides]  # Use modulo to loop back to the first vertex
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        side_lengths.append(distance)

    # Calculate the apothem (distance from center to flat side)
    apothem = radius * np.cos(np.pi / sides)

    results['angle'] = angle
    results['vertices'] = vertices
    results['side_lengths'] = side_lengths[0]  # Store the lengths of the sides (using the first side length)
    results['apothem'] = apothem  # Store the apothem (distance to flat side)

    return results

x, y, t = sy.symbols('x y t')


side_lengths = []
apothem = []


for i in range(3, 160):
    results = create_polygon(i, 0.5)
    side_lengths.append(results['side_lengths'])
    apothem.append(results['apothem'])

def road(A, x):
    return float((-A * sy.cosh(x/A)).evalf())  

def graph(curve_index):
    A = apothem[curve_index]  
    length = side_lengths[curve_index] / 2  

    lengthlist = np.linspace(-length, length, 300)  
    return lengthlist, A


lengthlist1, A1 = graph(1)
lengthlist10, A10 = graph(10)
lengthlist20, A20 = graph(20)
lengthlist30, A30 = graph(30)
lengthlist40, A40 = graph(40)
lengthlist50, A50 = graph(50)
lengthlist80, A80 = graph(80)
lengthlist120, A120 = graph(120)
lengthlist150, A150 = graph(150)

y1 = [road(A1, x) for x in lengthlist1]
y10 = [road(A10, x) for x in lengthlist10]
y20 = [road(A20, x) for x in lengthlist20]
y30 = [road(A30, x) for x in lengthlist30]
y40 = [road(A40, x) for x in lengthlist40]
y50 = [road(A50, x) for x in lengthlist50]
y80 = [road(A80, x) for x in lengthlist80]
y120 = [road(A120, x) for x in lengthlist120]
y150 = [road(A150, x) for x in lengthlist150]

plt.plot(lengthlist1, y1)
plt.plot(lengthlist10, y10)
plt.plot(lengthlist20, y20)
plt.plot(lengthlist30, y30)
plt.plot(lengthlist40, y40)
plt.plot(lengthlist50, y50)
plt.plot(lengthlist80, y80)
plt.plot(lengthlist120, y120)
plt.plot(lengthlist150, y150)

plt.ylim(-0.5005,-0.485)
plt.xlim(-0.125,0.125)
plt.grid(True, alpha = 0.5)
plt.title("Approximations for Perfect Road for Increasing Sided Polygons")
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.grid(True)
plt.show()
