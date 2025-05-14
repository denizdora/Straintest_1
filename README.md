# Wind Turbine Blade Strain Analysis Using Fiber Optic Sensors

This project analyzes how a glass composite structure (similar to a wind turbine blade) responds to bending forces using fiber optic sensors. We use a **three-point bending test** to apply strain and observe how the material behaves under load.

### 🧪 Experiment Setup

- A beam made of **glass fiber composite** is placed on two supports.
- A force is applied at the center, bending the beam — just like wind bends a turbine blade.
- **Fiber Bragg Grating (FBG) sensors** are embedded on the top and bottom surfaces of the beam.
- These sensors measure **tiny changes in light wavelength** as the material stretches or compresses.

### 📊 What the Code Does

This Python project processes the raw wavelength data from the sensors and produces clear plots and statistics:

1. **Peak Detection**: Finds the local maxima or minima in the signal.
2. **Wavelength Shift (Δλ)**: Measures how much the wavelength changes due to bending.
3. **Mean and Standard Deviation**: Calculates average shift and variation for each sensor.
4. **Trend Over Distance**: Compares how strain evolves as the force point moves closer (more bending).
5. **Raw Signal & Derivative Visualization**:
   - Shows the raw sensor data.
   - Plots the **rate of change (derivative)** to highlight sudden movements or mechanical transitions.

### 📁 Project Structure

- `analyze_strain.py`: Main script that processes each test file and creates plots.
- `config.py`: Contains sensor names, file order, and folder paths.
- `mean_std_evolution.py`: Plots how average wavelength shifts evolve as the bending increases.
- `data/`: Tab-separated files containing raw sensor data.
- `output/`: Auto-generated plots showing signal, derivative, and peak differences.
- `results/`: Computed values of mean and standard deviation per test.

### 📷 Sample Outputs

The analysis generates:
- Line plots of **wavelength shifts over time**
- Visual summaries of **strain evolution**
- Clear indications of **compression vs tension behavior**

---

### 🔬 Why It Matters

This method is commonly used in aerospace, civil, and renewable energy applications. By understanding how materials deform under stress, engineers can design safer, more efficient structures — like **wind turbine blades** that must endure strong, repetitive wind forces.

---

### 🛠 Built With

- Python
- Pandas
- Matplotlib
- NumPy

---

### 👤 Author

Deniz Dora Kabakçıoğlu  
Electronics Engineering · Izmir Institute of Technology  
Erasmus Research @ University of Mons
