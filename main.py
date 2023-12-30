from A_star import AStar
from bfs import BFS
from solver import SlidingPuzzleSolver

if __name__ == "__main__":
    print("Enter the number of rows (N):")
    N = int(input())
    print("Enter the number of columns(M):")
    M = int(input())
    print("Do you specify the initial board? (y)es / (n)o:")
    specify_board = input()
    if specify_board == "y":
        initial_board = []
        print("Enter the initial board:")
        for i in range(N):
            row = list(map(int, input().split()))
            initial_board.append(row)
    else:
        initial_board = None

    solver = SlidingPuzzleSolver(N, M, initial_board)

    print("Choose the algorithm. (b)fs / (a)*:")
    algorithm = input()
    if algorithm == "a":
        solver.run(AStar, "manhattan_distance")
    else:
        solver.run(BFS)
