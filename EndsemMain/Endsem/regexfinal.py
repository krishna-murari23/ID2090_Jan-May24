# Creating a class defining various transitions involved, reference obtained from Python FSM documentation
class State:
    def __init__(self):
        self.transitions = {}
        self.epsilon_transitions = []

    def add_transition(self, char, state):
        if char not in self.transitions:
            self.transitions[char] = []
        self.transitions[char].append(state)

    def add_epsilon_transition(self, state):
        self.epsilon_transitions.append(state)

    def get_transitions(self, char):
        return self.transitions.get(char, []) + self.transitions.get(None, [])

    def get_epsilon_transitions(self):
        return self.epsilon_transitions

class FSM:
    def __init__(self):
        self.start_state = State()
        self.accept_state = State()

    def add_transition(self, from_state, to_state, char):
        from_state.add_transition(char, to_state)

    def add_epsilon_transition(self, from_state, to_state):
        from_state.add_epsilon_transition(to_state)

    def build_from_regex(self, regex):
        current_states = [self.start_state]
        i = 0
        while i < len(regex):
            char = regex[i]
            if char == '*':
                # * means zero or more of the previous state
                for state in current_states:
                    self.add_epsilon_transition(state, state)
                i += 1
                continue

            next_states = [State() for _ in current_states]
            for from_state, to_state in zip(current_states, next_states):
                if char == '.':
                    self.add_transition(from_state, to_state, None)  # Wildcard transition
                else:
                    self.add_transition(from_state, to_state, char)
                if i + 1 < len(regex) and regex[i + 1] == '*':
                    self.add_epsilon_transition(to_state, from_state)
                    self.add_epsilon_transition(from_state, to_state)
            current_states = next_states
            i += 1

        for state in current_states:
            self.add_epsilon_transition(state, self.accept_state)

    def match(self, string):
        def epsilon_closure(states):
            stack = list(states)
            closure = set(states)
            while stack:
                state = stack.pop()
                for next_state in state.get_epsilon_transitions():
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
            return closure

        match_spans = []
        n = len(string)

        for i in range(n):
            current_states = epsilon_closure({self.start_state})
            j = i
            while j < n:
                new_states = set()
                for state in current_states:
                    new_states.update(state.get_transitions(string[j]))
                    new_states.update(state.get_transitions(None))
                current_states = epsilon_closure(new_states)
                if self.accept_state in current_states:
                    match_spans.append((i, j + 1))
                    break
                j += 1

        return match_spans

def highlight_match(string, match_spans):
    highlighted_string = ""
    start_highlight = "\033[31m"
    end_highlight = "\033[0m"

    last_end = 0
    for start, end in match_spans:
        highlighted_string += string[last_end:start]
        highlighted_string += start_highlight + string[start:end] + end_highlight
        last_end = end

    highlighted_string += string[last_end:]
    return highlighted_string

def test_regex_engine():
    regex = "a*c*" #Can be modified appropriately
    fsm = FSM()
    fsm.build_from_regex(regex)

    test_strings = ["baacc"] #Can be modified , giving multiple entries in the list
    for s in test_strings:
        match_spans = fsm.match(s)
        highlighted = highlight_match(s, match_spans)
        print(f"{highlighted}") #Prints highlighted portion

if __name__ == "__main__":
    test_regex_engine()
