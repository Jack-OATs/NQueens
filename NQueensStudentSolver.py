from NQueensWorld import NQueensWorld
import time
from random import randint, random
from math import exp

class NQueensSolver:
    def __init__(self, N, time_limit=300):
        self.__N = N
        self.count = 0
        self.__time_limit = time_limit
        self.__start_time = None

    def attempt_with_brute_force_dumb(self):
        self.__start_time = time.perf_counter()
        for i in range(10**self.__N):
            if time.perf_counter() - self.__start_time >= self.__time_limit:
                raise TimeoutError("Ran out of time with i={}".format(i))
            temp_state = [0 for _ in range(self.__N)]
            temp_i = i
            cnt = -1
            invalid = False
            while temp_i > 0 and not invalid:
                digit = temp_i % 10
                temp_state[cnt] = temp_i % 10
                temp_i = temp_i // 10
                cnt -= 1
            if not invalid:
                try:
                    temp_world = NQueensWorld(self.__N, state=temp_state)
                    if temp_world.eval_fn() == 0:
                        print("found solution in {} seconds".format(time.perf_counter()-self.__start_time))
                        return temp_world
                except ValueError:
                    pass
        return None

    def attempt_with_brute_force_smart(self):
        self.__start_time = time.perf_counter()
        for i in range(10**self.__N):
            if time.perf_counter() - self.__start_time >= self.__time_limit:
                raise TimeoutError("Ran out of time with i={}".format(i))
            temp_state = [0 for _ in range(self.__N)]
            temp_i = i
            cnt = -1
            invalid = False
            while temp_i > 0 and not invalid:
                digit = temp_i % 10
                if digit >= self.__N:
                    invalid = True
                temp_state[cnt] = temp_i % 10
                temp_i = temp_i // 10
                cnt -= 1
            if len(set(temp_state)) != self.__N:
                invalid = True
            if not invalid:
                try:
                    temp_world = NQueensWorld(self.__N, state=temp_state)
                    if temp_world.eval_fn() == 0:
                        return temp_world
                except ValueError:
                    pass
        return None

    def attempt_with_hill_climbing_dumb(self, world=None, depth=0):
        if depth == 0:
            self.__start_time = time.perf_counter()
        if time.perf_counter() - self.__start_time >= self.__time_limit:
            raise TimeoutError("Ran out of time.")
        if world is None:
            world = NQueensWorld(self.__N)
        best_ev = world.eval_fn()
        next_states = world.get_one_move_next_states()
        i = 0
        better_world = None
        while i < self.__N and better_world is None:
            temp_world = NQueensWorld(state=next_states[i])
            if temp_world.eval_fn() < best_ev:
                better_world = temp_world
                best_ev = temp_world.eval_fn()
            i += 1
        if better_world is None:
            return world
        if best_ev == 0:
            return better_world
        return self.attempt_with_hill_climbing_dumb(better_world, depth+1)

    def attempt_with_hill_climb_smart(self, world=None, depth=0):
        if depth == 0:
            self.__start_time = time.perf_counter()
        if time.perf_counter() - self.__start_time >= self.__time_limit:
            raise TimeoutError("Ran out of time.")
        if world is None:
            world = NQueensWorld(self.__N)
        best_ev = world.eval_fn()
        next_states = world.get_one_move_next_states()
        next_states = sorted(next_states)
        t_world = NQueensWorld(state=next_states[randint(0, len(next_states)-1)])
        x = 0
        for _ in next_states:
            if t_world.eval_fn() > NQueensWorld(state=next_states[x]).eval_fn():
                t_world = NQueensWorld(state=next_states[x])
            x += 1
        better_world = None
        temp_world = t_world
        if temp_world.eval_fn() < best_ev:
            better_world = temp_world
            best_ev = temp_world.eval_fn()
        if better_world is None:
            return world
        if best_ev == 0:
            return better_world
        return self.attempt_with_hill_climb_smart(better_world, depth+1)

    def attempt_with_stocastich_hill_climb(self, world=None, depth=0):
        if depth == 0:
            self.__start_time = time.perf_counter()
        if time.perf_counter() - self.__start_time >= self.__time_limit:
            raise TimeoutError("Ran out of time.")
        if world is None:
            world = NQueensWorld(self.__N)
        better = []
        best_ev = world.eval_fn()
        next_states = world.get_one_move_next_states()
        for i in next_states:
            if NQueensWorld(state=i).eval_fn() < best_ev:
                better.append(NQueensWorld(state=i))
        better_world = None
        if len(better) > 0:
            better_world = better[randint(0, len(better)-1)]
            best_ev = better_world.eval_fn()
        if better_world is None:
            return world
        if best_ev == 0:
            return better_world
        return self.attempt_with_stocastich_hill_climb(better_world, depth+1)

    def attempt_with_random_restart_hill_climbing(self):
        self.__start_time = time.perf_counter()
        curr_attempt = self.attempt_with_hill_climb_smart(world=NQueensWorld(state=-1))
        while time.perf_counter() - self.__start_time < self.__time_limit:
            if curr_attempt.eval_fn() == 0:
                return curr_attempt
        return curr_attempt

    def attempt_with_genetic_algo(self):
        self.__start_time = time.perf_counter()
        population_size = 3
        half = self.__N // 2
        population = []
        for _ in range(population_size):
            population.append(NQueensWorld(N=self.__N, state=-1))

        while time.perf_counter() - self.__start_time < self.__time_limit:
            for _ in range(population_size):
                parent1 = population[randint(0, population_size-1)].get_state()
                parent2 = population[randint(0, population_size-1)].get_state()
                child1 = NQueensWorld(state=parent1[:half] + parent2[half:])
                child2 = NQueensWorld(state=parent2[:half] + parent1[half:])
                if random() <= .85:
                    child1_state = child1.get_state()
                    child1_state[randint(0, self.__N-1)] = randint(0, self.__N-1)
                    child1 = NQueensWorld(state=child1_state)

                if random() <= .85:
                    child2_state = child2.get_state()
                    child2_state[randint(0, self.__N-1)] = randint(0, self.__N-1)
                    child2 = NQueensWorld(state=child2_state)
                if child1 not in population:
                    population.append(child1)
                if child2 not in population:
                    population.append(child2)
            population = sorted(population, reverse=True)
            population = population[:population_size]
            if population[0].eval_fn() == 0:
                return population[0]
        return population[0]

    def attempt_with_simulated_annealing(self):
        self.__start_time = time.perf_counter()
        curr_world = NQueensWorld(N=self.__N, state=-1)
        while time.perf_counter() - self.__start_time < self.__time_limit:
            temp = 1/time.perf_counter()
            if curr_world.eval_fn() == 0:
                return curr_world
            next_world = curr_world.get_one_move_next_states()
            next_world = NQueensWorld(state=next_world[randint(0, len(next_world)-1)])
            dE = next_world.eval_fn() - curr_world.eval_fn()
            if dE < 0:
                curr_world = next_world
            else:
                if exp(-(dE/temp)) >= random():
                    curr_world = next_world

        return curr_world

    def my_best_algo(self):
        return self.attempt_with_simulated_annealing()


if __name__ == "__main__":
    solver = NQueensSolver(6)
    # print(solver.attempt_with_genetic_algo())
