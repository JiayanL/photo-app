import utils
import requests

root_url = utils.root_url
import unittest

class TestLogoutEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_random_user()

    def test_successful_logout_redirects_to_login_screen(self):
        url = '{0}/logout'.format(root_url)
        response = requests.get(url)

        # check that it redirected to the home screen:
        self.assertEqual(response.url, '{0}/login'.format(root_url))
        self.assertTrue(response.status_code, 200)

if __name__ == '__main__':

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([
        TestLogoutEndpoint('test_successful_logout_redirects_to_login_screen')
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)
    