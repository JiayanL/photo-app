import utils
import requests

root_url = utils.root_url
import unittest

class TestBookmarkListEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_random_user()

    def test_bookmarks_get_check_if_query_correct(self):
        response = utils.issue_get_request('{0}/api/bookmarks'.format(root_url), user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 200)
        bookmarks = response.json()
        bookmark_ids = utils.get_bookmark_ids(self.current_user.get('id'))
        self.assertTrue(len(bookmarks) > 1)
        for bookmark in bookmarks:
            self.assertTrue(bookmark.get('id') in bookmark_ids)

    def test_bookmarks_get_check_if_data_structure_correct(self):
        response = utils.issue_get_request('{0}/api/bookmarks'.format(root_url), user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 200)
        bookmarks = response.json()
        bookmark = bookmarks[0]
        
        bookmark_db = utils.get_bookmark_by_id(bookmark.get('id'))
        post_db = utils.get_post_by_id(bookmark.get('post').get('id'))

        self.assertEqual(bookmark.get('id'), bookmark_db.get('id'))
        self.assertEqual(bookmark.get('post').get('id'), post_db.get('id'))
        self.assertEqual(bookmark.get('post').get('image_url'), post_db.get('image_url'))
        self.assertEqual(bookmark.get('post').get('caption'), post_db.get('caption'))
        self.assertEqual(bookmark.get('post').get('alt_text'), post_db.get('alt_text'))
        self.assertEqual(bookmark.get('post').get('user').get('id'), post_db.get('user_id'))

    def test_bookmarks_get_jwt_required(self):
        response = requests.get('{0}/api/bookmarks'.format(root_url))
        # print(response.text)
        self.assertEqual(response.status_code, 401)

    def test_bookmark_post_valid_request_201(self):
        post_id = utils.get_unbookmarked_post_id_by_user(self.current_user.get('id'))
        body = {
            'post_id': post_id
        }
        response = utils.issue_post_request(root_url + '/api/bookmarks', json=body, user_id=self.current_user.get('id'))
        # print(response.text)
        new_bookmark = response.json()
        self.assertEqual(response.status_code, 201)


        # check that the values are in the returned json:
        self.assertEqual(new_bookmark.get('post').get('id'), post_id)

        # check that it's actually in the database:
        bookmark_db = utils.get_bookmark_by_id(new_bookmark.get('id'))
        self.assertEqual(bookmark_db.get('id'), new_bookmark.get('id'))

        # now delete bookmark from DB:
        utils.delete_bookmark_by_id(new_bookmark.get('id'))

        # and check that it's gone:
        self.assertEqual(utils.get_bookmark_by_id(new_bookmark.get('id')), [])

    def test_bookmark_post_no_duplicates_400(self):
        bookmark = utils.get_bookmarked_post_by_user(self.current_user.get('id'))
        body = {
            'post_id': bookmark.get('post_id')
        }
        response = utils.issue_post_request(root_url + '/api/bookmarks', json=body, user_id=self.current_user.get('id'))
        # print(response.text)
        self.assertEqual(response.status_code, 400)

    def test_bookmark_post_invalid_post_id_format_400(self):
        body = {
            'post_id': 'dasdasdasd'
        }
        response = utils.issue_post_request(root_url + '/api/bookmarks', json=body, user_id=self.current_user.get('id'))
        # print(response.text)
        self.assertEqual(response.status_code, 400)

    def test_bookmark_post_invalid_post_id_404(self):
        body = {
            'post_id': 999999
        }
        response = utils.issue_post_request(root_url + '/api/bookmarks', json=body, user_id=self.current_user.get('id'))
        # print(response.text)
        self.assertEqual(response.status_code, 404)

    def test_bookmark_post_unauthorized_post_id_404(self):
        post = utils.get_post_that_user_cannot_access(self.current_user.get('id'))
        body = {
            'post_id': post.get('id'),
        }
        response = utils.issue_post_request(root_url + '/api/bookmarks', json=body, user_id=self.current_user.get('id'))
        # print(response.text)
        self.assertEqual(response.status_code, 404)
    
    def test_bookmark_post_missing_post_id_400(self):
        response = utils.issue_post_request(root_url + '/api/bookmarks', json={}, user_id=self.current_user.get('id'))
        # print(response.text)
        self.assertEqual(response.status_code, 400)

    def test_bookmarks_post_jwt_required(self):
        post_id = utils.get_unbookmarked_post_id_by_user(self.current_user.get('id'))
        body = { 'post_id': post_id }
        response = requests.post('{0}/api/bookmarks'.format(root_url), json=body)
        # print(response.text)
        self.assertEqual(response.status_code, 401)

    
class TestBookmarkDetailEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.current_user = utils.get_random_user()

    def test_bookmark_delete_valid_200(self):
        bookmark_to_delete = utils.get_bookmark_by_user(self.current_user.get('id'))
        bookmark_id =bookmark_to_delete.get('id')
        url = '{0}/api/bookmarks/{1}'.format(root_url, bookmark_id)
        
        response = utils.issue_delete_request(url, user_id=self.current_user.get('id'))
        print(response.text)
        self.assertEqual(response.status_code, 200)

        # restore the post in the database:
        utils.restore_bookmark(bookmark_to_delete)


    def test_bookmark_delete_invalid_id_format_400(self):
        url = '{0}/api/bookmarks/sdfsdfdsf'.format(root_url)
        response = utils.issue_delete_request(url, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 400)
        
    
    def test_bookmark_delete_invalid_id_404(self):
        url = '{0}/api/bookmarks/99999'.format(root_url)
        response = utils.issue_delete_request(url, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 404)

        
    def test_bookmark_delete_unauthorized_id_404(self): 
        unauthorized_bookmark = utils.get_bookmark_that_user_cannot_delete(self.current_user.get('id'))
        url = '{0}/api/bookmarks/{1}'.format(root_url, unauthorized_bookmark.get('id'))
        response = utils.issue_delete_request(url, user_id=self.current_user.get('id'))
        self.assertEqual(response.status_code, 404)
        
    def test_bookmarks_delete_jwt_required(self):
        bookmark_to_delete = utils.get_bookmark_by_user(self.current_user.get('id'))
        bookmark_id =bookmark_to_delete.get('id')
        url = '{0}/api/bookmarks/{1}'.format(root_url, bookmark_id)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    # to run all of the tests:
    # unittest.main()

    # to run some of the tests (convenient for commenting out some of the tests):
    suite = unittest.TestSuite()
    suite.addTests([
        
        # GET (List) Tests:
        TestBookmarkListEndpoint('test_bookmarks_get_check_if_query_correct'),
        TestBookmarkListEndpoint('test_bookmarks_get_check_if_data_structure_correct'),
        TestBookmarkListEndpoint('test_bookmarks_get_jwt_required'),
        
        # POST Tests:
        TestBookmarkListEndpoint('test_bookmark_post_valid_request_201'),
        TestBookmarkListEndpoint('test_bookmark_post_no_duplicates_400'),
        TestBookmarkListEndpoint('test_bookmark_post_invalid_post_id_format_400'),
        TestBookmarkListEndpoint('test_bookmark_post_invalid_post_id_404'),
        TestBookmarkListEndpoint('test_bookmark_post_unauthorized_post_id_404'),
        TestBookmarkListEndpoint('test_bookmark_post_missing_post_id_400'),  
        TestBookmarkListEndpoint('test_bookmarks_post_jwt_required'),

        # DELETE Tests
        TestBookmarkDetailEndpoint('test_bookmark_delete_valid_200'),
        TestBookmarkDetailEndpoint('test_bookmark_delete_invalid_id_format_400'),
        TestBookmarkDetailEndpoint('test_bookmark_delete_invalid_id_404'),
        TestBookmarkDetailEndpoint('test_bookmark_delete_unauthorized_id_404'),   
        TestBookmarkDetailEndpoint('test_bookmarks_delete_jwt_required') 
    ])

    unittest.TextTestRunner(verbosity=2).run(suite)