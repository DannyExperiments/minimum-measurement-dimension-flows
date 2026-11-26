from fractions import Fraction as F
from itertools import combinations, product
from random import Random

def fixture(n, clauses):
    m=len(clauses)
    B=n+2*m
    eta=F(1,2)
    E={}
    def add(u,v,d=1,scarce=False):
        E[u,v]=(F(d), B+1 if scarce else 1)
    for i in range(1,n+1):
        for b in (0,1):
            add(('v',i-1),('x',i,b))
            add(('x',i,b),('v',i))
    r=(('v',n),('c',0))
    add(*r)
    for j,C in enumerate(clauses,1):
        for k,(i,b) in enumerate(C):
            y=('lit',j,k)
            add(('c',j-1),y)
            add(y,('c',j))
            add(('x',i,1-b),y,2*(n-i+j),True)
    adj={}
    for u,v in E:
        adj.setdefault(u,[]).append(v)
    def paths(u):
        if u==('c',m):
            yield ()
        for v in adj.get(u,()):
            for t in paths(v):
                yield ((u,v),)+t
    P=list(paths(('v',0)))
    bypass=[p for p in P if r not in p]
    use_r=[p for p in P if r in p]
    for p in P:
        assert sum(E[e][0] for e in p)==2*n+2*m+(r in p)
    h=(1-eta)/(B+1)
    sats=[p for p in use_r if not any(e[0] in {i[1] for i in p} and e[1] in {i[1] for i in p}
                                           for e in E if E[e][1]>1)]
    if sats:
        p=sats[0]
        marked={e for e in E if (e[0][0]=='v' and e[1][0]=='x' or e[0][0]=='lit' and e[1][0]=='c') and e not in p}
        assert len(marked)==B
        rho=min(eta/(8*len(p)),eta/(8*sum(k for _,k in E.values())))
        w={e:rho+(1+eta/(4*B) if e in marked else 0) for e in E}
        assert 0<sum(E[e][1]*w[e] for e in E)<B+eta
        def val(p): return sum(E[e][0]+w[e] for e in p)
        assert val(p)<min(map(val,bypass))
    else:
        for p in use_r:
            vertices=[p[0][0]]+[e[1] for e in p]
            shortcut=next(e for e in E if E[e][1]>1 and e[0] in vertices and e[1] in vertices)
            i,j=map(vertices.index,shortcut)
            q=p[:i]+(shortcut,)+p[j:]
            assert q in bypass
            assert 1-(B+eta)/E[shortcut][1]==h
    sat=any(all(any(bits[i-1]==b for i,b in C) for C in clauses) for bits in product((0,1),repeat=n))
    assert bool(sats)==sat
    return sat

# Worked two-node fixture. Coordinates are (u, f1, f2, bypass, slack).
# The two equations are u+f1+f2+bypass=1 and u+slack=1/2.
def worked_vertices():
    columns = [(1, 1), (1, 0), (1, 0), (1, 0), (0, 1)]
    vertices = set()
    for i, j in combinations(range(len(columns)), 2):
        a, b = columns[i]
        c, d = columns[j]
        det = a * d - b * c
        if det == 0:
            continue
        vertex = [F(0)] * len(columns)
        vertex[i] = (d - c * F(1, 2)) / det
        vertex[j] = (a * F(1, 2) - b) / det
        if min(vertex) >= 0:
            assert sum(x > 0 for x in vertex) == 2
            vertices.add(tuple(vertex))
    assert len(vertices) == 6
    return vertices


def optima(vertices, cost):
    values = {x: sum(a * b for a, b in zip(x, cost)) for x in vertices}
    minimum = min(values.values())
    return {x for x in values if values[x] == minimum}


def replay_worked_flow():
    vertices = worked_vertices()
    run_1 = (F(1, 2), F(1, 2), F(0), F(0), F(0))
    run_2 = (F(1, 2), F(0), F(1, 2), F(0), F(0))
    bypass = (F(0), F(0), F(0), F(1), F(1, 2))
    assert optima(vertices, (1, 2, 2, 3, 0)) == {run_1, run_2}
    assert optima(vertices, (1, 2, F(5, 2), 3, 0)) == {run_1}
    assert optima(vertices, (1, F(5, 2), 2, 3, 0)) == {run_2}
    assert optima(vertices, (1, 2, 2, F(1, 2), 0)) == {bypass}
    assert tuple(a - b for a, b in zip(run_1, run_2)) == (0, F(1, 2), -F(1, 2), 0, 0)
    print("Worked flow: 6 nondegenerate vertices; tied/ordered/bypass optima checked exactly.")


def main():
    rng=Random(438)
    yes=no=0
    for _ in range(80):
        n=rng.randint(1,3)
        clauses=[tuple((rng.randint(1,n),rng.randrange(2)) for _ in range(3))
                 for __ in range(rng.randint(1,5))]
        ans=fixture(n,clauses)
        yes+=ans
        no+=not ans
    assert yes and no
    eps=[F(1,4**(i+2)) for i in range(8)]
    vals=[-1,F(1,2)]+[-e for e in eps]
    for k in product((-1,0,1),repeat=len(vals)):
        assert not any(k) or sum(x*y for x,y in zip(k,vals))
    print(f"Passed {yes} SAT + {no} UNSAT exact path fixtures and {3**len(vals)-1} nonzero RHS sign patterns")
    replay_worked_flow()


if __name__ == "__main__":
    main()
