import json
import time

MOVES = [(2,1), (1,2), (1,-2), (2,-1), (-2,-1), (-1,-2), (-1,2), (-2,1)]



def get_neighbors(x, y, visited):
    neighbors = []
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in visited:
            neighbors.append((nx, ny))
    return neighbors

def count_onward_moves(x, y, visited):
    count = 0
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in visited:
            count += 1
    return count

def MRV(successors, visited):
    successor_counts = []
    for x, y in successors:
        temp_visited = visited | {(x, y)}
        onward_moves = count_onward_moves(x, y, temp_visited)
        successor_counts.append((onward_moves, x, y))
    
    successor_counts.sort(key=lambda item: item[0])
    
    return [(x, y) for _, x, y in successor_counts]

def LCV(successors, visited):
    successor_scores = []
    
    for x, y in successors:
        temp_visited = visited | {(x, y)}
        
        total_freedom = 0
        neighbors = get_neighbors(x, y, temp_visited)
        
        for nx, ny in neighbors:
            total_freedom += count_onward_moves(nx, ny, temp_visited)
        
        successor_scores.append((total_freedom, x, y))
    
    successor_scores.sort(key=lambda item: -item[0])
    
    return [(x, y) for _, x, y in successor_scores]

def successor_fct(x, y, visited):
    return get_neighbors(x, y, visited)

def backtracking(assignment):
    if len(assignment) == 64:
        return assignment
    
    current_x, current_y = assignment[-1]
    visited = set(assignment)
    
    successors = successor_fct(current_x, current_y, visited)
    
    if not successors:
        return None
    
    successors = MRV(successors, visited)
    successors = LCV(successors, visited)
    
    for x, y in successors:
        assignment.append((x, y))
        result = backtracking(assignment)
        if result is not None:
            return result
        assignment.pop()
    
    return None

def save_solution_to_file(path):
    solution_data = {
        "fitness": len(path),
        "path": path,
        "total_moves": len(path)
    }
    with open("knight_solution.json", "w") as f:
        json.dump(solution_data, f, indent=2)

def main():
    print("algo starts")
    start_time = time.time()
    assignment = [(0, 0)]
    solution = backtracking(assignment)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if solution:
        print(f"time: {elapsed_time:.4f} seconds")
        save_solution_to_file(solution)
    else:
        print("\n no solution")
    return solution

if __name__ == "__main__":
    main()