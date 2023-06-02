import logging
import pytest
from misc.docs_parser import clean_term, get_values


def check_key_values(s, exp_key, exp_v):
    key, values = clean_term(s)

    try:
        assert key == exp_key
    except AssertionError:
        logging.info(key)
        logging.info(exp_key)
        raise

    check_values(s, exp_v)


def check_values(s, exp_v):
    values = get_values(s)

    try:
        assert values == exp_v
    except AssertionError:
        logging.info(values)
        logging.info(values)
        raise


def test_list():
    s = "TYPE [chart|circle|line|point|polygon|raster|query]"
    check_key_values(
        s, "type", ["chart", "circle", "line", "point", "polygon", "raster", "query"]
    )


def test_atts1():
    s = "[DD|DDMM|DDMMSS|C format string]"
    check_values(s, ["dd", "ddmm", "ddmmss", "c format string"])


def test_atts2():
    s = " [r] [g] [b] | [hexadecimal string]"
    check_values(s, ["r", "g", "b", "hexadecimal string"])


def test_atts3():
    s = "[r] [g] [b] | [hexadecimal string] | [attribute]"
    check_values(s, ["r", "g", "b", "hexadecimal string", "attribute"])


@pytest.mark.xfail
def test_template():
    s = ":ref:`TEMPLATE <template>` [filename]"
    check_key_values(s, "template", ["filename"])


def test_size():
    s = "SIZE [integer]"
    check_key_values(s, "size", ["integer"])


def test_debug():
    s = "DEBUG [on|off]"
    check_key_values(s, "debug", ["on", "off"])


def test_bgcolor():
    s = "BACKGROUNDCOLOR [r] [g] [b] - `deprecated`"
    check_key_values(s, "backgroundcolor", ["r", "g", "b"])


def run_tests():
    pytest.main(["misc/test_docs_parser.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_tests()
    print("Done!")
