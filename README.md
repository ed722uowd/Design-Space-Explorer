

# Pareto-Optimal Design Exploration for Sobel Filter Using Pragma Combinations

This project performs design space exploration by evaluating various pragma attribute combinations for a Sobel filter hardware description. It extracts latency and ALUT usage for each configuration and plots the Pareto-optimal points.

---

## Project Structure

```
├── main_script.py              # Main script to run
├── extract_attributes.py       # Contains get_attributes and attribute_combination functions
├── lib_sobel.info              # Input file with pragma attribute information
├── plot_points.txt             # Optional: precomputed ALUTs, Latency pairs
├── sobel.c                     # Sobel C model (used if CyberWorkBench is available)
├── sobel.QOR                   # Output QOR file from CyberWorkBench (if used)
├── attrs.h                     # Generated attribute header file
├── *.csv                       # Output files containing optimal pragma combinations
├── README.md                   # This file
```

---

## Requirements

* Python 3.6+
* Optional: CyberWorkBench (if doing full synthesis)
* Required Python libraries:

  * `pandas`
  * `matplotlib`
  * `numpy`

---

## Setup Instructions

### 1. Create Virtual Environment

```bash
python3 -m venv myenv
```

### 2. Activate Virtual Environment

* On **Linux/macOS**:

  ```bash
  source myenv/bin/activate
  ```
* On **Windows**:

  ```bash
  myenv\Scripts\activate
  ```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

Create a `requirements.txt` with the following content:

```
pandas
matplotlib
numpy
```

---

## How to Run

### Option 1: Without CyberWorkBench

1. **COMMENT OUT** the CyberWorkBench section mentioned below.
 ```python
    if os.path.exists(qor_file):
          os.remove(qor_file)
    subprocess.run('cpars sobel.c', shell=True)
    subprocess.run('bdltran -c2000 -s sobel.IFF -lfl cycloneV.FLIB -lb cycloneV.BLIB', shell=True)

    ALUTs, Latency = extract_points (qor_file)

    plot_points [i][0] = ALUTs
    plot_points [i][1] = Latency

    print(plot_points)
    subprocess.run('clear', shell=True)
    print(i)
```

2. **UNCOMMENT** the following line (which uses pre-saved data):

```python
plot_points = read_plot_points("plot_points.txt")
```

### Option 2: With CyberWorkBench (if available)

1. **UNCOMMENT** the following section inside the main script:

```python
    if os.path.exists(qor_file):
          os.remove(qor_file)
    subprocess.run('cpars sobel.c', shell=True)
    subprocess.run('bdltran -c2000 -s sobel.IFF -lfl cycloneV.FLIB -lb cycloneV.BLIB', shell=True)

    ALUTs, Latency = extract_points (qor_file)

    plot_points [i][0] = ALUTs
    plot_points [i][1] = Latency

    print(plot_points)
    subprocess.run('clear', shell=True)
    print(i)
```

2. **COMMENT** the following line:

```python
plot_points = read_plot_points("plot_points.txt")
```

> This ensures the program uses **actual synthesis results** rather than dummy data from `plot_points.txt`.

---

This will:

* Generate attribute combinations
* Create `attrs.h` with each configuration
* Run CyberWorkBench commands (cpars, bdltran)
* Parse the resulting `sobel.QOR`
* Extract ALUTs and Latency
* Identify and plot Pareto-optimal points

---

## Output

* A **scatter plot** showing all designs and Pareto-optimal points (ALUTs vs Latency).
* CSV files named:

  ```
  pragmas_Latency_<latency>_ALUTs_<aluts>_<index>.csv
  ```

  These contain the pragma combinations that led to optimal results.

---

## Notes

* Make sure `lib_sobel.info` is correctly formatted with attribute lines starting with `A` followed by numbers.
* If using CyberWorkBench, make sure `sobel.c` is compatible and synthesis tools are in your path.
  * If using CyberWorkBench, you need the `sobel.c` code with the required pragmas placed across the code read from `attrs.h`.
  * You will also need the .FLIB and .BLIB files.
* The code repository does'nt include the pragma version of `sobel.c` as the code is propriertory
* The code above gives an idea of how a Design Space explorer works trying all combinations exhastively.

---

