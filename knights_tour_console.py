"""
Knight's Tour Problem Solver using Genetic Algorithm - Console Version
This version runs without GUI visualization for better compatibility
"""

import random

class Chromosome:
    """
    Represents a chromosome in the genetic algorithm.
    Each chromosome contains genes representing the knight's moves.
    """
    
    def __init__(self, genes=None):
        """
        Creates a new chromosome.
        If no genes are provided, generates random genes for initial population.
        
        Args:
            genes: Array of 63 integers representing knight moves (1-8)
        """
        if genes is None:
            # Generate random moves (1-8) for initial population
            self.genes = [random.randint(1, 8) for _ in range(63)]
        else:
            self.genes = genes.copy()
    
    def crossover(self, partner):
        """
        Performs single-point crossover with another chromosome.
        
        Args:
            partner: Another Chromosome object to crossover with
            
        Returns:
            Two new Chromosome objects (offspring)
        """
        # Choose random crossover point
        crossover_point = random.randint(1, len(self.genes) - 1)
        
        # Create offspring by combining genes
        offspring1_genes = self.genes[:crossover_point] + partner.genes[crossover_point:]
        offspring2_genes = partner.genes[:crossover_point] + self.genes[crossover_point:]
        
        return Chromosome(offspring1_genes), Chromosome(offspring2_genes)
    
    def mutation(self, mutation_rate=0.1):
        """
        Applies mutation to the chromosome.
        Each gene has a probability to mutate into a random move.
        
        Args:
            mutation_rate: Probability of mutation for each gene
        """
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random.randint(1, 8)


class Knight:
    """
    Represents a knight on the chessboard with its position, chromosome, path, and fitness.
    """
    
    # Knight moves: direction -> (dx, dy)
    MOVES = {
        1: (2, 1),   # up-right
        2: (1, 2),   # right-up
        3: (1, -2),  # right-down
        4: (2, -1),  # down-right
        5: (-2, -1), # down-left
        6: (-1, -2), # left-down
        7: (-1, 2),  # left-up
        8: (-2, 1)   # up-left
    }
    
    def __init__(self, chromosome=None):
        """
        Creates a new knight.
        
        Args:
            chromosome: Chromosome object representing the knight's moves
        """
        self.position = (0, 0)  # Starting position
        self.chromosome = chromosome if chromosome else Chromosome()
        self.path = [(0, 0)]  # List of visited positions
        self.fitness = 0
        self.visited = set([(0, 0)])  # Set for faster lookup
    
    def move_forward(self, direction):
        """
        Moves the knight in the specified direction.
        
        Args:
            direction: Integer (1-8) representing the move direction
            
        Returns:
            New position (x, y) after the move
        """
        dx, dy = self.MOVES[direction]
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        return (new_x, new_y)
    
    def move_backward(self, direction):
        """
        Moves the knight backward (undoes a move).
        """
        if len(self.path) > 1:
            self.path.pop()
            self.position = self.path[-1]
            self.visited.remove(self.position) if len(self.path) > 1 else None
    
    def is_valid_position(self, pos):
        """
        Checks if a position is valid (within board and not visited).
        
        Args:
            pos: Position tuple (x, y)
            
        Returns:
            Boolean indicating if position is valid
        """
        x, y = pos
        return (0 <= x < 8 and 0 <= y < 8 and pos not in self.visited)
    
    def check_moves(self):
        """
        Checks and corrects the validity of moves in the chromosome.
        """
        self.position = (0, 0)
        self.path = [(0, 0)]
        self.visited = set([(0, 0)])
        
        cycle_forward = random.choice([True, False])  # Random cycle direction
        
        for i, move in enumerate(self.chromosome.genes):
            new_pos = self.move_forward(move)
            
            if self.is_valid_position(new_pos):
                # Valid move
                self.position = new_pos
                self.path.append(new_pos)
                self.visited.add(new_pos)
            else:
                # Invalid move - try to find alternative
                original_move = move
                found_valid = False
                
                # Try all other moves in cycle order
                for j in range(1, 8):  # Try 7 other moves
                    if cycle_forward:
                        test_move = ((original_move + j - 1) % 8) + 1
                    else:
                        test_move = ((original_move - j - 1) % 8) + 1
                    
                    test_pos = self.move_forward(test_move)
                    if self.is_valid_position(test_pos):
                        # Found valid alternative
                        self.chromosome.genes[i] = test_move
                        self.position = test_pos
                        self.path.append(test_pos)
                        self.visited.add(test_pos)
                        found_valid = True
                        break
                
                if not found_valid:
                    # No valid move found - keep original and stop
                    break
    
    def evaluate_fitness(self):
        """
        Evaluates the fitness of the knight based on visited squares.
        
        Returns:
            Fitness value (number of squares visited)
        """
        self.fitness = len(self.path)
        return self.fitness


