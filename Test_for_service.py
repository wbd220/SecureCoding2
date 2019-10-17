import unittest
import requests
from bs4 import BeautifulSoup

server_address = "http://127.0.0.1:5000"
SERVICE_ADDR = server_address


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

    def test_register_account(self):
        reqdata = {"tester2": uname, "password": pword, "15553334444": 2fa}
        req = requests.post(server_address + "/register", data=reqdata)
        print(req)
        soup = BeautifulSoup(req.text, "html_parser")
        login_result=soup.find("result")
        print(login_result)
        self.assertEqual(login_result, "success")



if __name__ == '__main__':
    unittest.main()
