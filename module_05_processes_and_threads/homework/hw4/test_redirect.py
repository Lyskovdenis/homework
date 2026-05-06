import io
import unittest
from redirect import Redirect


class RedirectTestCase(unittest.TestCase):
    def test_redirect_both_streams(self):
        out = io.StringIO()
        err = io.StringIO()

        with Redirect(stdout=out, stderr=err):
            print("hello stdout")
            try:
                raise Exception("hello stderr")
            except Exception:
                import traceback
                traceback.print_exc()  # пишет в sys.stderr

        self.assertIn("hello stdout", out.getvalue())
        self.assertIn("hello stderr", err.getvalue())

    def test_redirect_only_stdout(self):
        out = io.StringIO()

        with Redirect(stdout=out):
            print("only stdout")

        self.assertIn("only stdout", out.getvalue())

    def test_redirect_only_stderr(self):
        err = io.StringIO()

        with Redirect(stderr=err):
            try:
                raise Exception("only stderr")
            except Exception:
                import traceback
                traceback.print_exc()

        self.assertIn("only stderr", err.getvalue())

    def test_nested_redirects(self):
        outer = io.StringIO()
        inner = io.StringIO()

        with Redirect(stdout=outer):
            print("outer 1")
            with Redirect(stdout=inner):
                print("inner")
            print("outer 2")

        self.assertIn("outer 1", outer.getvalue())
        self.assertIn("outer 2", outer.getvalue())
        self.assertIn("inner", inner.getvalue())


if __name__ == '__main__':
    unittest.main()