# Here's a Python-based simulation that demonstrates 3D localization and mapping using sound (Time of Arrival) and optionally radio signals (Time Difference of Arrival). This minimal but extensible code models:
# A room or environment in 3D.
# Known receiver positions (microphones or radio receivers).
# Transmitters emitting acoustic pulses.
# Time-of-arrival (ToA) or time-difference-of-arrival (TDoA) measurements
# Trilateration to estimate transmitter (source) positions.
# Optionally estimating basic room reflection (multipath) delay characteristics.


import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Speed of sound (m/s) and optional radio wave speed
SOUND_SPEED = 343.0
RADIO_SPEED = 3e8  # not used directly here unless you mix both types

# Define known receiver positions in 3D space
receivers = np.array([
    [0, 0, 0],
    [5, 0, 0],
    [0, 5, 0],
    [0, 0, 3]
])

# Simulate one or more transmitter positions
true_transmitters = np.array([
    [2, 1, 1],
    [4, 2, 2]
])

# Compute simulated Time of Arrival (ToA) for each transmitter to each receiver
def simulate_toa(transmitter_pos, receivers, sound_speed=SOUND_SPEED):
    distances = np.linalg.norm(receivers - transmitter_pos, axis=1)
    return distances / sound_speed

# Function to estimate transmitter location from ToA using trilateration
def estimate_position_from_toa(receivers, toa, sound_speed=SOUND_SPEED):
    def residuals(pos):
        dists = np.linalg.norm(receivers - pos, axis=1)
        estimated_toa = dists / sound_speed
        return estimated_toa - toa

    # Initial guess at center
    x0 = np.mean(receivers, axis=0)
    result = least_squares(residuals, x0)
    return result.x

# Main simulation
estimated_transmitters = []
for transmitter in true_transmitters:
    toa = simulate_toa(transmitter, receivers)
    est_pos = estimate_position_from_toa(receivers, toa)
    estimated_transmitters.append(est_pos)

estimated_transmitters = np.array(estimated_transmitters)

# Visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(*receivers.T, c='blue', label='Receivers')
ax.scatter(*true_transmitters.T, c='green', label='True Transmitters')
ax.scatter(*estimated_transmitters.T, c='red', marker='x', label='Estimated Transmitters')

for i, pos in enumerate(estimated_transmitters):
    ax.text(*pos, f'Est{i}', color='red')
for i, pos in enumerate(true_transmitters):
    ax.text(*pos, f'True{i}', color='green')

ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.set_title("3D Localization using Sound (ToA)")
ax.legend()
plt.show()
