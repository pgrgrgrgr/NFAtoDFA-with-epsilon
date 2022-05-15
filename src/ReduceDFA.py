def reduce_DFA(states, symbols, delta, start, final):
  ## change diffrent types of automata arguments to integer

  ## set state to int
  n_state = []
  for i in states:
    n_state += [states.index(i)]
  
  ## set delta to int
  n_delta = []
  for k in delta:
    n_delta += [[[states.index(k[0][0]), k[0][1]], states.index(k[1])]]

  ## set start to int
  n_start = states.index(start)
  
  ## set final to int
  n_final = []
  for t in final:
      n_final += [states.index(t)]

  n_final = list(set(n_final))

  ## reset for reducing
  states = n_state
  delta = n_delta
  start = n_start
  final = n_final 
 
  ## reducing process
  m_state = []
  for i in states:
    m_state += [{i}]
  t_state = []

  m_symbol = symbols
  m_trans = []
  m_start = start
  m_final = []

  ## the list for partition for final state, equivalnce class, no more partition
  to_iden_list = []

  num_state = len(states)
  for i in range(0, num_state):
    for j in range(i+1, num_state):
        to_iden_list += [[{i, j}, 0]]

  ## set element 1 which have final state
  for k in final:
      for i in to_iden_list:
          if k in i[0]:
              i[1] = 1
  ## set element 0 final states each other
  for i in to_iden_list:
      if i[0] - set(final) == set():
          i[1] = 0

  ## set element 1 equivalnce relations
  for k in range(0, len(to_iden_list)):
      for s in symbols:
          for i in range(0, len(to_iden_list)):
              s_set = set()
              count = 0
              temp = to_iden_list[i][0]
              temp = list(temp)
              if to_iden_list[i][1] == 0:
                  for f in delta:
                      if f[0][0] == temp[0] and f[0][1] == s:
                          s_set.add(f[1])
                          count += 1
                      elif f[0][0] == temp[1] and f[0][1] == s:
                          s_set.add(f[1])
                          count += 1
                  if len(s_set) == 2:
                      for t in to_iden_list:
                          if s_set == t[0] and t[1] == 1:
                              to_iden_list[i][1] = 1
                  elif count == 1:
                      to_iden_list[i][1] = 1

  t_flag = False

  ## restruct equivalance states
  for i in to_iden_list:
      if i[1] == 0:
          t_state = []
          for k in m_state:
              if (i[0] & k) != set():
                  if t_flag:
                      continue
                  else:
                      t_state += [(i[0] | k)]
                      t_flag = True
              else:
                  t_state += [k]
          m_state = t_state
          t_flag = False

  for i in range(0, len(m_state)):
      m_state[i] = list(m_state[i])
      m_state[i].sort

  ## restruct delta funcions for minimized states
  for i in m_state:
      for f in delta:
          if f[0][0] == i[0]:
              for t in m_state:
                  try:
                      t.index(f[1])
                  except ValueError:
                      continue
                  else:
                      m_trans += [[[i, f[0][1]], t]]

  ## restruct final state
  for i in m_state:
      for k in final:
          try:
              i.index(k)
          except ValueError:
              continue
          else:
              m_final += [i]

  ## restruct start state 
  for i in m_state:
      try:
          i.index(start)
      except ValueError:
          continue
      else:
          m_start = i
  
  return(m_state, m_trans, m_final)