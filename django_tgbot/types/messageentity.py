from . import BasicType


class MessageEntity(BasicType):
    fields = {
        'type': str,
        'offset': int,
        'length': int,
        'url': str,
        'language': str,
    }

    def __init__(self, obj=None):
        super(MessageEntity, self).__init__(obj)

    def get_type(self) -> str:
        return getattr(self, 'type', None)

    def get_language(self) -> str:
        return getattr(self, 'language', None)


from django_tgbot.types import user

MessageEntity.fields.update(dict(user=user.User))
