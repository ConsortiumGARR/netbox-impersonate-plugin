"""
NetBox Impersonate Plugin

Lets a superuser browse NetBox as another user.
"""

__author__ = """rizlas"""
__email__ = "8522635+rizlas@users.noreply.github.com"
__version__ = "1.0.0"


from netbox.plugins import PluginConfig


class ImpersonateConfig(PluginConfig):
    name = "netbox_impersonate_plugin"
    verbose_name = "NetBox Impersonate Plugin"
    description = "Browse NetBox as another user."
    author = "rizlas"
    author_email = "8522635+rizlas@users.noreply.github.com"
    version = __version__
    base_url = "impersonate"
    min_version = "4.7.0"
    max_version = "4.7.99"
    django_apps = ["impersonate"]
    middleware = ["impersonate.middleware.ImpersonateMiddleware"]

    def ready(self):
        super().ready()
        from django.conf import settings

        from . import tables  # noqa: F401

        # NetBox does not pass arbitrary settings from configuration.py to Django, so the
        # plugin owns this one. NetBox users have no is_staff, which the library's default
        # check reads.
        settings.IMPERSONATE = {
            "CUSTOM_ALLOW": "netbox_impersonate_plugin.utils.allow_impersonate",
            "CUSTOM_USER_QUERYSET": "netbox_impersonate_plugin.utils.impersonable_users",
            "USE_HTTP_REFERER": True,
        }


config = ImpersonateConfig
