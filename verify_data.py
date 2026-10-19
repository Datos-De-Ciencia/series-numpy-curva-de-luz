"""Check the exported .npy files using only NumPy (plus matplotlib for the plot)."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

DATA = Path(__file__).parent / "data"

cube = np.load(DATA / "flux_cube.npy")
mask = np.load(DATA / "aperture_mask.npy")
time = np.load(DATA / "time.npy")

print("cube:", cube.shape, cube.dtype)
print("mask:", mask.shape, mask.dtype, "pixels in aperture:", mask.sum())
print("time:", time.shape, time.dtype, f"from {time[0]:.3f} to {time[-1]:.3f} days")

sizes = {p.name: p.stat().st_size / 1024 for p in DATA.glob("*.npy")}
for name, kb in sorted(sizes.items()):
    print(f"{name:20s} {kb:8.1f} KB")

nan_frames = np.isnan(cube).all(axis=(1, 2))
print(f"NaN frames: {nan_frames.sum()} of {len(cube)} ({nan_frames.mean():.1%})")
print("partially NaN frames:", (np.isnan(cube).any(axis=(1, 2)) & ~nan_frames).sum())

light_curve = np.nansum(cube[:, mask], axis=1)
light_curve[nan_frames] = np.nan  # nansum of all-NaN gives 0, hide those
normalized = light_curve / np.nanmedian(light_curve)
print(f"Deepest point: {np.nanmin(normalized):.4f} (1 - depth)")

outside = ~mask
print(f"Background per pixel (median outside aperture): {np.nanmedian(cube[:, outside]):.1f}")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(time, normalized, ".", ms=2, color="k")
ax.set_xlabel("Time [days]")
ax.set_ylabel("Normalized brightness")
ax.set_title("np.nansum(cube[:, mask], axis=1)")
fig.tight_layout()
fig.savefig(DATA / "light_curve_check.png", dpi=100)
print("Saved", DATA / "light_curve_check.png")
