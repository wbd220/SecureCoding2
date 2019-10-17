import unittest
import requests

server_address = "http://127.0.0.1:5000"
SERVICE_ADDR = server_address


class FeatureTest(unittest.TestCase):

    def home_page_check(self):
        req = requests.get(server_address)
        self.assertEqual(req.status_code, 200)
        print("testing to see if there is a default page")

    def login_page_check(self):
        req = requests.get(server_address + "/login")
        self.assertEqual(req.status_code, 200)
        print("testing to see if /login page is there")

    def register_page_check(self):
        req = requests.get(server_address + "/register")
        self.assertEqual(req.status_code, 200)
        print("testing to see if /register page is there")
