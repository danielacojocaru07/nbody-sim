import numpy as np
import random as rd
from math import *
from nbody.constants import *


class Body:
    def __init__(self, mass, position, velocity):
        self.mass = float(mass)
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.zeros(2, dtype=float)

    def __repr__(self):
        pos_str = np.array2string(self.position, formatter={'float_kind': lambda x: f"{x:.6f}"})
        vel_str = np.array2string(self.velocity, formatter={'float_kind': lambda x: f"{x:.6f}"})
        acc_str = np.array2string(self.acceleration, formatter={'float_kind': lambda x: f"{x:.6f}"})

        return (
            f"mass: {self.mass:.6f}, "
            f"pos: {pos_str}, "
            f"vel: {vel_str}, "
            f"acc: {acc_str}"
        )


class KeplerBody(Body):
    def __init__(self, mass, position, velocity):
        super().__init__(mass, position, velocity)
        self.mu = 0
        self.a = 0
        self.e = 0
        self.n = 0
        self.M0 = 0
        self.arg_perigee = 0

    def init_orbit(self, central_body):
        r_vec = self.position - central_body.position
        v_vec = self.velocity - central_body.velocity

        r_mag = np.linalg.norm(r_vec)
        v_mag_sq = np.dot(v_vec, v_vec)

        self.mu = central_body.mass + self.mass
        self.a = 1.0 / ((2.0 / r_mag) - (v_mag_sq / self.mu))

        rdotv = np.dot(r_vec, v_vec)

        v2_mur = v_mag_sq - self.mu / r_mag

        e_vec = (v2_mur * r_vec - rdotv * v_vec) / self.mu
        self.e = np.linalg.norm(e_vec)

        self.arg_perigee = atan2(e_vec[1], e_vec[0])
        self.n = sqrt(self.mu / (self.a ** 3))

        cos_nu = np.clip(np.dot(e_vec, r_vec) / (self.e * r_mag), -1.0, 1.0)

        nu0 = np.arccos(cos_nu)
        if rdotv < 0:
            nu0 = 2 * pi - nu0

        E0 = 2 * atan2(
            sqrt(1 - self.e ** 2) * sin(nu0),
            1 - self.e * cos(nu0)
        )

        self.M0 = E0 - self.e * sin(E0)

    def step_kepler(self, t, central_body):
        M = (self.M0 + self.n * t) % (2 * pi)

        E_val = M
        delta = 1

        for _ in range(50):
            f = E_val - self.e * sin(E_val) - M
            f_prime = 1 - self.e * cos(E_val)

            delta = f / f_prime
            E_val -= delta

            if abs(delta) < 1e-12: break

        x_p = self.a * (cos(E_val) - self.e)
        y_p = self.a * sqrt(1 - self.e ** 2) * sin(E_val)

        r_inst = self.a * (1 - self.e * cos(E_val))
        v_factor = sqrt(self.mu * self.a) / r_inst

        vx_p = -v_factor * sin(E_val)
        vy_p = v_factor * sqrt(1 - self.e ** 2) * cos(E_val)

        cos_ap = cos(self.arg_perigee)
        sin_ap = sin(self.arg_perigee)

        x_rel = x_p * cos_ap - y_p * sin_ap
        y_rel = x_p * sin_ap + y_p * cos_ap

        vx_rel = vx_p * cos_ap - vy_p * sin_ap
        vy_rel = vx_p * sin_ap + vy_p * cos_ap

        Mtot = self.mass + central_body.mass

        self.position = np.array([
            -(central_body.mass / Mtot) * x_rel,
            -(central_body.mass / Mtot) * y_rel
        ])

        central_body.position = np.array([
            (self.mass / Mtot) * x_rel,
            (self.mass / Mtot) * y_rel
        ])

        self.velocity = np.array([
            -(central_body.mass / Mtot) * vx_rel,
            -(central_body.mass / Mtot) * vy_rel
        ])

        central_body.velocity = np.array([
            (self.mass / Mtot) * vx_rel,
            (self.mass / Mtot) * vy_rel
        ])


class EulerBody(Body):
    def update_accelerations(self, others):
        accelerations = np.zeros(2, dtype=float)

        for other in others:
            if other is self: continue

            r_vec = other.position - self.position
            r_mag = np.linalg.norm(r_vec)

            accelerations += other.mass * r_vec / (r_mag ** 2 + epsilon ** 2) ** 1.5

        self.acceleration[:] = accelerations

    def update_velocity_positions(self, dt):
        # Semi-Implicit Euler (Euler-Cromer) Method
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt


class VerletBody(Body):
    def __init__(self, mass, position, velocity):
        super().__init__(mass, position, velocity)
        self.old_acceleration = np.zeros(2, dtype=float)

    def update_acceleration(self, others):
        # store old acceleration
        self.old_acceleration = self.acceleration.copy()
        acc = np.zeros(2, dtype=float)
        for other in others:
            if other is self: continue
            r_vec = other.position - self.position
            r_sq_eps = np.dot(r_vec, r_vec) + epsilon ** 2
            acc += other.mass * r_vec / (r_sq_eps ** 1.5)
        self.acceleration = acc

    def update_velocity(self, dt):
        self.velocity += 0.5 * (self.old_acceleration + self.acceleration) * dt

    def update_position(self, dt):
        self.position += (self.velocity * dt + 0.5 * self.acceleration * dt ** 2)


class RK4Body(Body):
    def __init__(self, mass, position, velocity):
        super().__init__(mass, position, velocity)
        # k vectors (velocity + acceleration samples)
        self.kv = [np.zeros(2) for _ in range(4)]
        self.ka = [np.zeros(2) for _ in range(4)]
        # temporary states
        self.temp_pos = np.zeros(2)
        self.temp_vel = np.zeros(2)

    def get_acceleration(self, others):
        acc = np.zeros(2)
        for other in others:
            if other is self: continue
            r_vec = other.temp_pos - self.temp_pos
            r2_epsilon = np.dot(r_vec, r_vec) + epsilon ** 2
            acc += other.mass * r_vec / (r2_epsilon ** 1.5)
        return acc


def generate_bodies(option, N):
    bodies = []

    sum_vx = 0.0
    sum_vy = 0.0

    for i in range(N):
        mass = rd.uniform(0.5, 2)

        x_pos = rd.uniform(-1, 1)
        y_pos = rd.uniform(-1, 1)

        if i < N - 1:
            vx = rd.uniform(-2e4, 2e4) * TU_AU
            vy = rd.uniform(-2e4, 2e4) * TU_AU

            sum_vx += mass * vx
            sum_vy += mass * vy

        else:
            vx = -sum_vx / mass
            vy = -sum_vy / mass

        pos = np.array([x_pos, y_pos], dtype=float)
        vel = np.array([vx, vy], dtype=float)

        if option == 0:
            body = KeplerBody(mass, pos, vel)
        elif option == 1:
            body = EulerBody(mass, pos, vel)
        elif option == 2:
            body = VerletBody(mass, pos, vel)
        elif option == 3:
            body = RK4Body(mass, pos, vel)

        bodies.append(body)
        print(f"Body {i + 1}: {body}")

    return bodies
