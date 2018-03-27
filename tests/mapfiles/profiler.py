import sys
import cProfile
import pstats
import glob
import os
import tempfile
import mappyfile


PY2 = sys.version_info[0] < 3


def parse(mf):
    m = mappyfile.open(mf, expand_includes=False)
    s = mappyfile.dumps(m)

    # if PY2:
    #     s = mappyfile.dumps(m)
    #     f = tempfile.NamedTemporaryFile(delete=False)
    #     f.write(s.encode("utf-8"))
    # else:
    #     f = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
    #     mappyfile.dump(m, f)
      
    # f.close()


def profile(mf, test_name):
    sortby = 'time'

    pr = cProfile.Profile()
    pr.enable()
    parse(mf)
    pr.disable()

    fn = os.path.join(os.path.dirname(__file__), "performance", test_name, "{}.txt".format(os.path.basename(mf)))

    with open(fn, "w") as f:
        ps = pstats.Stats(pr, stream=f).sort_stats(sortby)
        ps.print_stats()


    # pr.dump_stats(fn)
    # pr.print_stats(sort='time')

def run(test_name):

    sample_dir = os.path.dirname(__file__)
    pth = sample_dir + '/*.map'
    mapfiles = glob.glob(pth)

    for fn in mapfiles:
        print(fn)
        profile(fn, test_name)


if __name__ == "__main__":
    test_name = "run2-py37"
    run(test_name)
    print("Done!")
