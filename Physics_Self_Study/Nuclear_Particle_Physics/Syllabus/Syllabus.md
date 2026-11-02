# Nuclear & Particle Physics — Self-Paced Review Syllabus

**Scope:** a combined review of graduate Nuclear Physics I (nuclear structure, decay, reactions) and Nuclear Physics II (particle physics and the Standard Model). It covers both the **theory** and the **experimental** side: detectors, accelerators, statistics and heavy-ion physics.
**Length:** 13 weeks (about 3 months).
**Pace:** 3–4 core chapters per week. From Week 8 on, each week also has a short L&B block (chapters are ~10 pages; the block counts as about one chapter).
**Weekly rhythm:**
1. Read the core chapters.
2. Write notes in `../Notes/Week_XX.md`.
3. Work the AI-generated practice set in `../Exercises/Week_XX/`.
4. Use the cross-references when a topic needs a second explanation.
5. **QFT track (optional):** deeper field-theory reading (Schwartz, P&S, extra L&B chapters). It doesn't count toward the weekly core.

---

## Reading list (all in OneDrive `3_Textbooks/Nuclear_and_Particle_Physics_Books/`)

| Code | Book | Role |
|---|---|---|
| **Krane** | Krane, *Introductory Nuclear Physics* (`Nuclear_1/Textbooks/Introductory Nuclear Physics.pdf`) | Core: nuclear structure, decay and reactions |
| **Thomson** | Thomson, *Modern Particle Physics* (`Nuc_2/ModernParticlePhysics _Thomson.pdf`) | Core: particle theory and phenomenology |
| **Griffiths** | Griffiths, *Introduction to Elementary Particles*, 2nd ed. (`Nuc_2/introduction-to-elementary-particles-gnv64.pdf`) | Core: kinematics, symmetries, Feynman calculus |
| **Mann** | Mann, *An Introduction to Particle Physics and the Standard Model* (`Nuc_2/An Introduction to Particle Physics and the Standard Model_….pdf`) | Core: symmetries, accelerators, detectors, SM tests |
| **Povh** | Povh et al., *Particles and Nuclei* (`Nuclear_1/Textbooks/particles_nuclei.pdf`) | Core and cross-reference: links nuclear and particle topics |
| **Knoll** | Knoll, *Radiation Detection and Measurement*, 3rd ed. | Core: experimental methods |
| **PRL-Det** | *Particle Physics Reference Library Vol. 2: Detectors for Particles and Radiation* (`Nuclear_1/978-3-030-35318-6.pdf`) | Core and cross-reference: calorimetry, statistics, reconstruction |
| **PRL-Th** | *Particle Physics Reference Library Vol. 1: Theory and Experiments* (`Nuclear_1/978-3-030-38207-0.pdf`) | Cross-reference: SM, QCD, heavy-ion phase diagram |
| **Bartke** | Bartke, *Introduction to Relativistic Heavy Ion Physics* | Core (Week 13): QGP and heavy-ion observables |
| **Martin** | B. R. Martin, *Nuclear and Particle Physics: An Introduction* (`Nuc_2/`) | Cross-reference: concise overview of both subjects |
| **Wong** | Wong, *Introductory Nuclear Physics* (`Nuclear_1/Textbooks/`) | Cross-reference: nuclear theory |
| **H&M** | Halzen & Martin, *Quarks and Leptons* (`Nuc_2/`) | Cross-reference: QED, partons, QCD, electroweak |
| **Leo** | Leo, *Techniques for Nuclear and Particle Physics Experiments* | Cross-reference: detectors, electronics, statistics |
| **Wilson** | Wilson, *An Introduction to Particle Accelerators* (`9780198520542.pdf`) | Cross-reference: accelerators |
| **James** | James, *Statistical Methods in Experimental Physics* | Cross-reference: statistics and fitting |
| **Loveland** | Loveland, Morrissey & Seaborg, *Modern Nuclear Chemistry*, 2nd ed. | Cross-reference: decay and reactions |
| **R&S** | Ring & Schuck, *The Nuclear Many-Body Problem* (`NuclearTextBook.pdf`) | Optional deep dive: nuclear theory |
| **P&S** | Peskin & Schroeder, *An Introduction to Quantum Field Theory* (`Quantum_Textbooks/`; also a copy in `Nuc_2/`) | QFT track: standard graduate QFT |
| **Schwartz** | Schwartz, *Quantum Field Theory and the Standard Model* | QFT track: modern, Standard-Model-focused QFT |
| **L&B** | Lancaster & Blundell, *Quantum Field Theory for the Gifted Amateur* (`Nuc_2/QFT_Intro_GAmature.pdf`) | QFT track: gentle entry point; links to stat mech |
| **L&L 4** | Berestetskii, Lifshitz & Pitaevskii, *Quantum Electrodynamics* (Landau Vol. 4) (`Quantum_Textbooks/Textbooks/`) | Optional deep dive: QED |

