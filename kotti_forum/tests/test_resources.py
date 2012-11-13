# -*- coding: utf-8 -*-

from pyramid.threadlocal import get_current_registry

from kotti.resources import get_root

from kotti.testing import DummyRequest
from kotti.testing import UnitTestBase
from kotti.testing import FunctionalTestBase
from kotti.testing import testing_db_url

from kotti_forum import forum_settings
from kotti_forum.resources import Forum
from kotti_forum.resources import Post


class UnitTests(UnitTestBase):

    def test_forum(self):
        root = get_root()
        forum = Forum()
        assert forum.type_info.addable(root, DummyRequest()) is True
        root['forum'] = forum

        post = Post()

        assert len(forum.values()) == 0

        # there are no children of type Post yet, the UI should present the add link
        assert post.type_info.addable(forum, DummyRequest()) is True

        forum['post'] = post

        assert len(forum.values()) == 1

    def test_post_only_pypi_url_provided(self):
        root = get_root()
        forum = Forum()
        root['forum'] = forum

        post = Post(
                pypi_url="http://pypi.python.org/pypi/kotti_forum/json")

        forum['post'] = post

        assert len(forum.values()) == 1

    def test_post_only_github_owner_and_repo_provided(self):
        root = get_root()
        forum = Forum()
        root['forum'] = forum

        post = Post(
                github_owner="geojeff",
                github_repo="kotti_forum")

        forum['post'] = post

        assert len(forum.values()) == 1

    def test_post_github_data(self):
        root = get_root()
        forum = Forum()
        root['forum'] = forum

        post = Post(
                title="kotti_forum Project",
                date_handling_choice="use_github_date",
                desc_handling_choice="use_github_description",
                github_owner="geojeff",
                github_repo="kotti_forum")

        forum['post'] = post

        assert len(forum.values()) == 1

    def test_post_only_bitbucket_owner_and_repo_provided(self):
        root = get_root()
        forum = Forum()
        root['forum'] = forum

        post = Post(
                bitbucket_owner="pypy",
                bitbucket_repo="pypy")

        forum['post'] = post

        assert len(forum.values()) == 1

    def test_post_bitbucket_data(self):
        root = get_root()
        forum = Forum()
        root['forum'] = forum

        post = Post(
                title="kotti_forum Project",
                date_handling_choice="use_bitbucket_date",
                desc_handling_choice="use_bitbucket_description",
                bitbucket_owner="pypy",
                bitbucket_repo="pypy")

        forum['post'] = post

        assert len(forum.values()) == 1

    def test_post_pypi_overwriting(self):
        root = get_root()
        forum = Forum()
        root['forum'] = forum

        post = Post(
                pypi_url="http://pypi.python.org/pypi/Kotti/json",
                overwrite_home_page_url=True,
                overwrite_docs_url=True,
                overwrite_package_url=True,
                overwrite_bugtrack_url=True,
                desc_handling_choice='use_pypi_summary')

        forum['post'] = post

        assert len(forum.values()) == 1

        # desc_handling_choice is an either/or,
        # so also check for description overwriting
        post = Post(
                pypi_url="http://pypi.python.org/pypi/Kotti/json",
                desc_handling_choice='use_pypi_description')


class FunctionalTests(FunctionalTestBase):

    def setUp(self, **kwargs):
        self.settings = {'kotti.configurators': 'kotti_forum.kotti_configure',
                         'sqlalchemy.url': testing_db_url(),
                         'kotti.secret': 'dude',
                         'kotti_forum.forum_settings.pagesize': '5'}
        super(FunctionalTests, self).setUp(**self.settings)

    def test_asset_overrides(self):
        from kotti import main
        self.settings['kotti_forum.asset_overrides'] = 'kotti_forum:hello_world/'
        main({}, **self.settings)

    def test_forum_default_settings(self):
        b_settings = forum_settings()
        assert b_settings['use_batching'] == True
        assert b_settings['pagesize'] == 5
        assert b_settings['use_auto_batching'] == True
        assert b_settings['link_headline_overview'] == True

    def test_forum_change_settings(self):
        settings = get_current_registry().settings
        settings['kotti_forum.forum_settings.use_batching'] = u'false'
        settings['kotti_forum.forum_settings.pagesize'] = u'2'
        settings['kotti_forum.forum_settings.use_auto_batching'] = u'false'
        settings['kotti_forum.forum_settings.link_headline_overview'] = u'false'

        b_settings = forum_settings()
        assert b_settings['use_batching'] == False
        assert b_settings['pagesize'] == 2
        assert b_settings['use_auto_batching'] == False
        assert b_settings['link_headline_overview'] == False

    def test_forum_wrong_settings(self):
        settings = get_current_registry().settings
        settings['kotti_forum.forum_settings.use_batching'] = u'blibs'
        settings['kotti_forum.forum_settings.pagesize'] = u'blabs'
        settings['kotti_forum.forum_settings.use_auto_batching'] = u'blubs'
        settings['kotti_forum.forum_settings.link_headline_overview'] = u'blobs'

        b_settings = forum_settings()
        assert b_settings['use_batching'] == False
        assert b_settings['pagesize'] == 5
        assert b_settings['use_auto_batching'] == False
        assert b_settings['link_headline_overview'] == False
