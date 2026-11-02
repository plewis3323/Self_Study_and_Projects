# Statistical Mechanics — Self-Paced Review Syllabus

**Scope:** a graduate-level review that runs from thermodynamics through ensembles, quantum gases, interacting systems and phase transitions, ending with fluctuations and nonequilibrium.
**Length:** 13 weeks (about 3 months).
**Pace:** 3–4 core chapters per week.
**Weekly rhythm:**
1. Read the core chapters.
2. Write notes in `../Notes/Week_XX.md`.
3. Work the AI-generated practice set in `../Exercises/Week_XX/`.
4. Use the cross-references when a topic needs a second explanation.

---

## Reading list (all in OneDrive `3_Textbooks/Statistical_Mechanics/`)

| Code | Book | Role |
|---|---|---|
| **Pathria** | Pathria & Beale, *Statistical Mechanics*, 3rd ed. | Core spine (Ch. 1–16) |
| **Callen** | Callen, *Thermodynamics and an Introduction to Thermostatistics*, 2nd ed. (`Textbooks/`) | Core: thermodynamics, phase transitions, fluctuations |
| **Kardar** | Kardar, *Statistical Physics of Particles* (`Textbooks/…djvu`) | Core: probability, kinetic theory, quantum gases |
| **Schroeder** | Schroeder, *An Introduction to Thermal Physics* | Core and cross-reference: intuition and worked examples |
| **Chandler** | Chandler, *Introduction to Modern Statistical Mechanics* (`Textbooks/imsm_chandler.pdf`) | Core and cross-reference: phase transitions, Monte Carlo, fluids |
| **IGC** | *Statistical Mechanics: An Introductory Graduate Course* (Springer, 2019) (`Textbooks/statistical-mechanics-an-introductory-graduate-course-….pdf`) | Core and cross-reference: mean-field theory, Ising, RG |
| **Reichl** | Reichl, *A Modern Course in Statistical Physics*, 2nd ed. (`Textbooks/`) | Cross-reference: stochastic processes, transport |
| **Kubo** | Kubo, *Statistical Mechanics* (`Textbooks/`) | Cross-reference: worked problems |
| **L&L 5** | Landau & Lifshitz, *Statistical Physics* (Part 1) (`Textbooks/`) | Optional deep dive |
| **L&L 9 / 10** | Landau & Lifshitz, *Statistical Physics Part 2* and *Physical Kinetics* | Optional deep dive |
| **Engineers** | *Statistical Mechanics for Engineers* (Springer, 2015) (`Textbooks/2015_Book_…`) | Cross-reference: applied examples |
| **L&B** | Lancaster & Blundell, *QFT for the Gifted Amateur* (`Nuclear_and_Particle_Physics_Books/Nuc_2/`) | Field-theory link: statistical field theory, RG |
| **P&S** | Peskin & Schroeder, *An Introduction to Quantum Field Theory* (`Quantum_Textbooks/`) | Field-theory link: critical exponents, RG |
| **Schwartz** | Schwartz, *QFT and the Standard Model* (`Nuclear_and_Particle_Physics_Books/`) | Field-theory link: RG |

> Note: the solutions manuals in `Textbooks/` (Schroeder, Chandler, Reichl, Pathria) are there to check your own work after an attempt. Don't treat them as reading.

---

## Part A — Thermodynamics (Weeks 1–3)

### Week 1 — Postulates & equilibrium
- **Core:**
  - Callen Ch. 1 (The Problem and the Postulates)
  - Callen Ch. 2 (Conditions of Equilibrium)
  - Callen Ch. 3 (Formal Relationships and Sample Systems)
- **Cross-ref:**
  - Schroeder Ch. 1–2
  - Kardar Ch. 1
  - Chandler Ch. 1
- **Goals:**
  - Fundamental relations, entropy maximum, intensive vs. extensive variables.
  - Euler and Gibbs–Duhem relations.
  - Ideal gas and simple systems.

### Week 2 — Potentials, Maxwell relations & stability
- **Core:**
  - Callen Ch. 5 (Legendre Transformations)
  - Callen Ch. 6 (Extremum Principle in Transformed Representations)
  - Callen Ch. 7 (Maxwell Relations)
  - Callen Ch. 8 (Stability of Thermodynamic Systems)
- **Cross-ref:**
  - Callen Ch. 4
  - Schroeder Ch. 4–5
  - Chandler Ch. 2
