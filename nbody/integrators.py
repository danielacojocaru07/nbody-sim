from nbody.validation import *


def run_kepler(steps, dt, bodies, x, y, E0, P0, L0, e, p, l, abs_e, abs_p, abs_l, rel_e, rel_p, rel_l):
    body1 = bodies[0]
    body2 = bodies[1]

    x.clear()
    y.clear()

    x.extend([[], []])
    y.extend([[], []])

    body1.init_orbit(body2)
    current_time = 0

    for _ in range(steps):
        # UPDATE PARAMETERS
        current_time += dt
        body1.step_kepler(current_time, body2)

        # PLOT
        # Calculate validation parameters
        calculate_validation_step(bodies, 0, E0, P0, L0, e, p, l, abs_e, abs_p, abs_l, rel_e, rel_p, rel_l)

        # Add the new positions
        x[0].append(body1.position[0])
        y[0].append(body1.position[1])

        x[1].append(body2.position[0])
        y[1].append(body2.position[1])


def run_euler(steps, dt, bodies, x, y, E0, P0, L0, e, p, l, abs_e, abs_p, abs_l, rel_e, rel_p, rel_l):
    for _ in range(steps):

        # UPDATE PARAMETERS
        # Update accelerations
        for body in bodies:
            body.update_accelerations(bodies)

        # Update velocity and positions
        for body in bodies:
            body.update_velocity_positions(dt)

        # PLOT
        # Calculate validation parameters
        calculate_validation_step(bodies, 1, E0, P0, L0, e, p, l, abs_e, abs_p, abs_l, rel_e, rel_p, rel_l)

        # Add the new positions
        for i, body in enumerate(bodies):
            x[i].append(body.position[0])
            y[i].append(body.position[1])


def run_verlet(steps, dt, bodies, x, y, E0, P0, L0, e, p, l, abs_e, abs_p, abs_l, rel_e, rel_p, rel_l):
    for _ in range(steps):

        # UPDATE PARAMETERS
        # Update positions
        for body in bodies:
            body.update_position(dt)

        # Update accelerations
        for body in bodies:
            body.update_acceleration(bodies)

        # Update velocities
        for body in bodies:
            body.update_velocity(dt)

        # PLOT
        # Calculate validation parameters
        calculate_validation_step(bodies, 2, E0, P0, L0, e, p, l, abs_e, abs_p, abs_l, rel_e, rel_p, rel_l)

        # Add the new positions
        for i, body in enumerate(bodies):
            x[i].append(body.position[0])
            y[i].append(body.position[1])


def run_rk4(steps, dt, bodies, x, y, E0, P0, L0, e, p, l, abs_e, abs_p, abs_l, rel_e, rel_p, rel_l):
    for _ in range(steps):
        # UPDATE PARAMETERS

        # Step k1
        # Assign values to temporary variables
        for b in bodies:
            b.temp_pos = b.position.copy()

        # kv1 and ka1 are the current velocity and acceleration values
        for b in bodies:
            b.kv[0] = b.velocity.copy()
            b.ka[0] = b.get_acceleration(bodies)

        # Step k2
        # Calculate the temporary positions and velocities at half-step
        for b in bodies:
            b.temp_pos = b.position + b.kv[0] * dt * 0.5
            b.temp_vel = b.velocity + b.ka[0] * dt * 0.5

        # Recalculate the accelerations given the updated positions
        for b in bodies:
            b.kv[1] = b.temp_vel.copy()
            b.ka[1] = b.get_acceleration(bodies)

        # Step k3
        # Recalculate the temporary positions and velocities at half-step using past slope (velocity and acceleration)
        for b in bodies:
            b.temp_pos = b.position + b.kv[1] * dt * 0.5
            b.temp_vel = b.velocity + b.ka[1] * dt * 0.5

        for b in bodies:
            b.kv[2] = b.temp_vel.copy()
            b.ka[2] = b.get_acceleration(bodies)

        # Step k4
        # Calculate the "draft" of the final positions and velocities
        for b in bodies:
            b.temp_pos = b.position + b.kv[2] * dt
            b.temp_vel = b.velocity + b.ka[2] * dt

        for b in bodies:
            b.kv[3] = b.temp_vel.copy()
            b.ka[3] = b.get_acceleration(bodies)

        # Final Integration
        for b in bodies:
            b.position += (dt / 6.0) * (b.kv[0] + 2 * b.kv[1] + 2 * b.kv[2] + b.kv[3])
            b.velocity += (dt / 6.0) * (b.ka[0] + 2 * b.ka[1] + 2 * b.ka[2] + b.ka[3])

        # PLOT
        # Calculate validation parameters
        calculate_validation_step(bodies, 3, E0, P0, L0, e, p, l, abs_e, abs_p, abs_l, rel_e, rel_p, rel_l)

        # Add the new positions
        for i, body in enumerate(bodies):
            x[i].append(body.position[0])
            y[i].append(body.position[1])
