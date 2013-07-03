# -*- coding: utf-8 -*-

import re

SUPERTOOLS_MENU_CSS_ACTIVE = getattr(settings, 'SUPERTOOLS_MENU_CSS_ACTIVE', '')

attr_rx1 = re.compile(r"^in_(.+)$", flags=re.U)
attr_rx2 = re.compile(r"^if_menu(\d+)_is_(.+)$", flags=re.U)


class Menu(object):
    """
    Menu context object.
    """

    def __init__(self, menu):
        if isinstance(menu, (list, tuple)):
            self.menu = menu
        else:
            self.menu = (menu,)

    def __getattr__(self, attr):
        res1 = attr_rx1.search(attr)
        res2 = attr_rx2.search(attr)

        if res1:
            def default_method(*args):
                if res1.group(1) in self.menu:
                    return True if not SUPERTOOLS_MENU_CSS_ACTIVE else SUPERTOOLS_MENU_CSS_ACTIVE
                else:
                    return False if not SUPERTOOLS_MENU_CSS_ACTIVE else ''
            return default_method

        elif res2:
            menu_index, menu_name = res2.groups()
            def default_method(*args):
                try:
                    if self.menu[int(menu_index)] == menu_name:
                        return True if not SUPERTOOLS_MENU_CSS_ACTIVE else SUPERTOOLS_MENU_CSS_ACTIVE
                    else:
                        return False if not SUPERTOOLS_MENU_CSS_ACTIVE else ''
                except IndexError:
                    return False if not SUPERTOOLS_MENU_CSS_ACTIVE else ''
            return default_method

        return super(MenuActives, self).__getattr__(attr)


class MenuMixin(object):
    """
    Menu mixin add multilevel menu available to a template
    throught view.menu variable
    """

    def __init__(self, *args, **kwargs):
        self.menu = Menu(kwargs.pop("menu", getattr(self, "menu", [])))
        super(MenuMixin, self).__init__(*args, **kwargs)
