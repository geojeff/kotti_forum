# -*- coding: utf-8 -*-

from pyramid.threadlocal import get_current_registry

from kotti.resources import get_root

from kotti.testing import DummyRequest
from kotti.testing import FunctionalTestBase
from kotti.testing import testing_db_url

from kotti_forum import forum_settings
from kotti_forum.resources import Forum
from kotti_forum.resources import Post


def test_forum(db_session):
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

class FunctionalTests(FunctionalTestBase):

    def setUp(self, **kwargs):
        self.settings = {'kotti.configurators': 'kotti_forum.kotti_configure',
                         'sqlalchemy.url': testing_db_url(),
                         'kotti.secret': 'dude',
                         'kotti_forum.forum_settings.pagesize': '10'}
        super(FunctionalTests, self).setUp(**self.settings)

#    def test_asset_overrides(self):
#        from kotti import main
#        self.settings['kotti_forum.asset_overrides'] = 'kotti_forum:hello_world/'
#        main({}, **self.settings)

    def test_forum_default_settings(self):
        b_settings = forum_settings()
        assert b_settings['use_batching'] == True
        assert b_settings['pagesize'] == 10
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
        assert b_settings['pagesize'] == 10
        assert b_settings['use_auto_batching'] == False
        assert b_settings['link_headline_overview'] == False
