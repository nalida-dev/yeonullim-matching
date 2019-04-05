import random
import json

class Problem:
    def __init__(self, query):
        self.problem = None
        self.description = ''
        self.parse_query(query)

    def parse_query(self, query):
        try:
            args = [[j.strip() for j in i.split()] for i in query.split(',')]

            # validity check
            # 1. 중복된 사람
            alphabet = [i[0] for i in args] 
            if len(alphabet) != len(set(alphabet)):
                self.description = '뭔가 중복된 사람이 있는듯?'
                return

            # 2. 같은 사람 두 번 고름
            if any([i[1] == i[2] for i in args]):
                duplicated = next((i[0], i[1]) for i in args if i[1] == i[2])
                self.description = '{}(이)가 {}(을)를 두 번 골랐네요'.format(duplicated[0], duplicated[1])
                return

            # 2-1. 자기를 고름
            if any([i[0] == i[1] or i[0] == i[2] for i in args]):
                duplicated = next(i[0] for i in args if i[0] == i[1] or i[0] == i[2])
                self.description = '{}(이)가 자기를 골랐네요...'.format(duplicated)
                return

            # 3. 두 번 안 골라진 사람이 있음
            # 4. 없는 사람을 고름
            visited = [0] * len(alphabet)
            for i in args:
                if i[1] not in alphabet or i[2] not in alphabet:
                    self.description = '{}(이)가 누구임???'.format(i[1] if i[1] not in alphabet else i[2])
                    return
                visited[alphabet.index(i[1])] += 1
                visited[alphabet.index(i[2])] += 1
            for i, val in enumerate(visited):
                if val != 2:
                    self.description = '{}(을)를 {}번 고름;;'.format(alphabet[i], val)
                    return

            self.problem = {
                'alphabet': alphabet,
                'graph': [[alphabet.index(i[1]), alphabet.index(i[2])] for i in args]
            }
            
            descriptions = []
            for d_from, (d_to_1, d_to_2) in enumerate(self.problem['graph']):
                descriptions.append('{} -> {}, {}'.format(alphabet[d_from], alphabet[d_to_1], alphabet[d_to_2]))
            self.description = '\n'.join(descriptions)
        except:
            self.problem = None
            self.description = '형식에 맞게 적어주세요 ㅠㅠ'
            

class SolverPlain:
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
