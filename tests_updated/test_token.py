import utils
import requests

root_url = utils.root_url
import unittest

class TestTokenEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_random_user()
        pass

    def test_token_correct_username_password_yields_token(self):
        url = '{0}/api/token'.format(root_url)
        data = {
            'username': self.current_user.get('username'),
            'password': self.current_user.get('password_plaintext')
        }
        response = requests.post(url, json=data)
        data = response.json()
        # print(data)
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        
        # print(len(data.get('access_token')), len(data.get('refresh_token')))
        # testing for length kind of a weak test, but...
        self.assertTrue(len(access_token) > 300) 
        self.assertEqual(len(refresh_token), len(access_token) + 1)
        self.assertTrue(response.status_code, 200)

    def test_access_token_valid(self):
        url = '{0}/api/token'.format(root_url)
        data = {
            'username': self.current_user.get('username'),
            'password': self.current_user.get('password_plaintext')
        }
        response = requests.post(url, json=data)
        data = response.json()
        access_token = data.get('access_token')
        
        # Now use the token to access protected resource:
        url = '{0}/'.format(root_url)
        response = requests.get(url, headers={
            'Authorization': 'Bearer ' + access_token
        })

        # if the url was redirected to the login page, then the token
        # is invalid. If the not redirected, then token works.
        # This test assumes that you've already implemented security
        # for the landing page:
        self.assertEqual(response.url, url)
        self.assertTrue(response.status_code, 200)

    def test_token_bad_username_yields_error(self):
        url = '{0}/api/token'.format(root_url)
        data = {
            'username': 'dummy',
            'password': self.current_user.get('password_plaintext')
        }
        response = requests.post(url, json=data)
        # print(response.text)
        self.assertEqual(response.status_code, 401)

    def test_token_bad_password_yields_error(self):
        url = '{0}/api/token'.format(root_url)
        data = {
            'username': self.current_user.get('username'),
            'password': 'dummy'
        }
        response = requests.post(url, json=data)
        # print(response.text)
        self.assertEqual(response.status_code, 401)

class TestRefreshTokenEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_random_user()
        pass

    def test_refresh_token_valid_refresh_yields_access_token(self):
        url = '{0}/api/token/refresh'.format(root_url)
        refresh_token = utils.get_refresh_token(self.current_user.get('id'))
        data = {
            'refresh_token': refresh_token
        }
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # print(data)
        access_token = data.get('access_token')
        
        # print(len(data.get('access_token')), len(data.get('refresh_token')))
        # testing for length kind of a weak test, but...
        self.assertTrue(len(access_token) > 300) 
        self.assertEqual(len(refresh_token), len(access_token) + 1)


    def test_access_token_from_refresh_endpoint_is_valid(self):
        url = '{0}/api/token/refresh'.format(root_url)
        refresh_token = utils.get_refresh_token(self.current_user.get('id'))
        data = {
            'refresh_token': refresh_token
        }
        response = requests.post(url, json=data)
        data = response.json()
        # print(data)
        access_token = data.get('access_token')
        
        # Now use the token to access protected resource:
        url = '{0}/'.format(root_url)
        response = requests.get(url, headers={
            'Authorization': 'Bearer ' + access_token
        })

        # if the url was redirected to the login page, then the token
        # is invalid. If the not redirected, then token works.
        # This test assumes that you've already implemented security
        # for the landing page:
        self.assertEqual(response.url, url)
        self.assertTrue(response.status_code, 200)

    def test_bad_refresh_token_yields_error(self):
        url = '{0}/api/token/refresh'.format(root_url)
        data = {
            'refresh_token': 'abcde'
        }
        response = requests.post(url, json=data)
        self.assertTrue(response.status_code in [400, 422])

    def test_expired_refresh_token_yields_401(self):
        url = '{0}/api/token/refresh'.format(root_url)
        expired_refresh_token = utils.get_expired_refresh_token(self.current_user.get('id'))
        data = {
            'refresh_token': expired_refresh_token
        }
        response = requests.post(url, json=data)
        # print(response.text)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    # to run all of the tests:
    # unittest.main()

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([
        TestTokenEndpoint('test_token_correct_username_password_yields_token'),
        TestTokenEndpoint('test_access_token_valid'),
        TestTokenEndpoint('test_token_bad_username_yields_error'),
        TestTokenEndpoint('test_token_bad_password_yields_error'),
        TestRefreshTokenEndpoint('test_refresh_token_valid_refresh_yields_access_token'),
        TestRefreshTokenEndpoint('test_access_token_from_refresh_endpoint_is_valid'),
        TestRefreshTokenEndpoint('test_bad_refresh_token_yields_error'),
        TestRefreshTokenEndpoint('test_expired_refresh_token_yields_401')
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)