> Note: the Krane PDF in the library is missing Ch. 6–7 and 15–18. The chapters listed below are all ones that are present.

---

## Part A — Nuclear Physics (Weeks 1–5)

### Week 1 — Foundations & relativistic kinematics
- **Core:**
  - Krane Ch. 1 (Basic Concepts)
  - Griffiths Ch. 1 (Historical Introduction)
  - Griffiths Ch. 3 (Relativistic Kinematics)
  - Thomson Ch. 1 (Introduction)
- **Cross-ref:**
  - Krane Ch. 2 (QM review, skim)
  - Mann Ch. 1–2
  - Martin Ch. 1
  - Povh Ch. 1
- **QFT track (optional):**
  - L&B Ch. 0–2 (Overture, Lagrangians, harmonic oscillators)
  - Schwartz Ch. 2 (Lorentz invariance and second quantization)
- **Goals:**
  - Units and natural units.
  - Four-vectors, invariant mass, thresholds, rapidity.
  - The particle zoo and the four interactions.

### Week 2 — Nuclear properties & the nucleon–nucleon force
- **Core:**
  - Krane Ch. 3 (Nuclear Properties)
  - Krane Ch. 4 (Force Between Nucleons)
  - Povh Ch. 2 (Global Properties of Nuclei)
  - Povh Ch. 3 (Nuclear Stability)
- **Cross-ref:**
  - Povh Ch. 4–5 (Scattering, Geometric Shapes)
  - Wong Ch. 3–4
  - Martin Ch. 2
- **Goals:**
  - Nuclear radius and form factors.
  - Semi-empirical mass formula and binding energy.
  - Moments.
  - The deuteron, NN scattering, and the exchange-force model.

### Week 3 — Nuclear models
- **Core:**
  - Krane Ch. 5 (Nuclear Models)
  - Povh Ch. 17 (The Nuclear Force)
  - Povh Ch. 18 (Structure of Nuclei)
  - Povh Ch. 19 (Collective Nuclear Excitations)
- **Cross-ref:**
  - Wong Ch. 6–7
  - Martin Ch. 7
  - R&S (optional: mean-field and shell model)
- **Goals:**
  - Shell model and magic numbers.
  - Spin–orbit coupling.
  - Collective rotations and vibrations; deformation; giant resonances.

### Week 4 — Radioactive decay
- **Core:**
  - Krane Ch. 8 (Alpha Decay)
  - Krane Ch. 9 (Beta Decay)
  - Krane Ch. 10 (Gamma Decay)
- **Cross-ref:**
  - Wong Ch. 5
  - Loveland (decay chapters)
  - Povh Ch. 10 (weak phenomenology preview)
- **Goals:**
  - Gamow tunneling and Fermi theory.
  - Selection rules; parity violation (Wu experiment).
  - Multipole radiation, internal conversion, B(E2).

### Week 5 — Nuclear reactions, neutrons, fission & fusion
- **Core:**
  - Krane Ch. 11 (Nuclear Reactions)
  - Krane Ch. 12 (Neutron Physics)
  - Krane Ch. 13 (Fission)
  - Krane Ch. 14 (Fusion)
- **Cross-ref:**
  - Krane Ch. 19 (Nuclear Astrophysics)
  - Wong Ch. 8–10
  - Martin Ch. 8
- **Goals:**
  - Q-values and cross sections.
  - Compound-nucleus and direct reactions; Coulomb excitation.
  - Neutron moderation.
  - Fission and fusion energetics.

## Part B — Experimental Methods (Weeks 6–7)

