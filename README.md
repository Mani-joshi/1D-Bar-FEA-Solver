# 1D Bar FEA Solver

A from-scratch Finite Element Analysis solver for 1D axial-loaded bars — built to understand the method from first principles, not just call a library.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)

---

## What it does

Given a 1D bar under axial load, this solver:

1. **Assembles the global stiffness matrix** from element stiffness contributions
2. **Applies boundary conditions** — fixed node elimination (row/column reduction)
3. **Solves the system** `[K]{u} = {F}` for nodal displacements
4. **Back-computes reaction forces** using the full stiffness matrix
5. **Visualises** the displacement field as a 2D contour plot

---

## Background: Why FEA from scratch?

Most engineers use ANSYS or Abaqus as a black box. I wanted to understand what's actually happening — element formulation, matrix assembly, constraint handling, and the linear algebra underneath.

This is a direct implementation of the Direct Stiffness Method as taught in:
> Logan, D.L. — *A First Course in the Finite Element Method* (6th ed.)

---

## Theory

For a 1D bar element of length *L*, area *A*, and modulus *E*:

```
Element stiffness matrix:
       AE/L  [ 1  -1 ]
ke =         [-1   1 ]
```

Global assembly: each element stiffness matrix contributes to the corresponding DOF entries in the global `[K]`.

Boundary condition enforcement: the row and column corresponding to the fixed DOF are removed (since displacement = 0 there), reducing the system to a solvable square matrix.

Reaction forces are recovered by multiplying the full `[K]` by the complete displacement vector, including the enforced zero.

---

## Usage

```bash
pip install numpy matplotlib
python 1D_FEA.py
```

**Inputs (interactive prompts):**
```
Length of the bar (m)         → e.g. 1
Total elements in bar         → e.g. 4
Which node is fixed           → e.g. 1
Which node experiences force  → e.g. 5
Force magnitude (N)           → e.g. 5000
```

**Outputs:**
- Nodal displacement vector `{u}` (m)
- Nodal force vector `{F}` including reactions (N)
- Contour plot of displacement field along the bar

---

## Example

```
Bar: 1 m long, 4 elements (5 nodes)
Material: A = 15 m², E = 2 GPa
BC: Node 1 fixed, 5000 N applied at Node 5
```

**Displacement vector (m):**
```
[[ 0.        ]
 [ 4.167e-08 ]
 [ 8.333e-08 ]
 [ 1.250e-07 ]
 [ 1.667e-07 ]]
```

**Force vector (N) — Node 1 reaction = -5000 N ✓**
```
[[-5000.]
 [    0.]
 [    0.]
 [    0.]
 [ 5000.]]
```

---

## Output

The contour plot renders the displacement field across the bar cross-section using `matplotlib.contourf` with a `jet` colormap — useful for visually verifying that displacement increases linearly from the fixed end.

---

## File Structure

```
1D-Bar-FEA-Solver
└── examples/
    └── sample_output.png
├── 1D_FEA.py      # Main solver
├── LICENSE.md
├── README.md
```

---

## Planned Extensions

- [ ] Multi-material bars (piecewise E, A)
- [ ] Distributed axial loads (body forces)
- [ ] 2D truss solver (next step toward full FEM)
- [ ] Streamlit/web interface for interactive parameter input

---

## Broader Context

This project is part of my systematic study of computational mechanics. Parallel work includes:
- 2D heat diffusion FEM solver (Python)
- Structural analysis during my time at L&T-MHI (ASME/IBR pressure vessel compliance)

The goal: deep enough understanding to design and validate aerospace/defence structures without the black box.

---
