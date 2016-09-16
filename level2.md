Common
------

Let A = {a1, a2, ...} as the set of atom skills, witch is the basic operations that cannot be separated. we thought the skill set K = {k1, k2, ...} = A* is the set of any permutation of some of atom skills. Let S = {s1, s2, ...} as the full set of the concrete measure states.

The problem is how to abstract, pattern, class, search and match q in S* to a skill in K.

Level 2
-------

On this level, We store the skills one by one separately.

For example, we try to see if the queue of states,

...->s0->s1->s2->s3->s4->s5->s6->s7->s8->s9->s10->...

can match the skill k,

k = a8->a5->a3->a4->a9.

Algorithm 2

INIT STATES
  Si = {Diff_Above(I U a1)}

FINISH CONDTION
  Ai = {an}

BEBIN
func match_atom(a, s0, s):
    if a.pre in s0 and a.post in s:
        return true
    else:
        return false


s0 = Si[0]
for s in Si[1:]:
    for a in k:
        if not match_atom(a, s0, s1):
            break
        s = s0
    else:
        print "match found ({}, {})" % s,a
END
