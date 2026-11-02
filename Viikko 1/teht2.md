BFS:

Start with a, add b to queue:

[b]
[c, f]
[f, e, i]
[e, i, d, g]
[i ,d, g]
[d, g]
[g]
[h]

DFS:

Start with a, add b to stack:

[b]
[f, c]
[g, d, c]
[h, d, c]
[h] <- first in last stack, so found