- **Goals:**
  - The potentials U, F, H and G.
  - Maxwell relations and Jacobian tricks.
  - Response functions; stability conditions.

### Week 3 — Probability & kinetic theory
- **Core:**
  - Kardar Ch. 2 (Probability)
  - Kardar Ch. 3 (Kinetic Theory of Gases)
  - Schroeder Ch. 3 (Interactions and Implications)
- **Cross-ref:**
  - Reichl Ch. 4–5 (probability, stochastic dynamics)
  - L&L 10 (kinetics, optional)
- **Goals:**
  - Central limit theorem and large-N.
  - Liouville and the BBGKY hierarchy.
  - Boltzmann equation; H-theorem.

## Part B — Ensembles (Weeks 4–6)

### Week 4 — Statistical basis & the microcanonical ensemble
- **Core:**
  - Pathria Ch. 1 (Statistical Basis of Thermodynamics)
  - Pathria Ch. 2 (Elements of Ensemble Theory)
  - Kardar Ch. 4 (Classical Statistical Mechanics)
  - Callen Ch. 15 (Microcanonical Formalism)
- **Cross-ref:**
  - Schroeder Ch. 2–3
  - Chandler Ch. 3
- **Goals:**
  - Counting microstates Ω(N,V,E).
  - Gibbs paradox.
  - Phase space and Liouville's theorem.

### Week 5 — Canonical ensemble
- **Core:**
  - Pathria Ch. 3 (The Canonical Ensemble)
  - Schroeder Ch. 6 (Boltzmann Statistics)
  - Callen Ch. 16 (Canonical Formalism)
- **Cross-ref:**
  - Chandler Ch. 3
  - Kubo (canonical problems)
- **Goals:**
  - The partition function.
  - Equipartition and the virial theorem.
  - Harmonic oscillators and paramagnetism; negative temperature.

### Week 6 — Grand canonical ensemble & fluctuations
- **Core:**
  - Pathria Ch. 4 (The Grand Canonical Ensemble)
  - Callen Ch. 17 (Generalized Canonical Formulations)
  - Callen Ch. 19 (Fluctuations)
- **Cross-ref:**
  - Kardar Ch. 4 (remaining sections)
  - Chandler Ch. 3
  - Reichl Ch. 7
- **Goals:**
  - Fugacity and the grand potential.
  - Density and energy fluctuations.
  - Ensemble equivalence.

## Part C — Quantum Statistics (Weeks 7–9)

### Week 7 — Formulation of quantum statistics & simple gases
- **Core:**
  - Pathria Ch. 5 (Formulation of Quantum Statistics)
  - Pathria Ch. 6 (Theory of Simple Gases)
  - Kardar Ch. 6 (Quantum Statistical Mechanics)
- **Cross-ref:**
  - Schroeder Ch. 7.1–7.2
  - Chandler Ch. 4
- **Goals:**
  - The density matrix.
  - Bose–Einstein and Fermi–Dirac distributions.
  - Internal degrees of freedom of molecules.

### Week 8 — Ideal Bose systems
- **Core:**
  - Pathria Ch. 7 (Ideal Bose Systems)
  - Kardar Ch. 7 (Ideal Quantum Gases)
  - Callen Ch. 18 (Quantum Fluids)
- **Cross-ref:**
  - Schroeder Ch. 7.4–7.6
  - `Textbooks/Ideal_Bose_Pathria.pdf`
  - IGC Ch. 11
- **Goals:**
  - Blackbody radiation; phonons and the Debye model.
  - Bose–Einstein condensation.
  - Liquid ⁴He.

### Week 9 — Ideal Fermi systems & the early universe
- **Core:**
  - Pathria Ch. 8 (Ideal Fermi Systems)
  - Pathria Ch. 9 (Thermodynamics of the Early Universe)
  - Schroeder Ch. 7.3 (Degenerate Fermi Gases)
- **Cross-ref:**
  - Chandler Ch. 4
  - IGC Ch. 7
- **Goals:**
  - Fermi energy and Sommerfeld expansion.
  - Pauli paramagnetism and Landau diamagnetism.
  - White dwarfs.
  - Relativistic gases, the cosmic background and nucleosynthesis. This links to the nuclear/particle course and QGP thermodynamics.

## Part D — Interacting Systems & Phase Transitions (Weeks 10–12)

### Week 10 — Interacting systems
- **Core:**
  - Pathria Ch. 10 (Cluster Expansions)
  - Pathria Ch. 11 (Method of Quantized Fields)
  - Kardar Ch. 5 (Interacting Particles)
  - Chandler Ch. 7 (Classical Fluids)
