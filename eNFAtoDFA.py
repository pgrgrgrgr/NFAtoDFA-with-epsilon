from ReduceDFA import reduce_DFA

eps = 'e'

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

## epsilon-closure function
def ECLOSE(root_enfa_state: str):
    global eclose_dict

    if eclose_dict[root_enfa_state] != None:
        return eclose_dict[root_enfa_state]

    eclose = [root_enfa_state]

    if delta[root_enfa_state][eps] == []:
        eclose_dict[root_enfa_state] = eclose
        return eclose
    else:
        for enfa_state in delta[root_enfa_state][eps]:
            ECLOSE(enfa_state)
            eclose.extend(eclose_dict[enfa_state])
        eclose = sorted(list(set(eclose)))
        eclose_dict[root_enfa_state] = eclose
        return eclose_dict
        
## set epsilon-closure array None first
eclose_dict = {}
for enfa_state in Q:
  eclose_dict[enfa_state] = None

## get first state's epsilon-closure
dfa_states = [ECLOSE(q0)]

dfa_delta = []

new_dfa_states = [ECLOSE(q0)]

## after epsilon-closure, remove symbol epsilon
symbols.remove(eps)

## get DFA
while len(new_dfa_states) > 0:
    current_state = new_dfa_states[0]
    new_dfa_states = new_dfa_states[1:]

    for symbol in symbols:
        next_states = []
        for nfa_state in current_state:
            for x in delta[nfa_state][symbol]:
                if x not in next_states:
                    next_states.append(x)
        next_states = sorted(next_states)

        eclose_union = []
        for state in next_states:
            eclose_union.extend(ECLOSE(state))
        eclose_union = sorted(set(eclose_union))
        dfa_delta.append([current_state, symbol, eclose_union])

        if eclose_union not in dfa_states:
            dfa_states.append(eclose_union)
            new_dfa_states.append(eclose_union)

tmp = dfa_delta
dfa_delta = []

new_states = []

for_reduced_final = []
for_reduced_delta = []

## set values for reducing DFA
for v in tmp:
    if v not in dfa_delta:
        dfa_delta.append(v)
    if v[0] not in new_states:
        new_states.append(v[0])

for i in F:
    for j in new_states:
        if i in j and j:
            for_reduced_final.append(j)

for i in dfa_delta:
    if i[2]:
        for_reduced_delta.append([[i[0], i[1]], i[2]])

for i in new_states:
    if q0 in i:
        q0 = i
        break

## print
print("[ e-closure ]")
print("[[[current state, symbol], [next state]]")
for i in for_reduced_delta:
    print(i)

new_states, dfa_delta, for_reduced_final = reduce_DFA(new_states, symbols, for_reduced_delta, q0, for_reduced_final)
print("----------------------------------------")

print("[ reduced DFA ]")
print("[[[current state, symbol], [next state]]")
for i in for_reduced_delta:
    print(i)