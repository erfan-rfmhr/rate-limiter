from drf_spectacular.openapi import AutoSchema


class AppLabelTaggedSchema(AutoSchema):
    def get_tags(self):
        if hasattr(self.view, "__module__") and "api" in self.path:
            module_parts = self.view.__module__.split(".")
            return [module_parts[0].capitalize()]

        return super().get_tags()
