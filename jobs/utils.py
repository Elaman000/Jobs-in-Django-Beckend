menu = [
    #{"name":"Компания", "url_name":"/company"},
    {"name":"Вакаcии", "url_name":"/vakatsi/"},
    {"name":"Соискатели", "url_name":"/applicant/"},
    {"name":"Новости", "url_name":""},
    #{"name":"Размести вакасию", "url_name":"/form"},
]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        # if not self.request.user.is_authenticated:
        #     user_menu.pop(4)
        #     user_menu.pop(1)

        context["menu"] = user_menu
        return context