import pytest
import logging
from mappyfile.quoter import Quoter


def test_standardise_quotes():
    v = '"the_geom from (select * from road where "name_e"=\'Trans-Canada Highway\' order by gid) as foo using unique gid using srid=3978"'

    q = Quoter(quote='"')
    v2 = q.standardise_quotes(v)
    exp = r'''"the_geom from (select * from road where \"name_e\"='Trans-Canada Highway' order by gid) as foo using unique gid using srid=3978"'''
    assert v2 == exp

    q = Quoter(quote="'")
    v2 = q.standardise_quotes(v)
    exp = r"""'the_geom from (select * from road where "name_e"=\'Trans-Canada Highway\' order by gid) as foo using unique gid using srid=3978'"""
    assert v2 == exp


def run_tests():
    pytest.main(["tests/test_quoter.py"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_standardise_quotes()
    # run_tests()
    print("Done!")
