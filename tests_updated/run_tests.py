import utils
utils.modify_system_path()

import unittest

# import the tests you want to run:
from tests_updated.test_bookmarks import TestBookmarkListEndpoint
from tests_updated.test_comments import TestCommentListEndpoint, TestCommentDetailEndpoint
from tests_updated.test_followers import TestFollowerListEndpoint
from tests_updated.test_following import TestFollowingListEndpoint
from tests_updated.test_like_post import TestLikePostListEndpoint
from tests_updated.test_login import TestLoginEndpoint
from tests_updated.test_logout import TestLogoutEndpoint
from tests_updated.test_posts import TestPostListEndpoint, TestPostDetailEndpoint
from tests_updated.test_profile import TestProfileEndpoint
from tests_updated.test_stories import TestStoryListEndpoint
from tests_updated.test_suggestions import TestSuggestionsEndpoint
from tests_updated.test_token import TestTokenEndpoint, TestRefreshTokenEndpoint


if __name__ == '__main__':
    unittest.main()

# Note: to run on command line (from the tests directory): 
# $ python3 run_tests.py -v
# $ python3 run_tests.py TestPostListEndpoint -v
# $ python3 run_tests.py TestPostDetailEndpoint -v
# $ python3 run_tests.py TestFollowingListEndpoint -v
