"""
Small shared helpers for the paper-readings notebooks.

`natureStylePlots` is copied verbatim from
`UberPhys/src/pyUberPhys/utilities/utilities.py` so this repo does not
depend on the pyUberPhys package. Keep the two in sync if either changes.
"""

from typing import Literal

import matplotlib.pyplot as plt


# ------------------
#
# natureStylePlots
#
# ------------------

def natureStylePlots(
    *,
    fontSizeAdjust : Literal["regular", "small", "large"] = "regular",
) -> None:
    """
    Apply the SciencePlots ``['science', 'nature']`` style globally,
    then layer a few project-specific overrides on top: outward ticks,
    no minor ticks, no top/right ticks. Optionally also shrink the
    default text sizes for paper-figure use.

    Idempotent: safe to call multiple times. Modifies ``plt.rcParams``
    (and the active matplotlib style) for the rest of the Python
    session -- there is no built-in restore. If you need scoping for
    a single plot, wrap that plot in ``plt.style.context(...)``
    instead. Requires the ``scienceplots`` package to be installed so
    the ``'science'`` / ``'nature'`` style names are registered;
    importing ``scienceplots`` is done on demand inside this function.

    Parameters
    ----------
    fontSizeAdjust : {"regular", "small", "large"}, default "regular"
        Whether to override the Nature 7 pt baseline with a different
        font scheme.

        - ``"regular"``: leave font sizes at the Nature defaults
          (everything at 7 pt).
        - ``"small"``: set ``axes.labelsize`` / ``axes.titlesize`` to
          6.5, ``xtick.labelsize`` / ``ytick.labelsize`` to 6, and
          ``legend.fontsize`` to 5.5. Useful when several figures
          need to fit at small print sizes.
        - ``"large"``: set ``axes.labelsize`` / ``axes.titlesize`` to
          14, ``xtick.labelsize`` / ``ytick.labelsize`` to 12, and
          ``legend.fontsize`` to 10. Useful for slides, posters, and
          one-off exploratory figures that need to read at a glance.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If ``fontSizeAdjust`` is not one of ``"regular"``, ``"small"``,
        or ``"large"``.

    Notes
    -----
    The project-specific overrides applied on top of
    ``['science', 'nature']`` are:

    - ``xtick.direction`` / ``ytick.direction`` -> ``"out"`` (the
      science style points ticks inward; we want them outward).
    - ``xtick.minor.visible`` / ``ytick.minor.visible`` -> ``False``
      (the science style turns minor ticks on; we want major only).
    - ``xtick.top`` / ``ytick.right`` -> ``False`` (the science
      style draws ticks on all four sides; we want bottom + left
      only, matching the common `hideTopRightSpines=True` pattern).
    - ``font.sans-serif`` -> ``['Helvetica', 'Arial', 'DejaVu Sans',
      ...]`` -- prefer actual Helvetica / Arial over DejaVu Sans,
      so paper PDFs land with the same font as the rest of the
      manuscript.
    - ``pdf.fonttype`` / ``ps.fonttype`` -> ``42`` -- embed glyphs
      as TrueType rather than matplotlib's default Type 3 so that
      Adobe Illustrator can open / edit the saved PDFs.
    - ``'no-latex'`` is included in the style chain so that
      ``text.usetex`` stays False; matplotlib's own mathtext
      handles ``\\mathbf{}`` etc. With ``text.usetex=True`` (the
      science default), PDFs ship with Nimbus Sans L from TeX
      Live, which macOS / Illustrator do not have installed.
    """
    if fontSizeAdjust not in ("regular", "small", "large"):
        raise ValueError(
            f"natureStylePlots: fontSizeAdjust must be 'regular', "
            f"'small', or 'large'; got {fontSizeAdjust!r}."
        )
    import scienceplots  # noqa: F401  -- registers SciencePlots styles
    # Order matters: 'science' sets text.usetex=True (which makes
    # PDFs ship with Nimbus Sans L from TeX Live -- a free Helvetica-
    # clone that macOS / Illustrator do not have), 'no-latex' undoes
    # that but resets font.family to serif, and 'nature' then puts
    # font.family back to sans-serif and sets the rest of the Nature
    # journal sizes.
    plt.style.use(["science", "no-latex", "nature"])
    plt.rcParams["xtick.direction"]     = "out"
    plt.rcParams["ytick.direction"]     = "out"
    plt.rcParams["xtick.minor.visible"] = False
    plt.rcParams["ytick.minor.visible"] = False
    plt.rcParams["xtick.top"]           = False
    plt.rcParams["ytick.right"]         = False
    # Prefer actual Helvetica / Arial over DejaVu Sans so PDFs land
    # with the font the rest of the manuscript uses.
    plt.rcParams["font.sans-serif"] = [
        "Helvetica", "Arial", "DejaVu Sans", "Lucida Grande",
        "Verdana", "Geneva", "sans-serif",
    ]
    # Embed glyphs as TrueType (Type 42) instead of matplotlib's
    # default Type 3 -- Illustrator handles Type 3 PDFs poorly.
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"]  = 42
    if fontSizeAdjust == "small":
        plt.rcParams["axes.labelsize"]  = 6.5
        plt.rcParams["axes.titlesize"]  = 6.5
        plt.rcParams["xtick.labelsize"] = 6
        plt.rcParams["ytick.labelsize"] = 6
        plt.rcParams["legend.fontsize"] = 5.5
    elif fontSizeAdjust == "large":
        plt.rcParams["axes.labelsize"]  = 14
        plt.rcParams["axes.titlesize"]  = 14
        plt.rcParams["xtick.labelsize"] = 12
        plt.rcParams["ytick.labelsize"] = 12
        plt.rcParams["legend.fontsize"] = 10
