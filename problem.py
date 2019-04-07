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
            is_generous = [i.startswith('진행') for i in alphabet]
            alphabet = [i[2:] if i.startswith('진행') else i for i in alphabet]
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
                'is_generous': is_generous,
                'graph': [[alphabet.index(i[1]), alphabet.index(i[2])] for i in args]
            }
            
            descriptions = []
            for d_from, (d_to_1, d_to_2) in enumerate(self.problem['graph']):
                descriptions.append('{}{} -> {}, {}'.format(alphabet[d_from], '(진행자)' if is_generous[d_from] else '', alphabet[d_to_1], alphabet[d_to_2]))
            self.description = '\n'.join(descriptions)
        except:
            self.problem = None
            self.description = '형식에 맞게 적어주세요 ㅠㅠ'

