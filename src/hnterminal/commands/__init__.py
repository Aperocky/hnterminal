from .get_comments import get_tree_command
from .get_front_page import get_front_page_command
from .get_story import get_story_command
from .get_user import get_user_command
from .login import login_command, logout_command
from .votes import upvote_command, downvote_command, unvote_command
from .reply import reply_to_command

READ_COMMANDS = [
    get_front_page_command,
    get_tree_command,
    get_story_command,
    get_user_command
]

WRITE_COMMANDS = [
    login_command,
    logout_command,
    upvote_command,
    downvote_command,
    unvote_command,
    reply_to_command
]
