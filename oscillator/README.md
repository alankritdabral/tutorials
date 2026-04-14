---
title: Oscillator
permalink: tutorials-oscillator.html
keywords: Python, ODE, FMI
summary: We solve an oscillator with two masses in a partitioned fashion. Each mass is solved by an independent ODE.
---

{% note %}
Get the [case files of this tutorial](https://github.com/precice/tutorials/tree/develop/oscillator), as continuously rendered here, or see the [latest released version](https://github.com/precice/tutorials/tree/master/oscillator) (if there is already one). Read how in the [tutorials introduction](https://precice.org/tutorials.html).
{% endnote %}

## Setup

This tutorial solves a simple mass-spring oscillator with two masses and three springs. The system is cut at the middle spring and solved in a partitioned fashion:

<img src="images/tutorials-oscillator-schematic-drawing_light.png" class="img-light" alt="Schematic drawing of oscillator example">
<img src="images/tutorials-oscillator-schematic-drawing_dark.png" class="img-dark" style="display:none;" alt="Schematic drawing of oscillator example">

Note that this case applies a Schwarz-type coupling method and not (like most other tutorials in this repository) a Dirichlet-Neumann coupling. This results in a symmetric setup of the solvers. We will refer to the solver computing the trajectory of $m_1$ as `Mass-Left` and to the solver computing the trajectory of $m_2$ as `Mass-Right`. For more information, please refer to [1].

## Configuration

preCICE configuration (image generated using the [precice-config-visualizer](https://precice.org/tooling-config-visualization.html)):

<img src="images/tutorials-oscillator-precice-config_light.png" class="img-light" alt="preCICE configuration visualization">
<img src="images/tutorials-oscillator-precice-config_dark.png" class="img-dark" style="display:none;" alt="preCICE configuration visualization">

## Available solvers

There are two different implementations:

- *Python*: A solver using the preCICE [Python bindings](https://precice.org/installation-bindings-python.html). The run script installs the dependencies automatically via pip in a virtual environment. Using the option `-ts` allows you to pick the time stepping scheme being used. Available choices are Newmark beta, generalized alpha, explicit Runge Kutta 4, and implicit RadauIIA. The solver uses subcycling: Each participant performs 4 time steps in each time window. The data of these 4 substeps is then used by preCICE to create a third order B-spline interpolation (`waveform-degree="3"` in `precice-config.xml`).
- *FMI*: A solver using the [preCICE-FMI runner](https://github.com/precice/fmi-runner) (requires at least v0.2). The Runner executes the FMU model `Oscillator.fmu` for computation. The provided run scripts (see below) build this model if not already there. For more information, please refer to [2].

## Running the simulation

Open two separate terminals and start both participants. For example, you can run a simulation where the left participant is computed in Python and the right participant is computed with FMI with these commands:

```bash
cd mass-left-python
./run.sh
```

and

```bash
cd mass-right-fmi
./run.sh
```

Of course, you can also use the same solver for both sides.

## Post-processing

Each simulation run creates two files containing position and velocity of the two masses over time. These files are called `trajectory-Mass-Left.csv` and `trajectory-Mass-Right.csv`. You can use the script `plot-trajectory.py` for post-processing. Type `python3 plot-trajectory --help` to see available options. You can, for example, plot the trajectory of the left mass of the Python solver by running

```bash
python3 plot-trajectory.py mass-left-python/output/trajectory-Mass-Left.csv TRAJECTORY
```

The solvers allow you to study the effect of different time stepping schemes on energy conservation. Newmark beta conserves energy:

<img src="images/tutorials-oscillator-trajectory-newmark-beta_light.png" class="img-light" alt="Trajectory for Newmark beta scheme">
<img src="images/tutorials-oscillator-trajectory-newmark-beta_dark.png" class="img-dark" style="display:none;" alt="Trajectory for Newmark beta scheme">

Generalized alpha does not conserve energy:

<img src="images/tutorials-oscillator-trajectory-generalized-alpha_light.png" class="img-light" alt="Trajectory for generalized alpha scheme">
<img src="images/tutorials-oscillator-trajectory-generalized-alpha_dark.png" class="img-dark" style="display:none;" alt="Trajectory for generalized alpha scheme">

For details, refer to [1].

## References

[1] V. Schüller, B. Rodenberg, B. Uekermann and H. Bungartz, A Simple Test Case for Convergence Order in Time and Energy Conservation of Black-Box Coupling Schemes, in: WCCM-APCOM2022. [URL](https://www.scipedia.com/public/Rodenberg_2022a)

[2] L. Willeke, D. Schneider and B. Uekermann, A preCICE-FMI Runner to Couple FMUs to PDE-Based Simulations, Proceedings 15th Intern. Modelica Conference, 2023. [DOI](https://doi.org/10.3384/ecp204479)
