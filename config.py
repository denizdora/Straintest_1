# config.py

# Paths
DATA_FOLDER = "data"
OUTPUT_FOLDER = "output"
RESULTS_FOLDER = "results"

# File order by decreasing distance between clamps (for labeling)
FILE_ORDER = ["27.txt", "25.txt", "23.txt", "21.txt", "19.txt", "17.txt", "13.txt"]

# Bragg signals by placement
TOP_SURFACE_COLS = ["WL 1[nm]", "WL 2[nm]", "WL 3[nm]"]         # experience tension (↑ wavelength)
BOTTOM_SURFACE_COLS = ["WL 4[nm]", "WL 5[nm]", "WL 6[nm]"]      # experience compression (↓ wavelength)

ALL_SIGNAL_COLS = TOP_SURFACE_COLS + BOTTOM_SURFACE_COLS

"""
In the three-point bending setup, the optical fibers on the top surface of the beam experience tensile strain,
resulting in an increase in Bragg wavelength.
In contrast, the bottom surface fibers are subjected to compressive strain,
leading to a decrease in Bragg wavelength.
We label these groups as 'Top Surface' and 'Bottom Surface' respectively.
"""