from netbox.plugins import PluginTemplateExtension


class ImpersonateButton(PluginTemplateExtension):
    models = ["users.user"]

    def buttons(self):
        request = self.context["request"]
        real = request.real_user
        target = self.context["object"]
        if (
            not real.is_superuser
            or target.pk == real.pk
            or target.is_superuser
            or not target.is_active
        ):
            return ""
        return self.render("netbox_impersonate_plugin/inc/start_button.html")


class ImpersonateBanner(PluginTemplateExtension):
    def navbar(self):
        if not self.context["request"].impersonator:
            return ""
        return self.render("netbox_impersonate_plugin/inc/banner.html")


template_extensions = [ImpersonateButton, ImpersonateBanner]
