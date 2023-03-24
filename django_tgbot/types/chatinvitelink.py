from . import BasicType


class ChatInviteLink(BasicType):
    fields = {
        'invite_link': str,
        'creates_join_request': BasicType.bool_interpreter,
        'is_primary': BasicType.bool_interpreter,
        'is_revoked': BasicType.bool_interpreter,

    }

    def __init__(self, obj=None):
        super(ChatInviteLink, self).__init__(obj)

    def get_user(self):
        return getattr(self, 'user', None)


from django_tgbot.types import user

ChatInviteLink.fields.update({'user': user.User})
