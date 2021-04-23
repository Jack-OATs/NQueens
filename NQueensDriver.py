from NQueens.NQueensStudentSolver import NQueensSolver
import time

N = 45
time_limit = 30
solver = NQueensSolver(N, time_limit)
solve_options = {
                 # 'Dumb Brute force': solver.attempt_with_brute_force_dumb,
                 # 'Smart Brute Force': solver.attempt_with_brute_force_smart,
                 # 'Inefficient Hill Climbing': solver.attempt_with_hill_climbing_dumb,
                 # 'More Efficient Hill Climbing': solver.attempt_with_hill_climb_smart,
                 # 'Stochastic Hill Climbing': solver.attempt_with_stocastich_hill_climb,
                 # 'Random Restart Hill Climbing': solver.attempt_with_random_restart_hill_climbing
                 # 'Genetic Algorithm': solver.attempt_with_genetic_algo,
                 # 'My Best Algorithm': solver.my_best_algo,
                 'Simulated Annealing': solver.attempt_with_simulated_annealing
                 }

for k in solve_options.keys():
    st_time = time.perf_counter()
    solution = solve_options[k]()
    result = []
    ev = None
    if solution is not None:
        result = solution.get_state()
        ev = solution.eval_fn()
    end_time = time.perf_counter()
    print("Solution for {0} is {1} with eval fn of {3} in {2:.4f} seconds.".format(k, result, end_time - st_time, ev))

