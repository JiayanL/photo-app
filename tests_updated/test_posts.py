import utils
import requests

root_url = utils.root_url
import unittest

class TestPostListEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_random_user()
        pass

    def test_posts_get_defaults_to_20(self):
        response = utils.issue_get_request(root_url + '/api/posts', self.current_user.get('id'))
        data = response.json()
        self.assertLessEqual(len(data), 20)
        self.assertEqual(response.status_code, 200)

    def test_posts_get_jwt_required(self):
        response = requests.get(root_url + '/api/posts')
        self.assertEqual(response.status_code, 401)

    def test_posts_get_has_required_data(self):
        response = utils.issue_get_request(root_url + '/api/posts', self.current_user.get('id'))
        data = response.json()
        post = data[0]

        # check that all of the keys are in there and values are of the correct type:
        self.assertTrue('id' in post and type(post['id']) == int)
        self.assertTrue('image_url' in post and type(post['image_url']) == str)
        self.assertTrue('user' in post and type(post['user']) == dict)
        self.assertTrue('caption' in post and type(post['caption']) in [str, type(None)])
        self.assertTrue('alt_text' in post and type(post['alt_text']) in [str, type(None)])
        self.assertTrue('comments' in post and type(post['comments']) == list)
        self.assertEqual(response.status_code, 200)

    def test_posts_get_limit_argument(self):
        response = utils.issue_get_request(root_url + '/api/posts?limit=3', self.current_user.get('id'))
        data = response.json()
        self.assertEqual(len(data), 3)
        self.assertEqual(response.status_code, 200)

    def test_posts_get_bad_limit_argument_handled(self):
        response = utils.issue_get_request(root_url + '/api/posts?limit=80', self.current_user.get('id'))
        self.assertEqual(response.status_code, 400)

        response = utils.issue_get_request(root_url + '/api/posts?limit=abc', self.current_user.get('id'))
        self.assertEqual(response.status_code, 400)

    def test_posts_get_is_authorized(self):
        authorized_user_ids = utils.get_authorized_user_ids(self.current_user.get('id'))
        response = utils.issue_get_request(root_url + '/api/posts?limit=50', self.current_user.get('id'))
        self.assertEqual(response.status_code, 200)
        posts = response.json()
        for post in posts:
            # check that user has access to every post:
            # print(self.current_user.get('id'), '-', post.get('user').get('id'), authorized_user_ids)
            self.assertTrue(post.get('user').get('id') in authorized_user_ids)


    def test_post_post(self):
        body = {
            'image_url': 'https://picsum.photos/600/430?id=668',
            'caption': 'Some caption',
            'alt_text': 'some alt text'
        }
        response = utils.issue_post_request(root_url + '/api/posts', json=body, user_id=self.current_user.get('id'))
        new_post = response.json()
        self.assertEqual(response.status_code, 201)

        # check that the values are in the returned json:
        self.assertEqual(new_post.get('image_url'), body.get('image_url'))
        self.assertEqual(new_post.get('caption'), body.get('caption'))
        self.assertEqual(new_post.get('alt_text'), body.get('alt_text'))

        # verify that data was committed to the database:
        new_post_db = utils.get_post_by_id(new_post.get('id'))
        self.assertEqual(new_post_db.get('id'), new_post.get('id'))
        self.assertEqual(new_post_db.get('image_url'), new_post.get('image_url'))
        self.assertEqual(new_post_db.get('caption'), new_post.get('caption'))
        self.assertEqual(new_post_db.get('alt_text'), new_post.get('alt_text'))

        # now delete post from DB:
        utils.delete_post_by_id(new_post.get('id'))

        # and check that it's gone:
        self.assertEqual(utils.get_post_by_id(new_post.get('id')), [])

    def test_posts_post_jwt_required(self):
        response = requests.post(root_url + '/api/posts', json={})
        self.assertEqual(response.status_code, 401)

    def test_post_post_image_only(self):
        body = {
            'image_url': 'https://picsum.photos/600/430?id=668',
        }
        response = utils.issue_post_request(root_url + '/api/posts', json=body, user_id=self.current_user.get('id'))
        new_post = response.json()
        self.assertEqual(response.status_code, 201)

        # check that the values are in the returned json:
        self.assertEqual(new_post.get('image_url'), body.get('image_url'))
        self.assertEqual(new_post.get('caption'), body.get('caption'))
        self.assertEqual(new_post.get('alt_text'), body.get('alt_text'))

        # verify that data was committed to the database:
        new_post_db = utils.get_post_by_id(new_post.get('id'))
        self.assertEqual(new_post_db.get('id'), new_post.get('id'))
        self.assertEqual(new_post_db.get('image_url'), new_post.get('image_url'))
        self.assertEqual(new_post_db.get('caption'), new_post.get('caption'))
        self.assertEqual(new_post_db.get('alt_text'), new_post.get('alt_text'))

        # now delete post from DB:
        utils.delete_post_by_id(new_post.get('id'))

        # and check that it's gone:
        self.assertEqual(utils.get_post_by_id(new_post.get('id')), [])

    def test_post_post_bad_data_400_error(self):
        url = '{0}/api/posts'.format(root_url)
        
        response = utils.issue_post_request(url, json={}, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 400)
    

class TestPostDetailEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_random_user()
        pass

    def test_post_patch(self):
        post_to_update = utils.get_post_by_user(self.current_user.get('id'))
        body = {
            'image_url': 'https://picsum.photos/600/430?id=33',
            'caption': 'Another caption 222',
            'alt_text': 'Another alt text 222'
        }
        url = '{0}/api/posts/{1}'.format(root_url, post_to_update.get('id'))
        
        response = utils.issue_patch_request(url, json=body, user_id=self.current_user.get('id'))
        new_post = response.json()
        # print(new_post)
        self.assertEqual(response.status_code, 200)

        # check that the values are in the returned json:
        self.assertEqual(new_post.get('image_url'), body.get('image_url'))
        self.assertEqual(new_post.get('caption'), body.get('caption'))
        self.assertEqual(new_post.get('alt_text'), body.get('alt_text'))

        # verify that data was committed to the database:
        new_post_db = utils.get_post_by_id(new_post.get('id'))
        self.assertEqual(new_post_db.get('id'), new_post.get('id'))
        self.assertEqual(new_post_db.get('image_url'), new_post.get('image_url'))
        self.assertEqual(new_post_db.get('caption'), new_post.get('caption'))
        self.assertEqual(new_post_db.get('alt_text'), new_post.get('alt_text'))

        utils.restore_post(post_to_update)

    def test_post_patch_jwt_required(self):
        post_to_update = utils.get_post_by_user(self.current_user.get('id'))
        url = '{0}/api/posts/{1}'.format(root_url, post_to_update.get('id'))
        response = requests.patch(url, json={})
        self.assertTrue(response.status_code, 401)

    def test_post_patch_blanks_not_overwritten(self):
        post_to_update = utils.get_post_by_user(self.current_user.get('id'))
        body = {
            'image_url': 'https://picsum.photos/600/430?id=223'
        }
        url = '{0}/api/posts/{1}'.format(root_url, post_to_update.get('id'))
        
        response = utils.issue_patch_request(url, json=body, user_id=self.current_user.get('id'))
        new_post = response.json()
        self.assertEqual(response.status_code, 200)

        # check that the values are in the returned json:
        self.assertEqual(new_post.get('image_url'), body.get('image_url'))
        self.assertEqual(new_post.get('caption'), post_to_update.get('caption'))
        self.assertEqual(new_post.get('alt_text'), post_to_update.get('alt_text'))

        # verify that data was committed to the database:
        new_post_db = utils.get_post_by_id(new_post.get('id'))
        self.assertEqual(new_post_db.get('image_url'), new_post.get('image_url'))

        utils.restore_post(post_to_update)

    def test_post_patch_invalid_id_400(self):
        url = '{0}/api/posts/fdsfsdfsdfsdfs'.format(root_url)
        response = utils.issue_patch_request(url, json={}, user_id=self.current_user.get('id'))
        # print(response.json())
        self.assertEqual(response.status_code, 400)

    def test_post_patch_id_does_not_exist_404(self):
        url = '{0}/api/posts/99999'.format(root_url)
        response = utils.issue_patch_request(url, json={}, user_id=self.current_user.get('id'))
        # print(response.json())
        self.assertEqual(response.status_code, 404)

    def test_post_patch_unauthorized_id_404(self):
        post_no_access = utils.get_post_that_user_cannot_access(self.current_user.get('id'))
        url = '{0}/api/posts/{1}'.format(root_url, post_no_access.get('id'))
        
        response = utils.issue_patch_request(url, json={}, user_id=self.current_user.get('id'))
        # print(response.json())
        self.assertEqual(response.status_code, 404)
    
    def test_post_delete(self):
        post_to_delete = utils.get_post_by_user(self.current_user.get('id'))
        url = '{0}/api/posts/{1}'.format(root_url, post_to_delete.get('id'))
        
        response = utils.issue_delete_request(url, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 200)

        # restore the post in the database:
        utils.restore_post_by_id(post_to_delete)

    def test_post_delete_jwt_required(self):
        post_to_delete = utils.get_post_by_user(self.current_user.get('id'))
        url = '{0}/api/posts/{1}'.format(root_url, post_to_delete.get('id'))
        response = requests.delete(url)
        self.assertTrue(response.status_code, 401)

    def test_post_delete_invalid_id_400(self):
        url = '{0}/api/posts/sdfsdfdsf'.format(root_url)
        
        response = utils.issue_delete_request(url, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 400)

    def test_post_delete_id_does_not_exist_404(self):
        post_with_access = utils.get_post_by_user(self.current_user.get('id'))
        url = '{0}/api/posts/99999'.format(root_url, post_with_access.get('id'))
        
        response = utils.issue_delete_request(url, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 404)

    def test_post_delete_unauthorized_id_404(self):
        post_no_access = utils.get_post_that_user_cannot_access(self.current_user.get('id'))
        url = '{0}/api/posts/{1}'.format(root_url, post_no_access.get('id'))
        
        response = utils.issue_delete_request(url, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 404)

    def test_post_get(self):
        post_with_access = utils.get_post_by_user(self.current_user.get('id'))
        url = '{0}/api/posts/{1}'.format(root_url, post_with_access.get('id'))
        
        response = utils.issue_get_request(url, user_id=self.current_user.get('id'))
        # print(self.current_user.get('id'), response.text)
        post = response.json()
        self.assertEqual(post_with_access.get('id'), post.get('id'))
        self.assertEqual(post_with_access.get('image_url'), post.get('image_url'))
        self.assertEqual(post_with_access.get('caption'), post.get('caption'))
        self.assertEqual(post_with_access.get('alt_text'), post.get('alt_text'))
        self.assertTrue('comments' in post and type(post['comments']) == list)
        self.assertEqual(response.status_code, 200)

    def test_post_get_jwt_required(self):
        post_with_access = utils.get_post_by_user(self.current_user.get('id'))
        url = '{0}/api/posts/{1}'.format(root_url, post_with_access.get('id'))
        response = requests.get(url)
        self.assertTrue(response.status_code, 401)

    def test_post_get_invalid_id_400(self):
        post_with_access = utils.get_post_by_user(self.current_user.get('id'))
        url = '{0}/api/posts/sdfsdfdsf'.format(root_url, post_with_access.get('id'))
        
        response = utils.issue_get_request(url, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 400)

    def test_post_get_id_does_not_exist_404(self):
        post_with_access = utils.get_post_by_user(self.current_user.get('id'))
        url = '{0}/api/posts/99999'.format(root_url, post_with_access.get('id'))
        
        response = utils.issue_get_request(url, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 404)

    def test_post_get_unauthorized_id_404(self):
        post_no_access = utils.get_post_that_user_cannot_access(self.current_user.get('id'))
        # print(post_no_access.get('id'), '-', self.current_user.get('id'))
        url = '{0}/api/posts/{1}'.format(root_url, post_no_access.get('id'))
        
        response = utils.issue_get_request(url, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    # to run all of the tests:
    # unittest.main()

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([

        # List Endpoint Tests:
        TestPostListEndpoint('test_posts_get_defaults_to_20'),              # get (list view)
        TestPostListEndpoint('test_posts_get_jwt_required'),                # get (list view)
        TestPostListEndpoint('test_posts_get_has_required_data'),           # get (list view)
        TestPostListEndpoint('test_posts_get_limit_argument'),              # get (list view)
        TestPostListEndpoint('test_posts_get_bad_limit_argument_handled'),  # get (list view)
        TestPostListEndpoint('test_posts_get_is_authorized'),               # get (list view)

        TestPostListEndpoint('test_post_post'),                             # post (create)
        TestPostListEndpoint('test_posts_post_jwt_required'),   
        TestPostListEndpoint('test_post_post_image_only'),                  # post (create)
        TestPostListEndpoint('test_post_post_bad_data_400_error'),          # post (create)

        # Detail Endpoint Tests
        TestPostDetailEndpoint('test_post_patch'),                          # patch (update)
        TestPostDetailEndpoint('test_post_patch_jwt_required'),             # patch (update)
        TestPostDetailEndpoint('test_post_patch_blanks_not_overwritten'),   # patch (update)
        TestPostDetailEndpoint('test_post_patch_invalid_id_400'),           # patch (update)
        TestPostDetailEndpoint('test_post_patch_id_does_not_exist_404'),    # patch (update)
        TestPostDetailEndpoint('test_post_patch_unauthorized_id_404'),      # patch (update)
        
        TestPostDetailEndpoint('test_post_delete'),                         # delete
        TestPostDetailEndpoint('test_post_delete_jwt_required'),
        TestPostDetailEndpoint('test_post_delete_invalid_id_400'),          # delete
        TestPostDetailEndpoint('test_post_delete_id_does_not_exist_404'),   # delete
        TestPostDetailEndpoint('test_post_delete_unauthorized_id_404'),     # delete

        TestPostDetailEndpoint('test_post_get'),                            # get (individual)
        TestPostDetailEndpoint('test_post_get_jwt_required'),
        TestPostDetailEndpoint('test_post_get_invalid_id_400'),             # get (individual) 
        TestPostDetailEndpoint('test_post_get_id_does_not_exist_404'),      # get (individual)
        TestPostDetailEndpoint('test_post_get_unauthorized_id_404')         # get (individual)
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)