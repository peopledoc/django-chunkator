# Changelog

## master (unreleased)

- Added Django 1.9 suport (#9).

## 1.0.0 (2016-06-23)

* Django 1.8 compatibility, thank you ``tox`` (#5).
* Compatible with Python 3 (tested with Python 3.4), thx @wo0dyn (#6).
* Various fixes and added a proper MIT License file (#8).

## v0.0.5

(released on 2015-06-18)

* Bugfix: removed multiple "pk > 'x'" condition statements (#4).

## v0.0.4

(released on 2015-03-30)

* Allow the usage of ``values()`` instead of the usual queryset (#2 and #3)

## v0.0.3

(released on 2015-03-19)

* allow "non-integer" pk (#1), such as UUIDs.


## v0.0.2

(released on 2015-03-19)

* tox and travis setup,
* a few more tests

## v0.0.1

(released on 2015-03-18)

* Proof of concept release, we can iterate over large querysets chunk by chunk,
* include demo test suite,
