import random
from deap import creator, base, tools, algorithms
from problem import Problem

class SolverGA:
    def __init__(self, problem, send):
        self.send = send 

        self.alphabet = problem.problem['alphabet']
        self.graph = problem.problem['graph']
        self.ideal_group_size = 3
        self.n = len(self.alphabet)
        self.m = self.n // self.ideal_group_size + 1

        creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0, 1.0))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_k", random.randint, 1, self.m)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_k, n=self.n)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", self.eval)
        self.toolbox.register("mate", tools.cxUniform, indpb=0.5)
        # self.toolbox.register("mate", tools.cxTwoPoint) #Uniform, indpb=0.5)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def aggregate_genes_to_groups(self, individual):
        groups = []
        for group_ind in range(1, self.m + 1):
            aggr = [i for i in range(self.n) if individual[i] == group_ind]
            if aggr:
                groups.append(aggr)
        return groups

    def eval(self, individual, verbose=False):
        def vprint(*args, **kwargs):
            if verbose:
                print(*args, **kwargs)
        groups = self.aggregate_genes_to_groups(individual)
        matches = 0
        penalty = 0
        for group in groups:
            for person in group:
                if self.graph[person][0] in group or self.graph[person][1] in group:
                    matches += 1
            if self.ideal_group_size < len(group):
                penalty += 5 * (self.ideal_group_size - len(group)) ** 2
            else:
                penalty += (self.ideal_group_size - len(group)) ** 2

        groups_too_big = [i for i in groups if len(i) >= 6]
        return (-len(groups_too_big), matches, -penalty)

    def normalize(self, individual):
        intermediate = [individual.index(i) for i in individual]
        order = list(set(intermediate))
        individual[:] = [order.index(i) + 1 for i in intermediate] 

    def normalize_population(self, population):
        for individual in population:
            self.normalize(individual)

    def optimize(self, individual):
        flag = False
        current_fit = self.eval(individual)
        for i, val in enumerate(individual):
            for j in range(1, self.m+1):
                individual[i] = j
                new_fit = self.eval(individual)
                if current_fit < new_fit:
                    current_fit = new_fit
                    val = j
                    flag = True
            individual[i] = val
        individual.fitness.values = current_fit
        return flag

    def optimize_population(self, population):
        for i, individual in enumerate(population):
            while self.optimize(individual):
                pass

    def find_best_groups(self, generations=50):
        population = self.toolbox.population(n=50)#300)
        # population[0][:] = [1] * self.n
        self.optimize_population(population)
        self.normalize_population(population)
        # print(population)
        for gen in range(generations):
            # print(gen)
            offspring = algorithms.varAnd(population, self.toolbox, cxpb=0.5, mutpb=0.1)
            fits = self.toolbox.map(self.toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population.sort(key=lambda x:x.fitness)
            population[:40] = self.toolbox.select(offspring, k=40) 
            self.optimize_population(population)
            self.normalize_population(population)
            top10 = tools.selBest(population, k=10)
            # print(top10[0].fitness)
        top10 = tools.selBest(population, k=10)
        return top10[0]

    def solve(self):
        candidates = []
        generations = [10] * 10
        for repeat in range(10):
            if repeat == 3:
                self.send('1/3쯤 했어요...')
            elif repeat == 7:
                self.send('2/3쯤 했어요...')
            best_individual = self.find_best_groups(generations=generations[repeat])
            candidates.append((self.eval(best_individual), best_individual))
            # print(generations[repeat])
        # print(candidates)
        candidates.sort()
        self.best_fit = candidates[-1][0]
        self.best_individual = candidates[-1][1]
        return self.describe_solution()

    def describe_solution(self):
        best_groups = self.aggregate_genes_to_groups(self.best_individual)
        descriptions = ['매칭 점수: {}'.format(self.best_fit)]
        for i, group in enumerate(best_groups):
            descriptions.append('그룹 {}: {}'.format(i+1, ', '.join(map(lambda x: self.alphabet[x], group))))
            for person in group:
                target = self.graph[person][0] if self.graph[person][0] in group else self.graph[person][1]
                descriptions.append('{} -> {}'.format(self.alphabet[person], self.alphabet[target]))
        return '\n'.join(descriptions)

if __name__ == "__main__":
#    problem = Problem('주정 소소 냥냥, 편민 주정 냥냥, 소소 짱짱 주정, 짱짱 문졍 첸샤, 부엉 문졍 제제, 문졍 총총 짱짱, 첸샤 편민 강강, 총총 부엉 강강, 강강 제제 소소, 제제 총총 첸샤, 냥냥 부엉 편민')
    problem = Problem('주정 소소 냥냥, 편민 주정 냥냥, 소소 짱짱 주정, 짱짱 문졍 첸샤, 부엉 문졍 제제, 문졍 총총 짱짱, 첸샤 편민 강강, 총총 부엉 강강, 강강 제제 소소, 제제 총총 첸샤, 냥냥 부엉 편민, 1 2 3, 2 3 4, 3 4 5, 4 5 6, 5 6 7, 6 7 8, 7 8 9, 8 9 0, 9 0 1, 0 1 2')
    problem = Problem('주정 소소 냥냥, 편민 주정 냥냥, 소소 짱짱 주정, 짱짱 문졍 첸샤, 부엉 문졍 제제, 문졍 총총 짱짱, 첸샤 편민 강강, 총총 부엉 8, 강강 제제 소소, 제제 총총 첸샤, 냥냥 7 강강, 1 2 3, 2 3 4, 3 4 5, 4 5 6, 5 6 부엉, 6 7 편민, 7 8 9, 8 9 1, 9 1 2')
    solver = SolverGA(problem, print)
    print(solver.solve())

