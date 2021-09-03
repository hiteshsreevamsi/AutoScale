try:
    import unittest
    from app import app
except Exception as e:
    print("something went wrong")


class Unittest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        resp = tester.get("/")
        code = resp.status_code
        self.assertEqual(code, 200)


if __name__ == "__main__":
    unittest.main()
