from . import BasicType


class ChatMember(BasicType):
    fields = {
        'status': str,
        'custom_title': str,
        'until_date': str,
        'can_be_edited': BasicType.bool_interpreter,
        'can_post_messages': BasicType.bool_interpreter,
        'can_edit_messages': BasicType.bool_interpreter,
        'can_delete_messages': BasicType.bool_interpreter,
        'can_restrict_members': BasicType.bool_interpreter,
        'can_promote_members': BasicType.bool_interpreter,
        'can_change_info': BasicType.bool_interpreter,
        'can_invite_users': BasicType.bool_interpreter,
        'can_pin_messages': BasicType.bool_interpreter,
        'is_member': BasicType.bool_interpreter,
        'can_manage_topics': BasicType.bool_interpreter,
        'can_manage_video_chats': BasicType.bool_interpreter,
        'can_send_polls': BasicType.bool_interpreter,
        'can_send_other_messages': BasicType.bool_interpreter,
        'can_manage_chat': BasicType.bool_interpreter
    }

    def __init__(self, obj=None):
        super(ChatMember, self).__init__(obj)

    def get_user(self):
        return getattr(self, 'user', None)

    def get_status(self) -> str:
        return getattr(self, 'status', None)


# Placed here to avoid import cycles
from django_tgbot.types import user

ChatMember.fields.update({
    'user': user.User
})