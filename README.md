# SeamCarving

## Seam Carver in Python

A content-aware image resizing technique where the image is reduced in size by one pixel of height (or width) at a time.

Unlike standard content-agnostic resizing techniques (e.g., cropping and scaling), themost interesting features (aspect ratio, set of objects present, etc.) of the image are preserved.

Calculates the 'energy' of each pixel, then uses recursive backtracking to identify beams that have the least change in energy.
