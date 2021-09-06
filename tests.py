try:
    import unittest
    from app import app
except Exception as e:
    print("something went wrong")


class Unittest(unittest.TestCase):

    # ensure that flask app was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        resp = tester.get("/")
        code = resp.status_code
        self.assertEqual(code, 200)

    # Check whether the search page is loading correctly
    def test_default_page(self):
        tester = app.test_client(self)
        resp = tester.get("/", content_type='html/text')
        self.assertTrue(b'Zipcode to search...' in resp.data)

    # Check whether the search page data is loading correctly
    def test_search_operation(self):
        tester = app.test_client(self)
        resp = tester.post("/", data=dict(search_query="01832", radius=50),
                           content_type='multipart/form-data', follow_redirects=True)
        self.assertTrue(b'Results' in resp.data)
        self.assertEqual(resp.status_code, 200)

    # Check for format of data
    def test_search_operation_wrong_data(self):
        tester = app.test_client(self)
        resp = tester.post("/", data=dict(search_query="01832", radius=50),
                           content_type='html/text', follow_redirects=True)
        self.assertEqual(resp.status_code, 400)

    # Check for wrong zipcode
    def test_search_operation_wrong_zipcode(self):
        tester = app.test_client(self)
        resp = tester.post("/", data=dict(search_query="12345", radius=50),
                           content_type='multipart/form-data', follow_redirects=True)
        self.assertFalse(b'Results' in resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Zip code not found!' in resp.data)

    # Check with empty distance/radius
    def test_search_operation_empty_radius(self):
        tester = app.test_client(self)
        resp = tester.post("/", data=dict(search_query="12345"),
                           content_type='multipart/form-data', follow_redirects=True)
        self.assertFalse(b'Results' in resp.data)
        self.assertEqual(resp.status_code, 400)

    # Check with empty zipcode
    def test_search_operation_empty_zipcode(self):
        tester = app.test_client(self)
        resp = tester.post("/", data=dict(radius=100),
                           content_type='multipart/form-data', follow_redirects=True)
        self.assertFalse(b'Results' in resp.data)
        self.assertEqual(resp.status_code, 400)


if __name__ == "__main__":
    unittest.main()
