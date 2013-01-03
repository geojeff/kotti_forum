# -*- coding: utf-8 -*-

import os
import kotti
import plone
from kotti.resources import get_root
from kotti.testing import DummyRequest
from kotti.testing import UnitTestBase
from kotti_forum.resources import Forum
from kotti_forum.resources import Post
from kotti_forum.views import PostView
from kotti_forum.views import ForumView

here = os.path.abspath(os.path.dirname(__file__))


class ViewsTests(UnitTestBase):

    def test_post_view(self):

        root = get_root()
        post = root['post'] = Post()

        view = PostView(post, DummyRequest()).view()

        assert view is not None

    def test_forum_view_adding_post(self):

        root = get_root()
        forum = root['forum'] = Forum()
        view = ForumView(root['forum'],
                                      DummyRequest()).view()
        post = forum['post'] = Post()

        assert post is not None

        assert view is not None

        assert ('items' in view)
        
        batch = view['items']

        assert type(batch) is plone.batching.batch.BaseBatch

        assert ('api' in view) \
                and (type(view['api']) is kotti.views.util.TemplateAPI)

        assert ('settings' in view) \
                 and ('use_batching' in view['settings']) \
                 and (view['settings']['use_batching'] is True)
        assert ('settings' in view) \
                and ('pagesize' in view['settings']) \
                and (view['settings']['pagesize'] == 10)
        assert ('settings' in view) \
                and ('use_auto_batching' in view['settings']) \
                and (view['settings']['use_auto_batching'] is True)
        assert ('settings' in view) \
                and ('link_headline_overview' in view['settings']) \
                and (view['settings']['link_headline_overview'] is True)

    def test_forum_view_no_post(self):

        root = get_root()
        forum = root['forum'] = Forum()
        view = ForumView(root['forum'],
                                      DummyRequest()).view()

        assert view is not None

        assert ('items' in view) and (len(view['items']) == 0)

        assert ('settings' in view) \
                 and ('use_batching' in view['settings']) \
                 and (view['settings']['use_batching'] is True)
        assert ('settings' in view) \
                and ('pagesize' in view['settings']) \
                and (view['settings']['pagesize'] == 10)
        assert ('settings' in view) \
                and ('use_auto_batching' in view['settings']) \
                and (view['settings']['use_auto_batching'] is True)
        assert ('settings' in view) \
                and ('link_headline_overview' in view['settings']) \
                and (view['settings']['link_headline_overview'] is True)
        assert (('settings' in view) \
                 and ('use_batching' in view['settings']) \
                 and (view['settings']['use_batching'] is True))
