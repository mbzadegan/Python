# (0, 4, 7, 5, 2, 6, 1, 3) means:
# queens at (row,column) positions (0,0), (1,4), (2,7), ....
# The trick is rather elegant. Because permutations(range(8)) already guarantees one queen per row and one per column, we only have to check the two diagonals.

from itertools import permutations
print(*[p for p in permutations(range(8)) if len({p[i]-i for i in range(8)})==len({p[i]+i for i in range(8)})==8],sep="\n")
