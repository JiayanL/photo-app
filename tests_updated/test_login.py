import utils
import requests

root_url = utils.root_url
import unittest

class TestLoginEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_random_user()
        pass

    def test_successful_login_redirects_to_home_screen(self):
        url = '{0}/login'.format(root_url)
        form_data = {
            'username': self.current_user.get('username'),
            'password': self.current_user.get('password_plaintext')
        }
        response = requests.post(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'content-type': 'application/x-www-form-urlencoded'
        }, data=form_data)
        # print(response.text)
        # print(response.cookies.get_dict())
        
        # check that it redirected to the home screen:
        self.assertEqual(response.url, '{0}/'.format(root_url))
        self.assertTrue(response.status_code, 200)

    def test_bad_username_does_not_redirect(self):
        url = '{0}/login'.format(root_url)
        form_data = {
            'username': 'blah',
            'password': self.current_user.get('password_plaintext')
        }
        response = requests.post(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'content-type': 'application/x-www-form-urlencoded'
        }, data=form_data)
        
        # check that it redirected to the home screen:
        self.assertEqual(response.url, url)
        self.assertTrue(response.status_code, 200)

    def test_bad_password_does_not_redirect(self):
        url = '{0}/login'.format(root_url)
        form_data = {
            'username': self.current_user.get('username'),
            'password': 'blah'
        }
        response = requests.post(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'content-type': 'application/x-www-form-urlencoded'
        }, data=form_data)
        
        # check that it redirected to the home screen:
        self.assertEqual(response.url, url)
        self.assertTrue(response.status_code, 200)

    def test_home_redirects_to_login_without_jwt(self):
        url = '{0}/'.format(root_url)
        response = requests.get(url)
        
        # check that it redirected to the home screen:
        self.assertEqual(response.url, '{0}/login'.format(root_url))
        self.assertTrue(response.status_code, 200)

    def test_home_loads_with_jwt(self):
        url = '{0}/'.format(root_url)
        response = utils.issue_get_request(url, user_id=self.current_user.get('id'))
        
        # check that it redirected to the home screen:
        self.assertEqual(response.url, url)
        self.assertTrue(response.status_code, 200)
 
 
if __name__ == '__main__':
    # to run all of the tests:
    # unittest.main()

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([
        TestLoginEndpoint('test_successful_login_redirects_to_home_screen'),
        TestLoginEndpoint('test_bad_username_does_not_redirect'),
        TestLoginEndpoint('test_bad_password_does_not_redirect'),
        TestLoginEndpoint('test_home_redirects_to_login_without_jwt'),
        TestLoginEndpoint('test_home_loads_with_jwt')
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)