### Week 6 — Radiation–matter interactions & detector fundamentals
- **Core:**
  - Knoll Ch. 2 (Radiation Interactions)
  - Knoll Ch. 3 (Counting Statistics and Error Prediction)
  - Knoll Ch. 4 (General Properties of Radiation Detectors)
  - PRL-Det Ch. 6 (Calorimetry)
- **Cross-ref:**
  - Leo Ch. 2, 4, 5
  - PRL-Det Ch. 2
  - Mann Ch. 8 (Detectors)
  - Povh App. A.2
- **Goals:**
  - Bethe–Bloch energy loss.
  - Photon interactions; radiation length; EM and hadronic showers.
  - Energy resolution.
  - Poisson and Gaussian statistics.

### Week 7 — Detector technologies, accelerators & data analysis
- **Core:**
  - Knoll Ch. 10 (Spectroscopy with Scintillators)
  - Knoll Ch. 12 (Germanium Gamma-Ray Detectors)
  - Mann Ch. 7 (Accelerators)
  - PRL-Det Ch. 15 (Statistical Issues in Particle Physics)
- **Cross-ref:**
  - PRL-Det Ch. 3, 5, 13
  - Wilson (accelerator basics)
  - James (fitting and confidence intervals)
  - Leo Ch. 7–10
- **Goals:**
  - Scintillators, PMTs/SiPMs, HPGe spectroscopy.
  - Tracking and reconstruction.
  - Synchrotrons and luminosity.
  - Likelihood fits and limits.

## Part C — Particle Physics & the Standard Model (Weeks 8–13)

### Week 8 — Symmetries, conservation laws & the quark model
- **Core:**
  - Griffiths Ch. 4 (Symmetries)
  - Mann Ch. 5 (Particle Classification)
  - Mann Ch. 6 (Discrete Symmetries)
  - L&B Ch. 6–7 (First stab at relativistic QM; Examples of Lagrangians — assigned in Nuc II), Ch. 10 (Symmetry)
- **Cross-ref:**
  - Mann Ch. 3–4
  - Thomson Ch. 9
  - H&M Ch. 2
  - Griffiths Ch. 5
  - Povh Ch. 15–16
- **QFT track (optional):**
  - L&B Ch. 15 (Discrete transformations)
  - Schwartz Ch. 3 (Classical field theory: Noether), Ch. 11 (Spinor solutions and CPT)
- **Goals:**
  - SU(2) isospin and SU(3) flavor.
  - Meson and baryon multiplets.
  - C, P, T and CPT.

### Week 9 — Dirac equation, Feynman calculus & QED
- **Core:**
  - Thomson Ch. 4 (The Dirac Equation)
  - Griffiths Ch. 6 (Feynman Calculus)
  - Griffiths Ch. 7 (QED)
  - L&B Ch. 11–12 (Canonical quantization of fields; Examples — assigned in Nuc II)
- **Cross-ref:**
  - Thomson Ch. 3, 5
  - Mann Ch. 10–14
  - H&M Ch. 3–7
- **QFT track (optional):**
  - P&S Ch. 2–5 (Klein–Gordon field → elementary QED processes)
  - Schwartz Ch. 5–7, 10, 13
  - L&B Ch. 36–41 (Dirac field → renormalization of QED)
  - Running α: Schwartz Ch. 16–17 (vacuum polarization, g−2)
- **Goals:**
  - Fermi's golden rule and phase space.
  - Spinors and γ-matrices; Feynman rules and trace techniques.
  - Running α.

