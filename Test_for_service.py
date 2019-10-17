import unittest
import requests
from bs4 import BeautifulSoup

server_address = "http://127.0.0.1:5000"


class FeatureTest(unittest.TestCase):

    def test_home_page_check(self):
        req = requests.get(server_address)
        self.assertEqual(req.status_code, 200)
        print("testing to see if there is a default page")

    def test_login_page_check(self):
        req = requests.get(server_address + "/login")
        self.assertEqual(req.status_code, 200)
        print("testing to see if /login page is there")

    def test_register_page_check(self):
        req = requests.get(server_address + "/register")
        self.assertEqual(req.status_code, 200)
        print("testing to see if /register page is there")

    def test_register_account(self, session=None):
        login_result = None
        if session is None:
            session = requests.Session()
        reqdata = {"uname": "tester2", "pword": "password", "2fa": "15553334444"}
        req = session.post(server_address + "/register", data=reqdata)
        print("your request came back with", req)
        soup = BeautifulSoup(req.text, features="html.parser")
        login_result = soup.find("success")
        print("login_result is", login_result)
        # assert login_result is not None
        self.assertEqual(login_result, "success")


if __name__ == '__main__':
    unittest.main()
