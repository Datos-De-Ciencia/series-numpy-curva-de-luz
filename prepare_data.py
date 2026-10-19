"""Build the NumPy series dataset from a TESS Target Pixel File.

Star: WASP-18 (TIC 100100827), TESS sector 2, 2-minute cadence (SPOC).
Planet WASP-18 b transits every ~0.94 days with a ~1% dip.

Outputs (in data/):
    flux_cube.npy      float32, shape (T, H, W): pixel brightness, background included
    aperture_mask.npy  bool,    shape (H, W):    pixels that belong to the star
    time.npy           float64, shape (T,):      days since the first frame

All preparation complexity lives here so the videos never need it:
    - unreliable frames (QUALITY != 0) are set to NaN
    - the per-pixel background removed by the pipeline is added back,
      so later videos can subtract a background themselves
    - time is shifted to start at 0 (days)
    - the cube is cropped to 2 days containing two transits
"""

from pathlib import Path

import lightkurve as lk
import numpy as np

TARGET = "WASP-18"
SECTOR = 2
T_START, T_END = 1363.4, 1365.4  # BTJD window: transits at ~1363.87 and ~1364.81

HERE = Path(__file__).parent
RAW_DIR = HERE / "raw"
OUT_DIR = HERE / "data"


def main():
    search = lk.search_targetpixelfile(TARGET, author="SPOC", exptime=120, sector=SECTOR)
    tpf = search.download(download_dir=str(RAW_DIR), quality_bitmask="none")

    time = tpf.time.value
    keep = (time >= T_START) & (time <= T_END)

    flux = tpf.flux.value[keep] + tpf.flux_bkg.value[keep]
    flux = flux.astype(np.float32)
    flux[tpf.quality[keep] != 0] = np.nan

    time = (time[keep] - time[keep][0]).astype(np.float64)
    mask = np.asarray(tpf.pipeline_mask, dtype=bool)

    OUT_DIR.mkdir(exist_ok=True)
    np.save(OUT_DIR / "flux_cube.npy", flux)
    np.save(OUT_DIR / "aperture_mask.npy", mask)
    np.save(OUT_DIR / "time.npy", time)
    print(f"Saved {flux.shape} cube, {mask.sum()} aperture pixels, to {OUT_DIR}")


if __name__ == "__main__":
    main()
