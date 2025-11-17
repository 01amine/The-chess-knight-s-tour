import random
import json
import os

class Chromosome:
    
    
    def __init__(self, genes=None):
        if genes is None:
            self.genes = [random.randint(1, 8) for _ in range(63)]
        else:
            self.genes = genes.copy()
    
    def crossover(self, partner):
        
        point = random.randint(1, len(self.genes)-1)
        child1 = self.genes[:point] + partner.genes[point:]
        child2 = partner.genes[:point] + self.genes[point:]
        return Chromosome(child1), Chromosome(child2)
    
    def mutation(self, rate=0.1):
        
        for i in range(len(self.genes)):
            factor = 1 + (i / len(self.genes)) * 0.5
            effective_rate = min(0.4, rate * factor)
            if random.random() < effective_rate:
                self.genes[i] = random.randint(1, 8)

class Knight:
    

    MOVES = {
        1: (2,1), 2: (1,2), 3: (1,-2), 4: (2,-1),
        5: (-2,-1), 6: (-1,-2), 7: (-1,2), 8: (-2,1)
    }

    def __init__(self, chromosome=None):
        self.position = (0, 0)
        self.chromosome = chromosome if chromosome else Chromosome()
        self.path = [self.position]
        self.visited = set([self.position])
        self.fitness = 0

    def move_forward(self, direction):
        dx, dy = self.MOVES[direction]
        return (self.position[0] + dx, self.position[1] + dy)

    def move_backward(self, direction):

        dx, dy = self.MOVES[direction]
        self.position = (self.position[0] - dx, self.position[1] - dy)
        if self.path:
            self.path.pop()
        self.visited = set(self.path)

    def is_valid(self, pos):

        x, y = pos
        return 0 <= x < 8 and 0 <= y < 8 and pos not in self.visited

    def check_moves(self):

        self.position = (0, 0)
        self.path = [self.position]
        self.visited = set([self.position])
        cycle_forward = random.choice([True, False])  

        for i, move in enumerate(self.chromosome.genes):
            new_pos = self.move_forward(move)
            if self.is_valid(new_pos):
                # mouvement valide
                self.position = new_pos
                self.path.append(new_pos)
                self.visited.add(new_pos)
            else:
                
                valid_found = False
                for j in range(1, 8):
                    
                    if cycle_forward:
                        test_move = ((move + j - 1) % 8) + 1
                    else:
                        test_move = ((move - j - 1) % 8) + 1

                    test_pos = self.move_forward(test_move)
                    if self.is_valid(test_pos):
                        
                        self.chromosome.genes[i] = test_move
                        self.position = test_pos
                        self.path.append(test_pos)
                        self.visited.add(test_pos)
                        valid_found = True
                        break

                if not valid_found:
                   
                    self.move_backward(move)
                    break  

    def evaluate_fitness(self):

        self.fitness = len(self.path)
        return self.fitness
class Population:
    
    def __init__(self, size):
        self.size = size
        self.generation = 1
        self.knights = [Knight() for _ in range(size)]
    
    def check_population(self):
        for k in self.knights:
            k.check_moves()
    
    def evaluate(self):
        best_knight = max(self.knights, key=lambda k: k.evaluate_fitness())
        return best_knight.fitness, best_knight
    
    def tournament_selection(self, tour_size=None):
        if tour_size is None:
            tour_size = max(3, min(7, self.size//8)) if self.generation<50 else max(2, min(5, self.size//12))
        tour_size = min(tour_size, len(self.knights))
        tour = random.sample(self.knights, tour_size)
        tour.sort(key=lambda k: k.fitness, reverse=True)
        return tour[0], tour[1] if len(tour)>1 else tour[0]
    
    def create_new_generation(self):
        new_knights = []
        
        best = max(self.knights, key=lambda k: k.fitness)
        if best.fitness > 45:
            new_knights.append(best)
        
        while len(new_knights) < self.size:
            p1, p2 = self.tournament_selection()
            c1, c2 = p1.chromosome.crossover(p2.chromosome)
            avg_fit = (p1.fitness + p2.fitness)/2
            if avg_fit>55:
                c1.mutation(0.05)
                c2.mutation(0.05)
            else:
                c1.mutation(0.1)
                c2.mutation(0.1)
            new_knights.append(Knight(c1))
            if len(new_knights) < self.size:
                new_knights.append(Knight(c2))
        self.knights = new_knights[:self.size]
        self.generation += 1
        print(f"Generation {self.generation} created.")

def print_board(knight):
    board = [['  ']*8 for _ in range(8)]
    for i,pos in enumerate(knight.path):
        x,y = pos
        board[y][x] = f"{i+1:2d}"
    print("\nKnight's Path on Chessboard:")
    print("  "+"  ".join(map(str, range(8))))
    print("  "+"---"*8)
    for i,row in enumerate(board):
        print(f"{i}|"+"".join(f"{c:>3}" for c in row))
    print(f"\nTotal squares visited: {len(knight.path)}/64")
# ok
def save_solution_to_file(best_knight, fitness):

    solution_data = {
        "fitness": fitness,
        "path": best_knight.path,
        "chromosome": best_knight.chromosome.genes,
        "total_moves": len(best_knight.path)
    }
    
    with open("knight_solution.json", "w") as f:
        json.dump(solution_data, f, indent=2)
    print(f"Solution saved to knight_solution.json")

def main():
    pop_size = 100  
    population = Population(pop_size) 
    
    while True:
        
        population.check_population()
        
        
        maxFit, best_knight = population.evaluate()
        
        
        print(f"Generation {population.generation} - Best fitness: {maxFit}/64")
        
        
        if maxFit == 64:
            print("\n✅ Complete Knight's Tour achieved!")
            break
        
        
        population.create_new_generation()
    
   
    print_board(best_knight)
    print(f"Best chromosome: {best_knight.chromosome.genes}")
    
    save_solution_to_file(best_knight, maxFit)
    
    
    return maxFit, best_knight

if __name__ == "__main__":
    main()
