# paper-readings

Notes and numerical checks made while reading papers. One notebook per paper.
Working style: propose, agree, then one step / one cell at a time (see `~/.claude/CLAUDE.md`).

## Current paper: Pachitariu & Stringer 2026, "A critical initialization for biological neural networks"

- Notebook: `critical_init.ipynb`. Plan + derivations + open questions: `critical-init-handoff.md`.
- Paper code: https://github.com/mouseland/critical_init. Data: https://doi.org/10.25378/janelia.27854448.

### Environment

- Jupyter kernel: **`bl_datajoint`** conda env (`/opt/anaconda3/envs/bl_datajoint`). It has
  numpy 1.26, scipy 1.13, matplotlib 3.9 and `scienceplots`; base anaconda lacks `scienceplots`.
- `utilities.py` holds `natureStylePlots` (verbatim copy from
  `UberPhys/src/pyUberPhys/utilities/utilities.py`). Keep in sync if either changes.
- Cell 0.1 uses `%matplotlib qt` (figures in Qt windows, reused via `figNum`). For a headless
  check, execute a scratch copy with that line switched to `%matplotlib inline`, run from the repo
  dir so `utilities` imports.

### Notebook conventions

Follow the `analysis-notebook` skill: `# [Cell S.C]` headers with a complete contents list,
function-per-cell with full NumPy docstrings and type annotations, demo call at the bottom driven
by `UPPER_CASE` knobs, every plot function takes `figNum`. Markdown cells describe what/why and
name the knobs but **never state their values** — the user changes them freely.

### Cell map

| Cell | What |
|---|---|
| 0.1 | imports, autoreload, `natureStylePlots(fontSizeAdjust="large")`, `%matplotlib qt` |
| 1.1 | toy edge spectrum `λ_i = 1 − λ₀ i^(2/3)`; 3 log–log panels (cA, −M, Σ) vs rank per c. Knobs `TOY_N`, `TOY_C_VALUES`, `TOY_MAX_RANK` |

### Plan (from the handoff; steps not yet built are tentative)

1. ✅ Toy edge spectrum and the effect of c < 1 (floor at 1−c, knee at i* ~ ((1−c)/λ₀)^(3/2)).
2. Sample a real symmetric A; semicircle histogram; compare sorted top eigenvalues to the toy.
3. Closed-form Σ = ½(I−A)⁻¹ vs `scipy.linalg.solve_continuous_lyapunov`; symmetric vs not.
4. Exponent vs spectral radius: fit ranks 10–500 (paper's window) vs fit above the knee.
5. Universality across entry distributions.
6. Degrees of symmetry vs non-normality.

### Findings so far

- **Step 1 (toy, SOLID as a property of the formula):** at N = 10⁴, λ₀ ≈ 3.0×10⁻³. For
  c = 0.998 the floor (0.002) is *below* λ₀, so the knee is below rank 1 — the paper's
  "critical" setting is effectively fully critical. For c = 0.975 the knee is ≈ rank 25, inside
  the 10–500 fit window; for c = 0.95, ≈ rank 65. This is the mechanism for Fig. 2i.
- The toy is only the semicircle edge law; beyond roughly rank N/10 it is not a valid
  quantile (last value ≈ −0.4, not −1). Don't read the high-rank tails.

### Open questions

- Paper normalizes the *realized* top eigenvalue to 0.998; Tracy–Widom fluctuations of that
  eigenvalue are O(N^(−2/3)), the same scale as λ₀, so "c" in the toy is only approximately
  the paper's "maximum eigenvalue". Check in Step 2.
- Carried over from the handoff: SVCA2 circularity; α jointly sensitive to symmetry and to
  distance from criticality.
