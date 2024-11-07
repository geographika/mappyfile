"""
python -m timeit -n 10 -s "import mappyfile" "mappyfile.open(r'tests/mapfiles/large_map1.map')"

With lark_cython:
    10 loops, best of 5: 245 msec per loop

With lark:
    10 loops, best of 5: 274 msec per loop

"""

import timeit

N = 100

t = timeit.timeit(
    stmt="mappyfile.open(mf)",
    setup="import mappyfile; mf=r'tests/mapfiles/large_map1.map'",
    number=N,
)

print(t / N)
