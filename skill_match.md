Known skill matching
====================

Notation Conventions
----------

* s1, s2, ... State from measure.
* 1, 2, ...   Atom skill.
* A, B, ...   Combine skill.

Level 1: Mapping pre/post of the Ops of a known skill to states queue.
----------

From here on, we talk about `Layer 3` of our framework.

The known skill `A` using Skill Primitive queue:

A:8->5->3->4->9

Now we trying to mapping its pre/post to a states queue:

s0->s1->s2->s3->s4->s5

Result to see Chapter 5 [Table 2](http://localhost:8000/c5.py)


Level 2: Liner matching states queue to then known skill.
----------

Atom Sk.|Type| List of St_id |Diff Above |len(set)
--------|----|---------------|-----------|--------
~       |post| Universal Set |           |
8       |pre | [s0,s1]       | [s0,s1]   | 2
8       |post| [s1,s2,s3]    |           |
5       |pre | [s0,s1]       | [s1]      | 1
5       |post| [s2,s3,s4,s5] |           |
3       |pre | [s2,s3]       | [s2,s3]   | 2
3       |post| [s3]          |           |
4       |pre | [s3]          | [s3]      | 1
4       |post| [s4]          |           |
9       |pre | [s4]          | [s4]      | 1
9       |post| [s5]          |           |
~       |pre | Universal Set | [s5]      | 1

Total Conditions: 2*1*2*1*1*1=4

Following A, B, C are totally different combine skill!

Here, `[s0,s1]` is the initialize state set.

```
A:8->5->3->4->9
B:8->3->4->9
C:8->5->6->3->4->9
```

Then we try to see if the queue of states,

...->s0->s1->s2->s3->s4->s5->s6->s7->s8->s9->s10->....

matching following combine skill `A`,

```
A:8->5->3->4->9
```

```
Algorithm 2:
INIT SET=[s0,s1]
FINISH SET=[9]

START
s0(<8>) s1(<5>) s2(<3>) s3(<4>) s4(<9>) s5(<9>) OK
s1(<8>) s2(5)->STOP for s2 not in set [1]
END
```

Note 1: We define 2(5) as "if 2 in ADS(5)?". Witch means check if 2 in diff set between Current Op. Atom's pre and its father's post. In this case, that is the set diff of [1,2,3] (post of 8) and [0,1]  (pre of 5), that is [1]. Because 2 not in [1], STOP.

Note 2: In the same way, 2(<5>,3,6) means "if 2 in ADS(5)?" or "if 2 in ADS(3)?" or "if 2 in ADS(6)?". If some of the answers is true, we can choose one of it, with is marked with <>. If neither of answer is true, STOP.


Level 3: Spread to Tree.
----------

```
D:8->5->3->4->9
     |->6
     |->7->2
        |->6
```

...->s0->s1->s2->s3->s4->s5->s6->s7->s8->s9->s10->....

```
Algorithm 3:

INIT SET=[s0,s1]
FINISH SET=[9,2,6]

START
s0(<8>) s1(<5>) s2(<3>,6,7) s3(4,6,<7>) s4(4,6,2,6) ...
s1(8) s2(5) s3(3,6,7) ...
END
```

Level 3+: Spread to DAG (Directed acyclic graph).
----------

等价于Level 3,

```
D:8->5->3->4->9
     |---------
     |->7->2  |
        |------->6
```

Level 4: Spread to DAG with list-nodes.
----------

```
E:[8]->[5,2]->[3]->[4,1]->[9]
        |-------------
        |->[7]->[2]  |
            |----------->[6,3]
```

...->s0->s1->s2->s3->s4->s5->s6->s7->s8->s9->s10->....

```
Algorithm 4:

INIT SET=[s0,s1]
FINISH SET=[9,2,6,3]

START
s0(<8>) s1(<5>,2) s2(<3>,7,6,3) s3(4,1,<7>) s4(<4>,1,2) s5(9,2)...
s1(8) s2(5) s3(3,6,7) ...
END
```

Note 3: [5,2] means we can chose any one in [5,2] to satisfy the whole node.

Note 4: in `2(<3>,7,6,3)`, [3] finished, so [4,1] added, [7] remain. **[6,3]** has two fathers, namely [5,2] and [7]. Because 3 has been chosen, node [6,3] has been totally satisfied. So next round remains question 3(4,1,7).


Level 5: Match sub-skill of a known combine skill.
----------

```
E:[8]->[5,2]->[3]->[4,1]->[9]
        |-------------
        |->[7]->[2]  |
            |----------->[6,3]
```

For combine skill `E`, any non-end node of the DAG can be look on as a sub-skill. Of cause, a end node must be any one of a `Skill Primitive`, a atom in the alternate list.

...->s0->s1->s2->s3->s4->s5->s6->s7->s8->s9->s10->....

```
Algorithm 5:

START
for root in `root list` of DAG:
    for node in all non-end node in the children of root:
        INIT SET=ADS(node)
        FINISH SET=Leaf(ADS(node))

        if <Algorithm 5> returns OK, current node till all its leafs combines a new sub-skill, and this sub-skill satisfies the states queue.
            Out put the match.
            Ignore all children of the node and continue.
END
```

Note 5: Leaf(set) means for each item in `set`, find its all leafs and calculate the union.

Note 6: `root list` here is [8].


Level 6: Matching probability model
----------

In the real world, rarely have the opportunity to match a large combine skill, because there always some little, not important differences between a states queue and a large combine skill. Apply probability model, we can accept those very mush similar but not EXACTLY EQUAL ones.

```
Probability = Covered Nodes / Total Nodes
```

For example, in following case, a given states queue `SQ` can not match the combine skill `F` exactly.

```
F:[8]->[5,2]->[3]->[4,1]->[9]
        |-------------
        |->[7]->[2]  |
            |----------->[6,3]
```

Then, we try to calculate the matching probability of `F`. With <Algorithm 5> `SQ` matching following sub-skills of `F`,

```
G:[3]->[4,1]->[9]
H:[7]->[2]
   |----------->[6,3]
```

So the matching probability of `F` is,

```
Probability = Length(Union(G, H)) / Length(F) = 6 / 8 = 0.75
```

That means over 70% of probability that `SQ` matching with `F`, we may accept this matching. Or not, that depends on what threshold value you choose.


Level 7: Add atom skill from scratch
----------

From very small amount of simple pre-defined atom skills, we can built a method to allow robots abstract new skills from observe (states queues of above) and induction (calculate sub-skills with highly matching probability, see `Level 6`). That's not enough. Robots also need to know how to add new skill as atom skills as well. Next step (`Level 9`), we can remove all the `known skills` from human being and let robot build its brain from zero.

TODO: Add atom skill from scratch.


Level 8: Total skill matching
----------

From here on, we talk about `Layer 4` of our framework.

Whatever in the single brain of robot or in the whole world of robots that connects together (ie. SNS-Robot), there's lots of skills for searching and matching again and again. How to find out the matching skill with highly probability in most efficiency way? [Level 5](#Level 5) tell us a skill can be look as sub-skill of some other skill. In the other way, All the skills can be look as sub-skill of one huge skill.

The goodness of using one huge skill instead of lots of single ones is obversely about efficiency. Reappear parts  are ignored and optional operations are combine in the node list, that makes the total skills size much smaller and then makes search and match much faster.


Level 9: Matching probability model improved with ANN
----------

With Artificial Neural Networks (ANN), we built a matching evaluation network. This much improved the [Matching probability model](Level 5).


Level 10: Hidden Markov Model (HMM)
----------

