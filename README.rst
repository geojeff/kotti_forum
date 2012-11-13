===========
kotti_forum
===========

This is an extension to the Kotti CMS that adds a discussion forum to a site,
or more than one forum.

`Find out more about Kotti`_

Setting up kotti_forum
======================

This Addon adds three new Content Types to your Kotti site.
To set up the content types add ``kotti_forum.kotti_configure``
to the ``kotti.configurators`` setting in your ini file::

    kotti.configurators = kotti_forum.kotti_configure

Now you can create a forum and add topics and posts.

There are different settings to adjust the behavior of the
software.

You can select if the posts in the forum overview
should be batched. If you set 
``kotti_forum.forum_settings.use_batching`` to ``true``
(the default value) the posts will be shown on separate
pages. If you set it to ``false`` all posts are shown
all together on one page::

    kotti_forum.forum_settings.use_batching = false

If you use batching you can choose how many posts are
shown on one page. The default value for 
``kotti_forum.forum_settings.pagesize`` is 5::

    kotti_forum.forum_settings.pagesize = 10

You can use auto batching where the next page of the posts
is automatically loaded when scrolling down the overview page instead
of showing links to switch the pages. The default for
``kotti_forum.forum_settings.use_auto_batching`` is ``true``::

    kotti_forum.forum_settings.use_auto_batching = false

With ``kotti_forum.forum_settings.link_headline_overview`` you
can control whether the headline of a post in the
forum overview is linked to the post or not. This
setting defaults to ``true``::

    kotti_forum.forum_settings.link_headline_overview = false

Parts of kotti_forum can be overridden with the setting
``kotti_forum.asset_overrides``. Have a look to the 
`Kotti documentation about the asset_overrides setting`_, which is the
same as in ``kotti_forum``.

Be warned: This addon is in alpha state. Use it at your own risk.

Using kotti_forum
====================

Add a forum to your site, then to that add topics, and to those, posts.

Work in progress
================

``kotti_forum`` is considered alpha software, not yet suitable for use in
production environments.  The current state of the project is in no way feature
complete nor API stable.  If you really want to use it in your project(s), make
sure to pin the exact version in your requirements.  Not doing so will likely
break your project when future releases become available.

Development
===========

Contributions to ``kotti_forum`` are very welcome.
Just clone its `GitHub repository`_ and submit your contributions as pull requests.

Note that all development is done on the ``develop`` branch. ``master`` is reserved
for "production-ready state".  Therefore, make sure to always base development work
on the current state of the ``develop`` branch.

This follows the highly recommended `A successful Git branching model`_ pattern,
which is implemented by the excellent `gitflow`_ git extension.

Testing
-------

|build status|_

``kotti_forum`` has 100% test coverage.
Please make sure that you add tests for new features and that all tests pass before
submitting pull requests.  Running the test suite is as easy as running ``py.test``
from the source directory (you might need to run ``python setup.py dev`` to have all
the test requirements installed in your virtualenv).


.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti
.. _Kotti documentation about the asset_overrides setting: http://kotti.readthedocs.org/en/latest/configuration.html?highlight=asset#adjust-the-look-feel-kotti-asset-overrides
.. _GitHub repository: https://github.com/geojeff/kotti_forum
.. _gitflow: https://github.com/nvie/gitflow
.. _A successful Git branching model: http://nvie.com/posts/a-successful-git-branching-model/
x.x. |build status| image:: https://secure.travis-ci.org/geojeff/kotti_forum.png?branch=master
x.x. _build status: http://travis-ci.org/geojeff/kotti_forum
