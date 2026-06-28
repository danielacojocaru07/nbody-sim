# nbody-sim

A modular, object-oriented gravitational N-body simulator written in Python.
Supports 2-10 interacting bodies and four integration schemes: the analytical
Kepler solution (2-body only), Semi-Implicit Euler, Velocity Verlet, and
Runge-Kutta 4. Each simulation tracks the conservation of total energy,
linear momentum, and angular momentum over time.

> **Associated thesis:** *Neural Network-Based Prediction of N-Body System Evolution*
> Daniela Cojocaru — West University of Timișoara, Faculty of Computer Science, 2026
> Supervisor: Prof. Dr. Daniela Zaharie

---

## Features

- Four integration methods: Kepler (analytical), Semi-Implicit Euler, Velocity Verlet, RK4
- Supports 2 to 10 bodies with randomized initial conditions
- Automatic conservation of the center-of-mass momentum (zero net momentum)
- Softening parameter to prevent singularities at close encounters
- Tracks and plots total energy, linear momentum, and angular momentum
- Absolute and relative error plots for each conserved quantity
- Trajectory visualization for all bodies

---

## Project Structure

```
nbody-sim/
│
├── nbody/                  # Core package
│   ├── __init__.py
│   ├── constants.py        # Physical constants and simulation parameters
│   ├── bodies.py           # Body class hierarchy and body generation
│   ├── integrators.py      # Simulation loop for each integration method
│   ├── validation.py       # Energy, momentum, and error tracking
│   └── visualization.py    # Trajectory and conservation plots
│
├── notebooks/
│   └── simulation.ipynb    # Interactive simulation notebook
│
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/danielacojocaru07/nbody-sim.git
cd nbody-sim
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the package in editable mode

```bash
pip install -e .
```

This makes the `nbody` package importable from anywhere in the project,
including from inside the notebook.

---

## Requirements

- Python 3.10+
- numpy
- matplotlib

All dependencies are listed in `requirements.txt` and can be installed with:

```bash
pip install -r requirements.txt
```

---

## Usage

### Running the simulation notebook

Open `notebooks/simulation.ipynb` in JupyterLab, Jupyter Notebook, or
PyCharm and run all cells. You will be prompted to enter:

- **Number of bodies** (integer between 2 and 10)
- **Integration method:**

| Option | Method | Available for |
|--------|------------------------|---------------|
| 0 | Kepler (analytical) | 2 bodies only |
| 1 | Semi-Implicit Euler | 2-10 bodies   |
| 2 | Velocity Verlet | 2-10 bodies   |
| 3 | Runge-Kutta 4 (RK4) | 2-10 bodies   |

The simulation will then generate random initial conditions, run the
integration, and display:

1. **Trajectory plot** -- positions of all bodies over time
2. **Conservation plots** -- total energy, linear momentum, angular momentum
3. **Error plots** -- absolute and relative errors for each conserved quantity

### Using the package directly in a script

```python
from nbody.constants import *
from nbody.bodies import *
from nbody.integrators import *
from nbody.validation import *
from nbody.visualization import *

N = 3
option = 3  # RK4

bodies = generate_bodies(option, N)

x = [[b.position[0]] for b in bodies]
y = [[b.position[1]] for b in bodies]

total_energy, total_linear, total_angular = [], [], []
abs_energy,   abs_linear,   abs_angular   = [], [], []
rel_energy,   rel_linear,   rel_angular   = [], [], []

E0 = energy(bodies, option)
P0 = linear_momentum(bodies)
L0 = angular_momentum(bodies)

runners = {
    0: run_kepler,
    1: run_euler,
    2: run_verlet,
    3: run_rk4
}

runners[option](
    steps, dt, bodies,
    x, y, E0, P0, L0,
    total_energy, total_linear, total_angular,
    abs_energy, abs_linear, abs_angular,
    rel_energy, rel_linear, rel_angular
)

plot_trajectories(bodies, x, y, option)
plot_conserved_quantities(total_energy, total_linear, total_angular, option, dt)
plot_errors(abs_energy, abs_linear, abs_angular,
            rel_energy, rel_linear, rel_angular, option, dt)
```

### Using directly in Google Colaboratory

The simulation can be run directly in Google Colaboratory without any local
installation. The notebook is fully available at the following link:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uaHiCVMMFozr7Ss_AdGuMGh-QME43KVS?usp=sharing)
---

## Physical Units

The simulator uses a normalized unit system:

| Quantity | Unit | Value |
|----------|------|-------|
| Mass | M☉ (solar mass) | 10³⁰ kg |
| Length | AU (astronomical unit) | ≈ 1.5 × 10¹¹ m |
| Time | TU | ≈ 7,082,478 s ≈ 82 days |
| G | — | 1.0 (normalized) |

Setting G = 1 in these units simplifies the equations of motion and avoids
numerical issues from very large or very small constants.

A softening parameter `ε = 0.05 AU` is applied to the gravitational force
to prevent singularities when two bodies pass very close to each other.

---

## Integration Methods

| Method | Order | Energy Conservation | Notes |
|--------|-------|--------------------|------------------------------------|
| Kepler | exact | exact | 2-body only, analytical solution |
| Semi-Implicit Euler | 1st | good (symplectic) | Fast, suitable for long runs |
| Velocity Verlet | 2nd | very good | Time-reversible, widely used |
| RK4 | 4th | excellent | Most accurate, higher cost |

---

## License

This project was developed as part of a Bachelor's thesis at the West University
of Timișoara, Faculty of Computer Science, 2026.

© 2026 Daniela Cojocaru. All rights reserved.
