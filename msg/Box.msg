# A single garment detected in an image.
# Coordinates are in pixels, relative to the top-left corner of the frame.

string  class_id   # Garment label (e.g. "top", "pants", "footwear")
float32 prob       # Detection confidence, in [0, 1]
int32   x          # X coordinate of the top-left corner
int32   y          # Y coordinate of the top-left corner
int32   width      # Box width
int32   height     # Box height
