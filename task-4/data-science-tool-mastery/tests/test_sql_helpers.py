import sqlite3
import unittest

import pandas as pd

from dstoolkit import df_to_sqlite, explain, run_query


class TestSqlHelpers(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.df = pd.DataFrame({"name": ["a", "b", "c"], "score": [1.5, 2.5, 3.5]})
        df_to_sqlite(self.df, "t", self.conn)

    def tearDown(self):
        self.conn.close()

    def test_round_trip(self):
        out = run_query(self.conn, "SELECT * FROM t ORDER BY score")
        pd.testing.assert_frame_equal(out, self.df)

    def test_row_count_returned(self):
        self.assertEqual(df_to_sqlite(self.df, "t2", self.conn), 3)

    def test_parameter_binding_blocks_injection(self):
        evil = "a'; DROP TABLE t; --"
        out = run_query(self.conn, "SELECT * FROM t WHERE name = ?", (evil,))
        self.assertEqual(len(out), 0)
        self.assertEqual(len(run_query(self.conn, "SELECT * FROM t")), 3)    # the table still exists

    def test_index_changes_query_plan_from_scan_to_search(self):
        sql = "SELECT * FROM t WHERE name = ?"
        self.assertTrue(any("SCAN" in step for step in explain(self.conn, sql, ("a",))))
        self.conn.execute("CREATE INDEX idx_name ON t(name)")
        self.assertTrue(any("SEARCH" in step and "idx_name" in step for step in explain(self.conn, sql, ("a",))))

    def test_bad_sql_raises(self):
        with self.assertRaises(Exception):
            run_query(self.conn, "SELEC nothing")


if __name__ == "__main__":
    unittest.main()
