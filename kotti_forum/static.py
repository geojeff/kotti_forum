# -*- coding: utf-8 -*-

from fanstatic import Library
from fanstatic import Resource
from js.jquery_form import jquery_form

library = Library('kotti_forum', 'static')
kotti_forum_js = Resource(
    library,
    'kotti_forum.js',
    minified='kotti_forum.min.js',
    depends=[jquery_form, ]
)
