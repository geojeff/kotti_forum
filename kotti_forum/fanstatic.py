# -*- coding: utf-8 -*-

from __future__ import absolute_import

from kotti.fanstatic import view_needed

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.jquery_form import jquery_form

from js.jquery_infinite_ajax_scroll import jquery_infinite_ajax_scroll
from js.jquery_infinite_ajax_scroll import jquery_infinite_ajax_scroll_css

library = Library('kotti_forum', 'static')

kotti_forum_css = Resource(library,
                           "style.css",
                           depends=[jquery_infinite_ajax_scroll_css, ],
                           bottom=True)

kotti_forum_js = Resource(library,
                          "kotti_forum.js",
                          depends=[jquery_infinite_ajax_scroll, ],
                          bottom=True)

view_needed.add(Group([kotti_forum_css, kotti_forum_js, ]))
