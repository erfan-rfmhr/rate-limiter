from drf_spectacular.openapi import AutoSchema


class AppLabelTaggedSchema(AutoSchema):
    def get_tags(self):
        # Check for local apps in module
        if hasattr(self.view, '__module__'):
            module_parts = self.view.__module__.split('.')
            # local_apps = ['core', 'accounts', 'competitions', 'predictions']
            # for app_label in local_apps:
            return [module_parts[0].capitalize()]
        
        # Fallback to default
        return super().get_tags()
