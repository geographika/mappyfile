import cProfile
import pstats
import glob
import os
import mappyfile


def parse(mf):
    m = mappyfile.open(mf, expand_includes=False)
    s = mappyfile.dumps(m)
    return s


def log_profile_output(pr, output_file):

    sortby = 'tottime'
    sortby = 'time'

    with open(output_file, "w") as f:
        ps = pstats.Stats(pr, stream=f).sort_stats(sortby)
        ps.print_stats()

    # pr.dump_stats(fn)
    # pr.print_stats(sort='time')


def profile(mf, test_name):

    pr = cProfile.Profile()
    pr.enable()
    parse(mf)
    pr.disable()
    output_file = os.path.join(os.path.dirname(__file__), "performance", test_name, "{}.txt".format(os.path.basename(mf)))
    log_profile_output(pr, output_file)


def profile_test():
    from tests.test_validation import test_version_warnings
    test_name = "test_version_warnings"
    pr = cProfile.Profile()
    pr.enable()
    test_version_warnings()
    pr.disable()
    output_file = os.path.join(os.path.dirname(__file__), "performance", "{}.txt".format(test_name))
    print(output_file)
    log_profile_output(pr, output_file)


def run(test_name):

    sample_dir = os.path.dirname(__file__)
    pth = sample_dir + '/*.map'
    mapfiles = glob.glob(pth)

    for fn in mapfiles:
        print(fn)
        profile(fn, test_name)


if __name__ == "__main__":
    test_name = "run3-py27"
    # run(test_name)
    profile_test()
    print("Done!")