class Population:
    """
    Represents a population of knights for the genetic algorithm.
    """
    
    def __init__(self, population_size):
        """
        Creates initial population of knights.
        
        Args:
            population_size: Number of knights in the population
        """
        self.population_size = population_size
        self.generation = 1
        self.knights = [Knight() for _ in range(population_size)]
    
    def check_population(self):
        """
        Checks the validity of moves for all knights in the population.
        """
        for knight in self.knights:
            knight.check_moves()
    
    def evaluate(self):
        """
        Evaluates fitness of all knights and returns the best one.
        
        Returns:
            Tuple: (max_fitness, best_knight)
        """
        best_knight = None
        max_fitness = 0
        
        for knight in self.knights:
            fitness = knight.evaluate_fitness()
            if fitness > max_fitness:
                max_fitness = fitness
                best_knight = knight
        
        return max_fitness, best_knight
    
    def tournament_selection(self, size=3):
        """
        Selects parents using tournament selection.
        
        Args:
            size: Tournament size (number of knights to sample)
            
        Returns:
            Two parent knights
        """
        # First parent
        tournament1 = random.sample(self.knights, size)
        parent1 = max(tournament1, key=lambda k: k.fitness)
        
        # Second parent
        tournament2 = random.sample(self.knights, size)
        parent2 = max(tournament2, key=lambda k: k.fitness)
        
        return parent1, parent2
    
    def create_new_generation(self):
        """
        Creates a new generation of knights using crossover and mutation.
        """
        new_knights = []
        
        while len(new_knights) < self.population_size:
            # Select parents
            parent1, parent2 = self.tournament_selection()
            
            # Crossover
            offspring1_chromosome, offspring2_chromosome = parent1.chromosome.crossover(parent2.chromosome)
            
            # Mutation
            offspring1_chromosome.mutation()
            offspring2_chromosome.mutation()
            
            # Create new knights
            new_knights.append(Knight(offspring1_chromosome))
            if len(new_knights) < self.population_size:
                new_knights.append(Knight(offspring2_chromosome))
        
        self.knights = new_knights[:self.population_size]
        self.generation += 1


def print_board_with_path(knight):
    """
    Prints a text representation of the chessboard with the knight's path.
    
    Args:
        knight: The knight with the solution path
    """
    # Create an 8x8 board
    board = [[' ' for _ in range(8)] for _ in range(8)]
    
    # Mark the path with numbers
    for i, pos in enumerate(knight.path):
        x, y = pos
        if 0 <= x < 8 and 0 <= y < 8:
            board[y][x] = f'{i+1:2d}'[:2]  # Limit to 2 characters
    
    print("\nKnight's Path on Chessboard:")
    print("  " + "   ".join([f"{i}" for i in range(8)]))
    print("  " + "---" * 8)
    
    for i in range(8):
        row_str = f"{i}|"
        for j in range(8):
            cell = board[i][j]
            if cell == ' ':
                cell = '  '
            row_str += f"{cell:>3}"
        print(row_str)
    
    print(f"\nPath: {knight.path}")
    print(f"Total squares visited: {len(knight.path)}/64")


def main():
    """
    Main function that runs the genetic algorithm for the Knight's Tour problem.
    """
    population_size = 100
    max_generations = 200
    
    print("Knight's Tour Genetic Algorithm - Console Version")
    print(f"Population size: {population_size}")
    print(f"Max generations: {max_generations}")
    print("=" * 60)
    
    # Create the initial population
    population = Population(population_size)
    
    best_fitness_ever = 0
    best_solution_ever = None
    generations_without_improvement = 0
    max_stagnant_generations = 50
    
    generation_count = 0
    while generation_count < max_generations:
        # Check the validity of the current population
        population.check_population()
        
        # Evaluate the current generation and get the best knight with its fitness value
        maxFit, bestSolution = population.evaluate()
        
        # Track improvements
        if maxFit > best_fitness_ever:
            best_fitness_ever = maxFit
            best_solution_ever = bestSolution
            generations_without_improvement = 0
            print(f"Generation {population.generation:3d}: NEW BEST fitness = {maxFit:2d}/64")
        else:
            generations_without_improvement += 1
        
        # Print progress every 20 generations
        if population.generation % 20 == 0:
            print(f"Generation {population.generation:3d}: Current best = {maxFit:2d}/64, Overall best = {best_fitness_ever:2d}/64")
        
        # Check for perfect solution
        if maxFit == 64:
            print("\n" + "=" * 60)
            print("🎉 PERFECT SOLUTION FOUND! 🎉")
            print(f"Knight completed the tour in generation {population.generation}")
            print(f"All 64 squares visited!")
            break
        
        # Check for stagnation (optional early stopping)
        if generations_without_improvement >= max_stagnant_generations:
            print(f"\nStopping early due to {max_stagnant_generations} generations without improvement.")
            break
        
        # Generate the new population
        population.create_new_generation()
        generation_count += 1
    
    print(f"\n" + "=" * 60)
    print(f"FINAL RESULTS:")
    print(f"Best fitness achieved: {best_fitness_ever}/64 squares")
    print(f"Generations run: {min(generation_count + 1, max_generations)}")
    
    if best_fitness_ever == 64:
        print("✅ Complete Knight's Tour found!")
    else:
        print(f"❌ Partial solution: {best_fitness_ever}/64 squares ({(best_fitness_ever/64)*100:.1f}%)")
    
    # Display the best solution
    print_board_with_path(best_solution_ever)
    
    # Show chromosome representation
    print(f"\nBest chromosome (first 20 genes): {best_solution_ever.chromosome.genes[:20]}")
    print(f"Complete chromosome: {best_solution_ever.chromosome.genes}")
    
    return best_fitness_ever, best_solution_ever


if __name__ == "__main__":
    fitness, solution = main()
    print(f"\nProgram completed. Best fitness: {fitness}/64")
    input("Press Enter to exit...")