class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['active'] = kwargs.get('active')
        context['cat_name'] = kwargs.get('cat_name')

        # if 'cat_name' not in context:
        #     context['cat_name'] = None

        return context