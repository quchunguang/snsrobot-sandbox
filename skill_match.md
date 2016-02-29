Known skill matching
====================

Question 1: Mapping pre/post of the Ops of a known skill to states queue.
----------

The known skill `A` using Skill Primitive queue:

A:8->5->3->4->9

Now we trying to mapping its pre/post to a states queue:

0->1->2->3->4->5

Result to see Chapter 5 [Table 2](http://localhost:8000/c5.py)


Question 2: Liner matching states queue to then known skill.
----------

Op. Atom|Type|List of St_id |Diff Set |len(set)
--------|----|--------------|---------|--------
8       |pre |[0,1]         |  [0,1]  | 2
8       |post|[1,2,3]       |         |
5       |pre |[0,1]         |  [1]    | 1
5       |post|[2,3,4,5]     |         |
3       |pre |[2,3]         |  [2,3]  | 2
3       |post|[3]           |         |
4       |pre |[3]           |  [3]    | 1
4       |post|[4]           |         |
9       |pre |[4]           |  [4]    | 1
9       |post|[5]           |  [5]    | 1

Total Conditions: 2*1*2*1*1*1=4

Following A, B, C are totally different combine skill!

```
A:8->5->3->4->9
B:8->3->4->9
C:8->5->6->3->4->9
```

Then we try to see if the queue of states,

...->0->1->2->3->4->5->6->7->8->9->10->....

matching following combine skill `A`,

```
A:8->5->3->4->9
```

```
Algorithm 2:
INIT SET=[0,1]
FINISH SET=[9]

START
0(<8>) 1(<5>) 2(<3>) 3(<4>) 4(<9>) 5(<9>) OK
1(<8>) 2(5)->STOP for 2 not in set [1]
END
```

Note 1: We define 2(5) as "if 2 in ADS(5)?". Witch means check if 2 in diff set between Current Op. Atom's pre and its father's post. In this case, that is the set diff of [1,2,3] (post of 8) and [0,1]  (pre of 5), that is [1]. Because 2 not in [1], STOP.

Note 2: In the same way, 2(<5>,3,6) means "if 2 in ADS(5)?" or "if 2 in ADS(3)?" or "if 2 in ADS(6)?". If some of the answers is true, we can choose one of it, with is marked with <>. If neither of answer is true, STOP.


Question 3: Spread to Tree.
----------

```
D:8->5->3->4->9
     |->6
     |->7->2
        |->6
```

...->0->1->2->3->4->5->6->7->8->9->10->....

```
Algorithm 3:

INIT SET=[0,1]
FINISH SET=[9,2,6]

START
0(<8>) 1(<5>) 2(<3>,6,7) 3(4,6,<7>) 4(4,6,2,6) ...
1(8) 2(5) 3(3,6,7) ...
END
```

Question 3+: Spread to DAG (Directed acyclic graph).
----------

等价于Question 3,

```
E:8->5->3->4->9
     |---------
     |->7->2  |
        |------->6
```

Question 4: Spread to DAG with list-nodes.
----------

```
E:[8]->[5,2]->[3]->[4,1]->[9]
        |-------------
        |->[7]->[2]  |
            |----------->[6,3]
```

...->0->1->2->3->4->5->6->7->8->9->10->....

```
Algorithm 4:

INIT SET=[0,1]
FINISH SET=[9,2,6,3]

START
0(8) 1(<5>,2) 2(<3>,7,6,3) 3(4,1,<7>) 4(<4>,1,6,2) 5(9,6,2)...
1(8) 2(5) 3(3,6,7) ...
END
```

Note 3: [5,2] means we can chose any one in [5,2] to satisfy the whole node.

Note 4: in `2(<3>,7,6,3)`, [3] finished, so [4,1] added, [7] remain. **[6,3]** has two father [5,2] and [7]. Because 3 is choosing, node [6,3] totally satisfied. So next round remains question 3(4,1,7).


Question 5: Match sub-skill of a known combine skill.
----------

```
E:[8]->[5,2]->[3]->[4,1]->[9]
        |-------------
        |->[7]->[2]  |
            |----------->[6,3]
```

For combine skill `E`, any non-end node of the DAG can be look on as a sub-skill. Of cause, a end node must be any one of a `Skill Primitive`, a atom in the alternate list.

...->0->1->2->3->4->5->6->7->8->9->10->....

```
Algorithm 5:

START
for root in the set of root node of DAG:
    for node in all non-end node in the children of root:
        INIT SET=ADS(node)
        FINISH SET=Leaf(ADS(node))

        if <Algorithm 5> returns OK, current node till all its leafs combines a new sub-skill, and this sub-skill satisfies the states queue.
            Out put the match.
            Ignore all children of the node and continue.
END
```

Note 5: Leaf(set) means for each item in `set`, find its all leafs and calculate the union.

Note 6: `root set` here is [8].


Question 6: Probability model matching
----------

In real world, rarely have the opportunity to match a large combine skill, because there always some little, not important differences between a states queue and a large combine skill. Apply probability model, we can accept those very mush similar but not EXACTLY EQUAL ones.

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

Then, we try to calculate the matching probability of `F`. we matched following sub-skills of `F`,

```
G:[3]->[4,1]->[9]
H:[7]->[2]
   |----------->[6,3]
```

So the matching probability of `F` is,

```
Probability = Length(Union(G, H)) / Length(f) = 6 / 8 = 0.75
```

That means over 70% of probability that `SQ` matching with `F`, we may accept this matching. Or not, that depends on what threshold value you choose.
