# Knight's Tour Problem Solver using Genetic Algorithm

**Author:** Dr. Meriem SEBAI, USTHB  
**Course:** Problem Solving - Master 1, Visual Computing  
**Academic Year:** 2025/2026  
**Project:** Project 2

## Overview

This project implements a genetic algorithm to solve the Knight's Tour problem. The knight must visit every square on an 8×8 chessboard exactly once using only valid L-shaped moves.

## Algorithm Details

### Knight Moves
The knight can move in 8 possible L-shaped directions:
1. Up-right: (2, 1)
2. Right-up: (1, 2)  
3. Right-down: (1, -2)
4. Down-right: (2, -1)
5. Down-left: (-2, -1)
6. Left-down: (-1, -2)
7. Left-up: (-1, 2)
8. Up-left: (-2, 1)

### Genetic Algorithm Components

#### 1. Chromosome Class
- **Genes:** Array of 63 integers (1-8) representing knight moves
- **Crossover:** Single-point crossover between two parents
- **Mutation:** Random change of genes with configurable probability

#### 2. Knight Class  
- **Position:** Current (x, y) coordinates on the board
- **Chromosome:** Sequence of moves (genes)
- **Path:** List of visited positions
- **Fitness:** Number of squares successfully visited (max 64)
- **Move validation:** Checks for board boundaries and revisited squares
- **Move correction:** Uses forward/backward cycling to find valid alternatives

#### 3. Population Class
- **Tournament Selection:** Selects parents using tournament of size 3
- **Generational Replacement:** Creates new population through crossover and mutation
- **Fitness Evaluation:** Tracks best solution across generations

## Files

### Core Implementation
- `knights_tour_genetic.py` - Main implementation with GUI visualization
- `knights_tour_console.py` - Console-only version (recommended)
- `test_knights_tour.py` - Unit tests for all classes
- `quick_test.py` - Fast test with optimized parameters

### Generated Files
- `knights_tour_solution_fitness_XX.png` - Visualization of best solution

## Usage

### Console Version (Recommended)
```bash
python knights_tour_console.py
```

### GUI Version
```bash
python knights_tour_genetic.py
```
*Note: GUI version requires proper tkinter setup*

### Running Tests
```bash
python test_knights_tour.py
```

## Algorithm Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Population Size | 100 | Number of knights in each generation |
| Max Generations | 200 | Maximum number of iterations |
| Tournament Size | 3 | Number of candidates in parent selection |
| Mutation Rate | 0.1 | Probability of gene mutation (10%) |
| Crossover Type | Single-point | Method for combining parent chromosomes |

## Results

The algorithm typically achieves:
- **Best Case:** Complete tour (64/64 squares) - rare but possible
- **Typical Results:** 58-62 squares visited (90-97% completion)
- **Convergence:** Usually within 50-200 generations

### Sample Output
```
Generation   1: NEW BEST fitness = 56/64
Generation   7: NEW BEST fitness = 61/64
...
FINAL RESULTS:
Best fitness achieved: 61/64 squares
Generations run: 57
❌ Partial solution: 61/64 squares (95.3%)
```

## Visualization

The console version displays:
1. **Text Board:** Numbered squares showing the knight's path
2. **Path Coordinates:** Complete list of visited positions  
3. **Chromosome:** The genetic representation of the solution

Example board output:
```
Knight's Path on Chessboard:
  0   1   2   3   4   5   6   7
  ------------------------
0|  1  4 49 24 29       22
1| 50 27 30  3 48 23 32 37
2|  5  2 25 28 31 36 21 46
3| 26 51 10 35 14 47 38 33
4| 11  6 13 52  9 34 45 20
5| 56 53  8 15 60 19 42 39
6|  7 12 57 54 17 40 59 44
7|    55 16 61 58 43 18 41
```

## Dependencies

- Python 3.7+
- matplotlib (for GUI version only)
- numpy (for GUI version only)

### Installing Dependencies
```bash
pip install matplotlib numpy
```

## Algorithm Features

### 1. Move Validation and Correction
- Checks if moves lead outside the 8×8 board
- Prevents revisiting already visited squares
- Automatically corrects invalid moves using cycling strategy

### 2. Adaptive Search Strategy  
- Random forward/backward cycling for each knight
- Maintains diversity in move correction approaches
- Balances exploration vs exploitation

### 3. Tournament Selection
- Size-3 tournaments ensure good parent quality
- Maintains population diversity
- Prevents premature convergence

### 4. Early Stopping
- Stops after 50 generations without improvement
- Prevents unnecessary computation
- Configurable stagnation threshold

## Performance Optimization Tips

1. **Increase Population Size:** Better exploration but slower per generation
2. **Adjust Mutation Rate:** Higher rates increase exploration
3. **Tournament Size:** Larger tournaments increase selection pressure  
4. **Multiple Runs:** Run algorithm several times for better results

## Known Limitations

1. **Perfect Solutions Rare:** Complete 64-square tours are mathematically challenging
2. **Local Optima:** Algorithm may get stuck in high-fitness partial solutions
3. **No Backtracking:** Once a path is established, no revisiting of earlier decisions

## Educational Value

This implementation demonstrates:
- Genetic algorithm principles
- Constraint satisfaction problems
- Heuristic search techniques  
- Object-oriented design patterns
- Algorithm analysis and optimization

## Future Improvements

- **Hybrid Approaches:** Combine with local search or backtracking
- **Advanced Crossover:** Multi-point or uniform crossover methods
- **Adaptive Parameters:** Dynamic mutation rates based on population diversity
- **Parallel Processing:** Multi-threaded population evaluation
- **Different Board Sizes:** Generalize to NxN boards

---

*This implementation serves as both a practical solver and educational tool for understanding genetic algorithms applied to combinatorial optimization problems.*