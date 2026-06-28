import numpy as np
from nbody.constants import *


# Kinetic Energy
def KE(m, v): return 0.5 * m * np.dot(v, v)


# Potential Energy
def PE(m1, m2, r1, r2, option):
    r_vec = r1 - r2
    r2_val = np.dot(r_vec, r_vec)

    if option == 0:
        r = np.sqrt(r2_val)
        return -m1 * m2 / r
    else:
        return -m1 * m2 / np.sqrt(r2_val + epsilon ** 2)


# Linear Momentum
def P(m, v): return m * np.array(v)


# Angular Momentum
def L(m, r, v): return m * (r[0] * v[1] - r[1] * v[0])


# Total Energy
def energy(bodies, option):
    ke = 0.0
    pe = 0.0

    for i, body in enumerate(bodies):
        ke += KE(body.mass, body.velocity)
        for j in range(i + 1, len(bodies)):
            pe += PE(body.mass, bodies[j].mass, body.position, bodies[j].position, option)
    return ke + pe


# Total Linear Momentum
def linear_momentum(bodies):
    current_p = np.array([0.0, 0.0])
    for body in bodies:
        current_p += P(body.mass, body.velocity)
    return current_p


# Total Angular Momentum
def angular_momentum(bodies):
    current_l = 0
    for body in bodies:
        current_l += L(body.mass, body.position, body.velocity)
    return current_l


def calculate_validation_step(bodies, option, E0, P0, L0, e, p, l, abs_e, abs_p, abs_l, rel_e, rel_p, rel_l):
    nom_E = abs(E0) if abs(E0) > 1e-15 else 1.0
    nom_P = np.linalg.norm(P0) if np.linalg.norm(P0) > 1e-15 else 1.0
    nom_L = abs(L0) if abs(L0) > 1e-15 else 1.0

    E_current = energy(bodies, option)
    P_current = linear_momentum(bodies)
    L_current = angular_momentum(bodies)

    err_e_abs = abs(E_current - E0)
    err_p_abs = np.linalg.norm(P_current - P0)
    err_l_abs = abs(L_current - L0)

    e.append(E_current)
    p.append(np.linalg.norm(P_current))
    l.append(L_current)

    abs_e.append(err_e_abs)
    abs_p.append(err_p_abs)
    abs_l.append(err_l_abs)

    rel_e.append((err_e_abs / nom_E) * 100)
    rel_p.append((err_p_abs / nom_P) * 100)
    rel_l.append((err_l_abs / nom_L) * 100)
