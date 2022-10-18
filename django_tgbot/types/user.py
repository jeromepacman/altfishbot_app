from . import BasicType


class User(BasicType):
    fields = {
        'id': str,
        'is_bot': BasicType.bool_interpreter,
        'first_name': str,
        'last_name': str,
        'username': str,
        'language_code': str,
        'is_premium': BasicType.bool_interpreter,
        'can_join_groups': BasicType.bool_interpreter,
        'can_read_all_group_messages': BasicType.bool_interpreter,
        'supports_inline_queries': BasicType.bool_interpreter
    }

    def __init__(self, obj=None):
        super(User, self).__init__(obj)

    def get_id(self):
        return getattr(self, 'id', None)

    def get_is_bot(self):
        return getattr(self, 'is_bot', None)

    def get_username(self):
        return getattr(self, 'username', None)

    def get_first_name(self):
        return getattr(self, 'first_name', None)

    def get_last_name(self):
        return getattr(self, 'last_name', None)

    def get_language_code(self):
        return getattr(self, 'language_code', None)

    def get_is_premium(self):
        return getattr(self, 'is_premium', None)