### Week 10 — e⁺e⁻ annihilation, elastic & deep inelastic scattering
- **Core:**
  - Thomson Ch. 6 (e⁺e⁻ Annihilation)
  - Thomson Ch. 7 (Electron–Proton Elastic Scattering)
  - Thomson Ch. 8 (Deep Inelastic Scattering)
  - L&B Ch. 16–19 (Propagators and Green's functions → S-matrix → Feynman diagrams)
- **Cross-ref:**
  - Povh Ch. 6, 7, 9
  - H&M Ch. 8–9
  - Mann Ch. 15, 17
- **QFT track (optional):**
  - P&S Ch. 5.1 (e⁺e⁻ → μ⁺μ⁻), Ch. 14 (Invitation: parton model)
  - Schwartz Ch. 32 (QCD and the parton model)
- **Goals:**
  - Helicity structure and form factors (Rosenbluth).
  - Bjorken scaling and parton distribution functions.
  - The R ratio.

### Week 11 — QCD, quarkonia & hadronization
- **Core:**
  - Thomson Ch. 10 (QCD)
  - Griffiths Ch. 8 (Electrodynamics and Chromodynamics of Quarks)
  - Mann Ch. 18 (Heavy Quarks and QCD)
  - L&B Ch. 46 (Non-abelian gauge theory)
- **Cross-ref:**
  - Povh Ch. 8, 14 (Quarkonia)
  - H&M Ch. 10–11
  - PRL-Th Ch. 4–5 (QCD and lattice QCD)
- **QFT track (optional):**
  - P&S Ch. 15–17 (non-Abelian gauge theory → QCD)
  - Schwartz Ch. 25–26 (Yang–Mills), Ch. 36 (jets)
  - Running α_s: P&S Ch. 12, Schwartz Ch. 23 (renormalization group)
- **Goals:**
  - Color and asymptotic freedom.
  - Running α_s.
  - Jets, fragmentation and DGLAP.
  - Charmonium and bottomonium.

### Week 12 — Weak interactions, neutrinos & CP violation
- **Core:**
  - Thomson Ch. 11 (The Weak Interaction)
  - Thomson Ch. 12 (Weak Interactions of Leptons)
  - Thomson Ch. 13 (Neutrinos and Oscillations)
  - Thomson Ch. 14 (CP Violation)
- **Cross-ref:**
  - Griffiths Ch. 9, 11
  - Povh Ch. 10–11
  - Mann Ch. 19–21
  - H&M Ch. 12
- **QFT track (optional):**
  - Schwartz Ch. 29 (Weak interactions), Ch. 30 (Anomalies, optional)
  - P&S Ch. 19 (anomalies, optional)
- **Goals:**
  - V–A structure.
  - Muon and pion decay.
  - The CKM and PMNS matrices.
  - Neutrino oscillation phenomenology.
  - The kaon system.

### Week 13 — Electroweak unification, Higgs & the QCD phase diagram (heavy ions)
- **Core:**
  - Thomson Ch. 15 (Electroweak Unification)
  - Thomson Ch. 17 (The Higgs Boson)
  - Bartke Ch. 2 (QCD and the Phase Transition)
  - Bartke Ch. 15–20, selected: flow, charmonium suppression, direct photons, high-p_T, jets
  - L&B Ch. 47 (Weinberg–Salam model)
- **Cross-ref:**
  - Thomson Ch. 16, 18
  - Griffiths Ch. 10
  - Mann Ch. 22–25
  - H&M Ch. 13–15
  - PRL-Th Ch. 6–7
  - Povh Ch. 20–21
- **QFT track (optional):**
  - P&S Ch. 20–21 (spontaneously broken gauge theories)
  - Schwartz Ch. 28 (SSB), Ch. 31 (Precision tests of the SM)
  - L&B Ch. 26 (Broken symmetry)
- **Goals:**
  - SU(2)×U(1) and the Higgs mechanism; W/Z masses.
  - Higgs discovery.
  - QGP signatures: jet quenching, R_AA, elliptic flow, π⁰ / direct-photon measurements (the sPHENIX connection).

---

## Progress tracker

| Week | Topic | Read | Notes | Exercises |
|---|---|:-:|:-:|:-:|
| 1 | Foundations & kinematics | ☐ | ☐ | ☐ |
| 2 | Nuclear properties & NN force | ☐ | ☐ | ☐ |
| 3 | Nuclear models | ☐ | ☐ | ☐ |
| 4 | Radioactive decay | ☐ | ☐ | ☐ |
| 5 | Reactions, neutrons, fission/fusion | ☐ | ☐ | ☐ |
| 6 | Radiation–matter & detectors | ☐ | ☐ | ☐ |
| 7 | Detector tech, accelerators, statistics | ☐ | ☐ | ☐ |
| 8 | Symmetries & quark model | ☐ | ☐ | ☐ |
| 9 | Dirac, Feynman calculus, QED | ☐ | ☐ | ☐ |
| 10 | e⁺e⁻, elastic & DIS | ☐ | ☐ | ☐ |
| 11 | QCD & quarkonia | ☐ | ☐ | ☐ |
| 12 | Weak interactions & neutrinos | ☐ | ☐ | ☐ |
| 13 | Electroweak, Higgs, heavy ions | ☐ | ☐ | ☐ |
