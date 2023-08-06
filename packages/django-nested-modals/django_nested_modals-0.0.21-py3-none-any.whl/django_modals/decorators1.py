from django_modals.helper import modal_button
from django_modals.modals import Modal


class ConfirmAjaxMethod:

    def __init__(self, *args, **kwargs):
        if args:
            raise Exception('Decorator class ConfirmAjaxMethod must be an instance and have ()')
        self.kwargs = kwargs

    @staticmethod
    def buttons(view, func):
        return [modal_button('Confirm', dict(function='post_modal',
                                             button=dict(ajax_method=func.__name__, confirm=True)),
                             'btn-success'),
                modal_button('Cancel', 'close', 'btn-secondary')]

    def __call__(self, _func=None, _ajax=True, **kwargs):
        def method(view, _ajax=True, **kwargs):
            if kwargs.get('confirm'):
                return _func(view, **kwargs)
            view.request.method = 'GET'
            message = self.kwargs.get('message', 'Are you sure?')
            title = self.kwargs.get('title', 'Warning')
            buttons = self.buttons(view, _func)
            return Modal.as_view()(view.request, slug='-', message=message, modal_title=title, buttons=buttons)
        return method
