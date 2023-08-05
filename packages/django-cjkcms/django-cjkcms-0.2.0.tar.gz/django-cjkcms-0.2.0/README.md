![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-cjkcms)
[![GitHub license](https://img.shields.io/github/license/cjkpl/django-cjkcms)](https://github.com/cjkpl/django-cjkcms/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/cjkpl/django-cjkcms)](https://github.com/cjkpl/django-cjkcms/issues) 

CMS system for Wagtail 3.x (4.x starting with v.0.2.0) forked from and based on [Wagtail CRX](https://github.com/coderedcorp/coderedcms) - an excellent CMS by [CodeRed](https://www.coderedcorp.com/).

## Warning!

As of 03 Sept 22 (v.0.2.0) two required dependencies: wagtail-seo and wagtail-cache are not available in releases compatible with Wagtail 4. As a result, installing cjkcms may uninstall your Django==4.1 and Wagtail==4.0 versions. If it happens, simply reinstall ignoring complaints about version mismatch wagtail-seo and wagtail-cache - they work ok.

## Summary

Out of the box, CjkCMS provides your project with generic, reusable pages:
`ArticleIndex`, `Article`, `WebPage` which you can use in your project, or extend with additional functionality. CjkCMS pages provide you with a generic "body" section and, using `wagtail-seo` package, a basic SEO functionality.

## Documentation
Documentation is a work in progress. See here: [Docs](https://github.com/cjkpl/django-cjkcms/blob/main/docs/index.md)

For a quick overview, see the [quick start guide](https://github.com/cjkpl/django-cjkcms/blob/main/docs/quick-start.md)

For detailed installation instructions, see the [installation guide](https://github.com/cjkpl/django-cjkcms/blob/main/docs/installation.md)

## Contact & support
Please use [Github's Issue Tracker](https://github.com/cjkpl/django-cjkcms/issues) to report bugs, request features, or request support.