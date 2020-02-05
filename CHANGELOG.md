# Changelog

## master (unreleased)

Nothing here yet.

## 1.5.0 (2020-02-05)

- Confirm support for Django 2.2 (#33).
- Add Python 3.8 support (#34).

## 1.4.0 (2018-12-17)

- Django 2 support
- Drop support for Django <1.11 and Python <3.5 (we keep 2.7 still)
- Confirm support for Django 2.1
- Add python 3.7 support

## 1.3.1 (2018-05-14)

- Changing Github Organization from ``novafloss`` to ``peopledoc`` (#24),
- Added documentation to install and bootstrap the demo app (#26),
- Removed `PendingDeprecationWarning` due to `StopIteration` usage (#23).

## 1.3.0 (2017-09-14)

- Run tox with Django 1.11 (#22).
- Run tests with the Django master version (#22).

## 1.2.0 (2017-07-03)

- Deal with OneToOne Primary Keys (#19).
- Expose the util function ``chunkator_page`` (#21).

## 1.1.0 (2017-03-25)

- Drop Django 1.6 and 1.7 support (#15).
- Add Django 1.10 support (#18).
- Add Python 3.5 support (#17).

## 1.0.1 (2016-08-26)

**Warning**: this version will be the last to support Django 1.6 or 1.7. Starting of the next version, we'll only support 1.8+.

- Added Django 1.9 support (#9).
- Python 3.4 jobs are being tested in travis (#10).
- Deprecate Django 1.6 and 1.7 support (#9).

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
