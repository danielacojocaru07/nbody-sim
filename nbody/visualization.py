import matplotlib.pyplot as plt

METHODS = {
    0: "Kepler 2-Body",
    1: "Semi-Implicit Euler",
    2: "Velocity Verlet",
    3: "Runge-Kutta 4"
}


def plot_trajectories(bodies, x, y, option, save_path=None):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    all_x = [val for body_x in x for val in body_x]
    all_y = [val for body_y in y for val in body_y]

    margin = max(all_x) * 0.2

    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

    for i in range(len(bodies)):
        ax.plot(x[i], y[i], label=f'Body {i + 1}')
        ax.scatter(x[i][-1], y[i][-1], s=50, zorder=5)

    ax.legend()
    ax.set_title(f"N-Body System ({METHODS.get(option)})")
    ax.set_xlabel("x, AU")
    ax.set_ylabel("y, AU")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.show()


def plot_conserved_quantities(total_energy, total_linear, total_angular, option, dt):
    time_axis = [i * dt for i in range(len(total_energy))]

    fig, axes = plt.subplots(1, 3, figsize=(16, 4))

    axes[0].plot(time_axis, total_energy, color='red')
    axes[0].set_title(f"Total Energy ({METHODS.get(option)})")
    axes[0].set_ylabel(r"energy, $\text{M}_\text{U} \cdot \text{AU}^2 \cdot \text{T}_\text{U}^{-2}$")
    axes[0].set_xlabel("time, TU")
    axes[0].grid(True)

    axes[1].plot(time_axis, total_linear, color='blue')
    axes[1].set_title(f"Total Linear Momentum ({METHODS.get(option)})")
    axes[1].set_ylabel(r"linear momentum, $\text{M}_\text{U} \cdot \text{AU} \cdot \text{T}_\text{U}^{-1}$")
    axes[1].set_xlabel("time, TU")
    axes[1].grid(True)

    axes[2].plot(time_axis, total_angular, color='green')
    axes[2].set_title(f"Total Angular Momentum ({METHODS.get(option)})")
    axes[2].set_ylabel(r"angular momentum, $\text{M}_\text{U} \cdot \text{AU}^2 \cdot \text{T}_\text{U}^{-1}$")
    axes[2].set_xlabel("time, TU")
    axes[2].grid(True)

    plt.tight_layout()
    plt.show()


def plot_errors(abs_energy, abs_linear, abs_angular,
                rel_energy, rel_linear, rel_angular, option, dt):
    time_axis = [i * dt for i in range(len(abs_energy))]

    fig, axes = plt.subplots(2, 3, figsize=(16, 8))

    axes[0, 0].plot(time_axis, abs_energy, color='red')
    axes[0, 0].set_title(f"Absolute Energy Error ({METHODS.get(option)})")
    axes[0, 0].set_ylabel(r"absolute error, $\text{M}_\text{U} \cdot \text{AU}^2 \cdot \text{T}_\text{U}^{-2}$")
    axes[0, 0].set_xlabel("time, TU")
    axes[0, 0].grid(True)

    axes[0, 1].plot(time_axis, abs_linear, color='blue')
    axes[0, 1].set_title(f"Absolute Linear Momentum Error ({METHODS.get(option)})")
    axes[0, 1].set_ylabel(r"absolute error, $\text{M}_\text{U} \cdot \text{AU} \cdot \text{T}_\text{U}^{-1}$")
    axes[0, 1].set_xlabel("time, TU")
    axes[0, 1].grid(True)

    axes[0, 2].plot(time_axis, abs_angular, color='green')
    axes[0, 2].set_title(f"Absolute Angular Momentum Error ({METHODS.get(option)})")
    axes[0, 2].set_ylabel(r"absolute error, $\text{M}_\text{U} \cdot \text{AU}^2 \cdot \text{T}_\text{U}^{-1}$")
    axes[0, 2].set_xlabel("time, TU")
    axes[0, 2].grid(True)

    axes[1, 0].plot(time_axis, rel_energy, color='red')
    axes[1, 0].set_title(f"Relative Energy Error ({METHODS.get(option)})")
    axes[1, 0].set_ylabel("relative error, %")
    axes[1, 0].set_xlabel("time, TU")
    axes[1, 0].grid(True)

    axes[1, 1].plot(time_axis, rel_linear, color='blue')
    axes[1, 1].set_title(f"Relative Linear Momentum Error ({METHODS.get(option)})")
    axes[1, 1].set_ylabel("relative error, %")
    axes[1, 1].set_xlabel("time, TU")
    axes[1, 1].grid(True)

    axes[1, 2].plot(time_axis, rel_angular, color='green')
    axes[1, 2].set_title(f"Relative Angular Momentum Error ({METHODS.get(option)})")
    axes[1, 2].set_ylabel("relative error, %")
    axes[1, 2].set_xlabel("time, TU")
    axes[1, 2].grid(True)

    plt.tight_layout()
    plt.show()
