import collections

class WidgetManager:
    widgets = collections.OrderedDict()

    @classmethod
    def register(cls, name, constructor, animated=False):
        cls.widgets[name] = (constructor, animated)

    @classmethod
    def create(cls, name, *args, **kwargs):
        widget = cls.widgets[name][0](*args, **kwargs)
        widget.animated = cls.widgets[name][1]
        return widget

    @classmethod
    def get_list(cls):
        return cls.widgets.keys()
                



