from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from zope.interface import implements

from kotti.resources import IDocument
from kotti.resources import IDefaultWorkflow
from kotti.resources import Document

from kotti_forum import _


class Forum(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column('id', Integer, ForeignKey('documents.id'), primary_key=True)

    type_info = Document.type_info.copy(
        name=u'Forum',
        title=_(u'Forum'),
        add_view=u'add_forum',
        addable_to=[u'Document'],
        )

    def __init__(self, **kwargs):
        super(Forum, self).__init__(**kwargs)

        self.default_view = 'folder-view'


class Topic(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column('id', Integer, ForeignKey('documents.id'), primary_key=True)
    votable = Column('votable', Boolean())

    type_info = Document.type_info.copy(
        name=u'Topic',
        title=_(u'Topic'),
        add_view=u'add_topic',
        addable_to=[u'Forum'],
        )

    def __init__(self, votable=True, **kwargs):
        super(Topic, self).__init__(**kwargs)
        self.votable = votable

        self.default_view = 'folder-view'


class Post(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column(Integer, ForeignKey('documents.id'), primary_key=True)

    type_info = Document.type_info.copy(
        name=u'Post',
        title=_(u'Post'),
        add_view=u'add_post',
        addable_to=[u'Topic'],
        )

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)


class Vote(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column(Integer, ForeignKey('documents.id'), primary_key=True)

    vote = Column('vote', Integer())

    type_info = Document.type_info.copy(
        name=u'Vote',
        title=_(u'Vote'),
        add_view=u'add_vote',
        addable_to=[u'Topic'],
        )

    def __init__(self, vote="0", **kwargs):
        super(Vote, self).__init__(**kwargs)

        self.vote = vote
