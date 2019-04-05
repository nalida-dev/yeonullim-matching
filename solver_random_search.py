import random

from problem import Problem

class SolverRandomSearch:
    def __init__(self, problem):
        self.alphabet = problem.problem['alphabet']
        self.graph = problem.problem['graph']
        self.ideal_group_size = 3
        # self.tried_groups = set()

    def random_group(self, l, k):
        while True:
            group = [random.randint(1, k) for _ in range(len(l))]
            # key = ''.join(map(str, group))
            # if key in self.tried_groups:
                # continue
            # self.tried_groups.add(key)
            if len(set(group)) == k:
                result = []
                for group_ind in range(1, k+1):
                    result.append([elem for i, elem in enumerate(l) if group[i] == group_ind])
                return result


    def group_fit(self, groups):
        fit = 0
        for group in groups:
            for person in group:
                if self.graph[person][0] in group or self.graph[person][1] in group:
                    fit += 1000
            if self.ideal_group_size < len(group):
                fit -= 5 * (self.ideal_group_size - len(group)) ** 2
            else:
                fit -= (self.ideal_group_size - len(group)) ** 2
        return fit

    def find_best_groups(self, iterations=70000):
        n = len(self.alphabet)
        possible_num_group = int(n / self.ideal_group_size)
        num_groups_range = list(range(max(1, possible_num_group - 2), min(possible_num_group + 2, n)))

        max_fit = -99999999;
        for _ in range(iterations):
            for num_groups in num_groups_range:
                groups = self.random_group(list(range(len(self.alphabet))), num_groups)
                fit = self.group_fit(groups)
                if max_fit < fit:
                    max_groups = groups
                    max_fit = fit
                    # print(max_fit, max_groups)

        self.best_groups = max_groups
        self.best_fit = max_fit

    def describe_solution(self):
        if not self.best_groups:
            return 'Sorry, I could not find the valid match'
        descriptions = ['매칭 점수: {}'.format(self.best_fit)]
        for i, group in enumerate(self.best_groups):
            descriptions.append('그룹 {}: {}'.format(i+1, ', '.join(map(lambda x: self.alphabet[x], group))))
            for person in group:
                target = self.graph[person][0] if self.graph[person][0] in group else self.graph[person][1]
                descriptions.append('{} -> {}'.format(self.alphabet[person], self.alphabet[target]))
        return '\n'.join(descriptions)

    def solve(self):
        groups = self.find_best_groups()
        return self.describe_solution()

if __name__ == "__main__":
    problem = Problem('주정 소소 냥냥, 편민 주정 냥냥, 소소 짱짱 주정, 짱짱 문졍 첸샤, 부엉 문졍 제제, 문졍 총총 짱짱, 첸샤 편민 강강, 총총 부엉 강강, 강강 제제 소소, 제제 총총 첸샤, 냥냥 부엉 편민, 1 2 3, 2 3 4, 3 4 5, 4 5 6, 5 6 7, 6 7 8, 7 8 9, 8 9 1, 9 1 2')
    solver = SolverRandomSearch(problem)
    print(solver.solve())

