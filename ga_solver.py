import random
from deap import creator, base, tools, algorithms
from matching import Problem


class SolverGA:
    def __init__(self, problem):
        self.alphabet = problem.problem['alphabet']
        self.graph = problem.problem['graph']
        self.ideal_group_size = 3
        self.n = len(self.alphabet)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_k", random.randint, 1, self.n)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_k, n=self.n)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", self.eval)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def aggregate_genes_to_groups(self, individual):
        groups = []
        for group_ind in range(1, self.n + 1):
            aggr = [i for i in range(self.n) if individual[i] == group_ind]
            if aggr:
                groups.append(aggr)
        return groups

    def eval(self, individual, verbose=False):
        def vprint(*args, **kwargs):
            if verbose:
                print(*args, **kwargs)
        groups = self.aggregate_genes_to_groups(individual)
        fit = 0
        for group in groups:
            for person in group:
                if self.graph[person][0] in group or self.graph[person][1] in group:
                    fit += 1000
            if self.ideal_group_size < len(group):
                fit -= 5 * (self.ideal_group_size - len(group)) ** 2
            else:
                fit -= (self.ideal_group_size - len(group)) ** 2
        return fit,

    def find_best_groups(self, generations=50):
        population = self.toolbox.population(n=300)
        for gen in range(generations):
            offspring = algorithms.varAnd(population, self.toolbox, cxpb=0.5, mutpb=0.1)
            fits = self.toolbox.map(self.toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population = self.toolbox.select(offspring, k=len(population))
        top10 = tools.selBest(population, k=10)
        return top10[0]

    def solve(self):
        candidates = []
        for repeat in range(20):
            best_individual = self.find_best_groups()
            candidates.append((self.eval(best_individual), best_individual))
        print(candidates)
        candidates.sort()
        self.best_fit = candidates[-1][0]
        self.best_individual = candidates[-1][1]

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
    problem = Problem('주정 소소 냥냥, 편민 주정 냥냥, 소소 짱짱 주정, 짱짱 문졍 첸샤, 부엉 문졍 제제, 문졍 총총 짱짱, 첸샤 편민 강강, 총총 부엉 강강, 강강 제제 소소, 제제 총총 첸샤, 냥냥 부엉 편민')
    solver = SolverGA(problem)
    solver.solve()
    print(solver.describe_solution())

