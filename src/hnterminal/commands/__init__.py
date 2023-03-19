from .get_comments import get_comments_command
from .get_front_page import get_front_page_command
from .get_story import get_story_command
from .get_user import get_user_command

READ_COMMANDS = [
    get_front_page_command,
    get_comments_command,
    get_story_command,
    get_user_command
]
