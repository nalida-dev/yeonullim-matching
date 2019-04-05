class Problem:
    def __init__(self, query):
        self.problem = None
        self.description = ''
        parsed = self.parse_query(query)

    def parse_query(self, query):
        args = [[j.strip() for j in i.split()] for i in query.split(',')]

        # validity check
        # 1. 중복된 사람
        alphabet = [i[0] for i in args] 
        if len(alphabet) != len(set(alphabet)):
            self.description = '뭔가 중복된 사람이 있는듯?'
            return

        # 2. 같은 사람 두 번 고름
        if any([i[1] == i[2] for i in args]):
            duplicated = next(i[1] for i in args if i[1] == i[2])
            self.description = '{}가 {}를 두 번 골랐네요'.format(i[0], i[1])
            return

        # 3. 두 번 초과로 골라짐
        # 4. 없는 사람을 고름
        visited = [0] * len(alphabet)
        for i in args:
            if i[1] not in alphabet or i[2] not in alphabet:
                self.description = '{}가 누구임???'.format(i[1] if i[1] not in alphabet else i[2])
                return
            visited[alphabet.index(i[1])] += 1
            visited[alphabet.index(i[2])] += 1
        for i, val in enumerate(visited):
            if val > 2:
                self.description = '{}를 {}번 고름;;'.format(alphabet[i], val)
                return

        self.problem = {
            'alphabet': alphabet,
            'graph': [[alphabet.index(j) for j in i] for i in args]
        }
        
        descriptions = []
        for d_from, d_to_1, d_to_2 in self.problem['graph']:
            descriptions.append('{}는 {} 또는 {}를 원한다.'.format(alphabet[d_from], alphabet[d_to_1], alphabet[d_to_2]))
        self.description = '\n'.join(descriptions)
