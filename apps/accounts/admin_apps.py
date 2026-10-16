"""
``django.contrib.admin`` with the back office's own site as its default (F-5).

Django's documented way of replacing the default admin site: an ``AdminConfig`` whose ``default_site`` names the
class, listed in INSTALLED_APPS in place of ``django.contrib.admin``. Every ``admin.site.register`` and
``@admin.register`` — this project's and third parties' — then lands on ``accounts.admin_site.BackofficeAdminSite``.
unfold is installed with its ``BasicAppConfig``, which leaves the default site alone (its default config would
install a plain ``UnfoldAdminSite`` over it).

This module is imported while the app registry is being populated, so it names the site by its dotted path and
imports nothing else: the site class is loaded the first time ``admin.site`` is used, when the apps are ready.
It is a module of its own, not ``accounts/apps.py``, because Django picks an app's configuration from that file
and a second ``AppConfig`` there would unseat ``AccountsConfig``.
"""

from django.contrib.admin.apps import AdminConfig


class BackofficeAdminConfig(AdminConfig):
    default_site = "accounts.admin_site.BackofficeAdminSite"
