"""
python -m timeit "import mappyfile; mappyfile.open(r'D:\GitHub\mappyfile\tests\mapfiles\large_map1.map')"

With lark_cython:

    1 loop, best of 5: 322 msec per loop

With lark:

    1 loop, best of 5: 373 msec per loop

"""
import timeit
import mappyfile

t = timeit.timeit(stmt="mappyfile.open(mf)",
setup="import mappyfile; mf=r'D:/GitHub/mappyfile/tests/mapfiles/large_map1.map'", number=10)

# 34.8 s with lark_cython
# 38.5 without
print(t)