- **Cross-ref:**
  - Schroeder Ch. 8
  - Reichl Ch. 9
- **Field-theory link (optional):**
  - L&B Ch. 3–4 (Occupation numbers and second quantization), Ch. 43 (The many-body problem and the metal)
- **Goals:**
  - Virial expansion and the van der Waals gas.
  - Pair correlation g(r).
  - Second quantization for gases.

### Week 11 — Phase transitions & mean-field theory
- **Core:**
  - Pathria Ch. 12 (Criticality, Universality, Scaling)
  - Callen Ch. 9 (First-Order Phase Transitions)
  - Callen Ch. 10 (Critical Phenomena)
  - Chandler Ch. 5 (Statistical Theory of Phase Transitions)
- **Cross-ref:**
  - IGC Ch. 8–10
  - Callen Ch. 20
  - Schroeder Ch. 5.3, 8.2
- **Field-theory link (optional):**
  - L&B Ch. 21 (Statistical physics crash course), Ch. 25 (Statistical field theory), Ch. 26 (Broken symmetry)
  - P&S Ch. 8 (Ultraviolet cutoffs and critical fluctuations)
- **Goals:**
  - The Clausius–Clapeyron relation.
  - Order parameters and Landau theory.
  - Critical exponents, scaling and universality.

### Week 12 — Exact results & the renormalization group
- **Core:**
  - Pathria Ch. 13 (Exact Results for Various Models)
  - Pathria Ch. 14 (Renormalization Group Approach)
  - IGC Ch. 17 (Ising Model: Exact Solutions)
  - IGC Ch. 19 (Real-Space Renormalization Group)
- **Cross-ref:**
  - IGC Ch. 20–21
  - L&L 5
- **Field-theory link (optional):**
  - P&S Ch. 12–13 (Renormalization group; Critical exponents and scalar field theory)
  - L&B Ch. 34–35 (RG; ferromagnetism RG tutorial)
  - Schwartz Ch. 23
- **Goals:**
  - 1D and 2D Ising models; transfer matrices.
  - Block-spin RG; fixed points.
  - Relevant and irrelevant operators.

## Part E — Fluctuations, Nonequilibrium & Simulation (Week 13)

### Week 13 — Fluctuations, nonequilibrium & computer simulation
- **Core:**
  - Pathria Ch. 15 (Fluctuations and Nonequilibrium Statistical Mechanics)
  - Pathria Ch. 16 (Computer Simulations)
  - Chandler Ch. 6 (Monte Carlo Method)
  - Chandler Ch. 8 (Non-Equilibrium Systems)
- **Cross-ref:**
  - IGC Ch. 18 (Monte Carlo)
  - Reichl Ch. 11 (Transport Theory)
  - Callen Ch. 14
  - L&L 10
- **Field-theory link (optional):**
  - L&B Ch. 22–24 (Generating functional and path/field integrals: partition function ↔ path integral)
  - L&B Ch. 42, 44 (Superfluids, superconductors)
- **Goals:**
  - Brownian motion; Langevin and Fokker–Planck equations.
  - The fluctuation–dissipation theorem.
  - Linear response.
  - Metropolis Monte Carlo and molecular dynamics.

---

## Progress tracker

| Week | Topic | Read | Notes | Exercises |
|---|---|:-:|:-:|:-:|
| 1 | Postulates & equilibrium | ☐ | ☐ | ☐ |
| 2 | Potentials, Maxwell relations, stability | ☐ | ☐ | ☐ |
| 3 | Probability & kinetic theory | ☐ | ☐ | ☐ |
| 4 | Microcanonical ensemble | ☐ | ☐ | ☐ |
| 5 | Canonical ensemble | ☐ | ☐ | ☐ |
| 6 | Grand canonical & fluctuations | ☐ | ☐ | ☐ |
| 7 | Quantum statistics & simple gases | ☐ | ☐ | ☐ |
| 8 | Ideal Bose systems | ☐ | ☐ | ☐ |
| 9 | Ideal Fermi systems & early universe | ☐ | ☐ | ☐ |
| 10 | Interacting systems | ☐ | ☐ | ☐ |
| 11 | Phase transitions & mean field | ☐ | ☐ | ☐ |
| 12 | Exact results & RG | ☐ | ☐ | ☐ |
| 13 | Fluctuations, nonequilibrium, simulation | ☐ | ☐ | ☐ |
