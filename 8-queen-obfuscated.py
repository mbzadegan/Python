from itertools import permutations
print(*[p for p in permutations(range(8)) if len({p[i]-i for i in range(8)})==len({p[i]+i for i in range(8)})==8],sep="\n")
