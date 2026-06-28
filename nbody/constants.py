from math import sqrt

G_REAL = 6.6743e-11  # gravitational constant
G = 1

MU = 1e30
AU = 149597870700  # ≈ 1.5e11

TU = sqrt(AU ** 3 / (G_REAL * MU))  # ​≈ 7 082 478 seconds ≈ 82 days
TU_AU = TU / AU  # used for generating bodies' velocities

dt = 0.001  # time step in time units
steps = 2000

epsilon = 0.05  # softening parameter
