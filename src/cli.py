from replbuilder import ReplRunner
from hnterminal.hncontext import HNContext
from hnterminal.commands.get_front_page import get_front_page_command
from hnterminal.commands.get_story import get_story_command
from hnterminal.commands.get_comments import get_comments_command


def build_cli():
    hn_context = HNContext()
    cli_runner = ReplRunner("hnterminal", hn_context)
    cli_runner.add_commands([get_front_page_command, get_story_command, get_comments_command], namespace="Read")
    return cli_runner


def main():
    cli_runner = build_cli()
    cli_runner.run()


if __name__ == "__main__":
    main()
