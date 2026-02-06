import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# Setup figure and axis
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, facecolor='black')
ax.set_aspect("equal")
ax.axis("off")

# Solar system parameters
planet_data = [
    # name, orbital radius, size, color, orbital period (frames), eccentricity, moons
    ("Mercury", 1.5, 0.08, 'darkgoldenrod', 88, 0.2, 0),
    ("Venus", 2.2, 0.12, 'bisque', 225, 0.01, 0),
    ("Earth", 3.0, 0.13, 'dodgerblue', 365, 0.02, 1),
    ("Mars", 3.8, 0.11, 'tomato', 687, 0.09, 2),
    ("Jupiter", 5.5, 0.25, 'burlywood', 4333, 0.05, 4),
    ("Saturn", 7.0, 0.22, 'navajowhite', 10759, 0.06, 3),
    ("Uranus", 8.2, 0.18, 'lightcyan', 30687, 0.05, 2),
    ("Neptune", 9.5, 0.17, 'royalblue', 60190, 0.01, 1)
]

# Create starry background
np.random.seed(42)
x_stars = np.random.uniform(-12, 12, 200)
y_stars = np.random.uniform(-12, 12, 200)
sizes_stars = np.random.uniform(0.1, 2, 200)
brightness = np.random.uniform(0.1, 1, 200)
ax.scatter(x_stars, y_stars, s=sizes_stars, c='white', alpha=brightness)

# Create orbits with proper eccentricity
for planet in planet_data:
    name, r, size, color, period, e, moons = planet
    a = r / (1 - e)  # semi-major axis
    b = a * np.sqrt(1 - e**2)  # semi-minor axis
    theta = np.linspace(0, 2*np.pi, 300)
    x_orbit = a * np.cos(theta) - a * e
    y_orbit = b * np.sin(theta)
    ax.plot(x_orbit, y_orbit, color='white', linestyle='-', linewidth=0.7, alpha=0.3)

# Create Sun with glow effect
sun_cmap = LinearSegmentedColormap.from_list('sun_glow', ['yellow', 'red', 'black'])
sun_radius = 0.4
sun = plt.Circle((0, 0), sun_radius, color='yellow', zorder=20)
ax.add_artist(sun)

# Add glow effect to sun
for alpha in [0.3, 0.2, 0.1]:
    glow_radius = sun_radius + (1 - alpha) * 0.5
    glow = plt.Circle((0, 0), glow_radius, color='yellow', alpha=alpha*0.7, zorder=10)
    ax.add_artist(glow)

# Create planets and their moons
planets = []
moons = []
for i, planet in enumerate(planet_data):
    name, r, size, color, period, e, num_moons = planet
    a = r / (1 - e)
    
    # Planet
    planet_circle = plt.Circle((0, 0), size, color=color, zorder=15)
    ax.add_artist(planet_circle)
    
    # Planet label
    label = ax.text(0, 0, name, color='white', fontsize=8, ha='center', va='bottom', zorder=30)
    
    # Moons
    planet_moons = []
    for j in range(num_moons):
        moon_size = size * 0.3
        moon_orbit_radius = size * 2.5
        moon = plt.Circle((0, 0), moon_size*0.5, color='lightgray', zorder=14)
        ax.add_artist(moon)
        planet_moons.append((moon, moon_orbit_radius, 20*(j+1)))
    
    planets.append((planet_circle, label, a, e, period, planet_moons))
    moons.extend(planet_moons)

# Add asteroid belt between Mars and Jupiter
theta_asteroids = np.random.uniform(0, 2*np.pi, 100)
r_asteroids = np.random.uniform(4.2, 5.0, 100)
x_asteroids = r_asteroids * np.cos(theta_asteroids)
y_asteroids = r_asteroids * np.sin(theta_asteroids)
sizes_asteroids = np.random.uniform(0.02, 0.05, 100)
ax.scatter(x_asteroids, y_asteroids, s=sizes_asteroids, color='gray', alpha=0.7, zorder=5)

# Animation function
def update(frame):
    for planet in planets:
        circle, label, a, e, period, planet_moons = planet
        
        # Calculate planet position with eccentricity
        angle = 2 * np.pi * frame / period
        r = a * (1 - e**2) / (1 + e * np.cos(angle))
        x = r * np.cos(angle) - a * e
        y = r * np.sin(angle)
        circle.center = (x, y)
        
        # Update label position
        label.set_position((x, y + circle.get_radius() + 0.1))
        
        # Update moons
        for moon, moon_orbit_radius, moon_period in planet_moons:
            moon_angle = 2 * np.pi * frame / moon_period
            moon_x = x + moon_orbit_radius * np.cos(moon_angle)
            moon_y = y + moon_orbit_radius * np.sin(moon_angle)
            moon.center = (moon_x, moon_y)
    
    # Rotate the star background slightly for parallax effect
    if frame % 5 == 0:
        for i in range(len(x_stars)):
            distance = np.sqrt(x_stars[i]**2 + y_stars[i]**2)
            x_stars[i] += 0.001 * (12 - distance) * (-y_stars[i]) / (distance + 0.1)
            y_stars[i] += 0.001 * (12 - distance) * x_stars[i] / (distance + 0.1)
    
    return [circle for circle, _, _, _, _, _ in planets] + [moon for moon, _, _ in moons]

# Setup axis limits with some margin
ax.set_xlim(-11, 11)
ax.set_ylim(-11, 11)

# Add title
fig.suptitle('Solar System Simulation', color='white', fontsize=16, y=0.92)

# Animate with higher quality
ani = animation.FuncAnimation(
    fig, 
    update, 
    frames=1000, 
    interval=20, 
    blit=False,
    repeat=True
)

plt.tight_layout()
plt.show()

# To save the animation (uncomment if needed):
# ani.save('solar_system.mp4', writer='ffmpeg', fps=30, dpi=300)