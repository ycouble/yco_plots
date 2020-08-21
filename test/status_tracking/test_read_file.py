import pytest

import status_tracking as st


EXAMPLE_TEST_STATUSES = """,Test1,Test2,Test3,Test4
2020-08-20,0,0,0,0
2020-08-21,0,1,0,0
2020-08-22,0,1,0,1
"""


@pytest.mark.parametrize(
    "content, nb_days, nb_tests",
    [(EXAMPLE_TEST_STATUSES, 3, 4), (None, 0, 0)],
    ids=["normal", "non_existant"],
)
def test_read_csv(tmpdir, content, nb_days, nb_tests):
    print(tmpdir)
    filename = tmpdir / "hello.txt"
    if content:
        filename.write_text(content, encoding="utf-8")
    status_df = st.read_status_file(filename)
    assert status_df.shape == (nb_days, nb_tests)
