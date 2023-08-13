"""
Steps:

1. Create a new run folder
2. Run script as a command:

cd D:/GitHub/mappyfile
python ./tests/mapfiles/profiler.py run4-py310-cython
"""
import cProfile
import pstats
import glob
import os
import mappyfile
import sys


def parse(mf):
    m = mappyfile.open(mf, expand_includes=False)
    mappyfile.validate(m)
    s = mappyfile.dumps(m)
    return s


def log_profile_output(pr, output_file):
    sortby = "tottime"
    sortby = "time"

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

    output_folder = os.path.join(os.path.dirname(__file__), "performance", test_name)

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    output_file = os.path.join(
        output_folder,
        "{}.txt".format(os.path.basename(mf)),
    )
    log_profile_output(pr, output_file)


def profile_test():
    from tests.test_validation import test_version_warnings

    test_name = "test_version_warnings"
    pr = cProfile.Profile()
    pr.enable()
    test_version_warnings()
    pr.disable()
    output_file = os.path.join(
        os.path.dirname(__file__), "performance", "{}.txt".format(test_name)
    )
    print(output_file)
    log_profile_output(pr, output_file)


def run(test_name):
    sample_dir = os.path.dirname(__file__)
    pth = sample_dir + "/*.map"
    mapfiles = glob.glob(pth)

    for fn in mapfiles:
        print(fn)
        profile(fn, test_name)


if __name__ == "__main__":
    # profile_test()

    # Check if any command-line arguments were provided
    if len(sys.argv) > 1:
        # Print the first command-line argument (excluding the script filename)
        test_name = sys.argv[1]
        run(test_name)
        print(f"Results output to {test_name} - done!")
    else:
        print("No command-line arguments provided.")
