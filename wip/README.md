# Unfinished work

This directory contains code that is **not runnable**. It is kept only as a
record of the approach that was being developed.

## `visualization.py`

A node that detected people with YOLOv8, cropped each person's region of
interest, computed HSV histograms over those crops, and cross-referenced them
against the garments published by `clothing_detector_node.py`, with the goal of
re-identifying a person across subsequent frames.

**Why it does not run:** it depends on three modules that were not preserved.

| Module | Role | Status |
|---|---|---|
| `hsvHistogramCode.ImageProcessing` | Computed the HSV histogram of a ROI | Lost |
| `compareFrame.EnterFrame` | Managed the database and compared descriptors | Lost |
| `publish_image.ImageProcessing` | Published cropped ROIs | Lost |

The original project was put on hold and those files could not be recovered.
No reimplementations are included here, since they would not reflect the work
that was actually done.

## If this is ever resumed

What would need rebuilding, in order:

1. `hsvHistogramCode.py` — normalised HSV histogram per ROI. This is the base
   descriptor; nothing downstream has an input without it.
2. `compareFrame.py` — on-disk persistence plus a similarity metric between
   histograms (Bhattacharyya or correlation, via `cv2.compareHist`).
3. `publish_image.py` — publishing utility, the simplest piece.

The design is worth reconsidering before rewriting it: HSV-histogram
re-identification is highly sensitive to lighting changes, and a learned
descriptor (OSNet or any modern re-ID model) would give considerably better
results with less code.
