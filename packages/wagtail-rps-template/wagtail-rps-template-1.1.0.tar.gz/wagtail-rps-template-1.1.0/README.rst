===========================
Wagtail red pepper Template
===========================

An app that customising the Wagtail Admin Interface for red pepper Customer.


Installation
============

Recommended way to install is ``pip``::

  pip install wagtail-rps-template


* Add ``wagtail_rps`` to ``INSTALLED_APPS`` in settings.py before ``wagtail.admin`` ::

    INSTALLED_APPS = [
      "wagtail_rps",
      ...
    ]

Notes
============

Publishing to PyPI::

	python -m pip install -U wheel twine setuptools
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload --skip-existing dist/*
