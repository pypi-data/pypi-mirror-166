# 0.1.1 (2022-08-14)
* Updated the README.md

# 0.1.2 (2022-08-14)
* Updated the README.md

# 0.1.3 (2022-08-15)
* added config for mkdocs
* moved docs folder one level up
* started basic documentation and updated readme
* updated pyproject.toml and added requirements to setup.cfg

# 0.1.4 (2022-08-15)
* fixed broken docs links in readme

# 0.1.5 (2022-08-15)
* fixed missing folders in the install package (modified manifest file)

# 0.1.6 (2022-08-25)
* Added import of `BaseBlock` to cjkcms.blocks for compatibility with other apps using the block
* Fixed missing InlinePanel allowing choosing default site navbar in Settings -> Layout
* Removed models/cms_models_legacy.py as it was crashing doctests due to duplicate model names
* extracted get_panels() method from Cjkcmspage get_edit_handler() to simplify overriding admin panels in subclasses. (as per suggestion of @FilipWozniak)

# 0.1.7 (2022-08-27)
* Added missing InlinePanel allowing choosing footers for the website in Settings -> Layout

# 0.1.8 (2022-08-27)
* Fixed missing search template in CjkcmsMeta (for backward compatibility)
* Fixed broken Advanced Settings in admin panel (hooks adding js/css were missing)

# 0.1.9.x (2022-09-01)
* Fixed broken get_panels() call preventing display of body panels in backend editor
* Removed useless debug/print entries in page_models

# 0.2.0 (2022-09-03)
* NON-COMPATIBLE with Wagtail<4.0! 
* Added missing attribute `use_json_field=True` in StreamField in several models - new migration.
* Removed unused block ada_skip in base page template.

# 0.2.1 (2022-09-03)
* Changed dependencies wagtail-seo i wagtail-cache to forked versions, which allow Wagtail 4.0.

# 0.2.2 (2022-09-03)
* Added cms_models to models/_init__.py, as they are already part of migration 0001, so they are not optional. Updated docs to reflect this.