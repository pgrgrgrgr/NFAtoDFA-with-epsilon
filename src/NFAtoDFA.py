from ReduceDFA import reduce_DFA

## automata arguments
Q = input("enter states: ").split()
symbols = input("enter symbols: ").split()
q0 = input("enter start state: ")
F = input("enter final state: ").split()
delta = {}

## mapping
for Vn in Q:
    delta[Vn] = {}
    for Vt in symbols:
        print("δ(", Vn, ",", Vt, ") =", end=" ")
        delta[Vn][Vt] = list(sorted(input().split()))

## set first state
dfa_states = [[q0]]

dfa_delta = []

new_dfa_states = [[q0]]

## get DFA
while len(new_dfa_states) > 0:
    current_state = new_dfa_states[0]
    new_dfa_states = new_dfa_states[1:]

    print('Current state: ', current_state)

    for symbol in symbols:
        next_states = []
        for nfa_state in current_state:
            for x in delta[nfa_state][symbol]:
                if x not in next_states:
                    next_states.append(x)
        next_states = sorted(next_states)
        dfa_delta.append([current_state, symbol, next_states])
        print('Symbol: ', symbol, ' States: ', next_states)
        if next_states not in dfa_states:
            dfa_states.append(next_states)
            new_dfa_states.append(next_states)
    
## set values for reducing DFA
for_reduced_states = sum(dfa_states, [])
for_reduced_final = []
for_reduced_delta = []


for i in F:
    for j in dfa_states:
        if i in j and j:
            for_reduced_final.append(j)

for i in dfa_delta:
    if i[2]:
        for_reduced_delta.append([[i[0], i[1]], i[2]])

## print
print("[ DFA ]")
print("[[[current state, symbol], [next state]]")
for i in for_reduced_delta:
    print(i)

for_reduced_states, for_reduced_delta, for_reduced_final = reduce_DFA(dfa_states, symbols, for_reduced_delta, [q0], for_reduced_final)
print("----------------------------------------")

print("[ reduced DFA ]")
print("[[[current state, symbol], [next state]]")
for i in for_reduced_delta:
    print(i)