from replbuilder import ReplRunner
from hnterminal.hncontext import HNContext
from hnterminal.commands import READ_COMMANDS, WRITE_COMMANDS


def build_cli():
    hn_context = HNContext()
    cli_runner = ReplRunner("hnterminal", hn_context)
    cli_runner.add_commands(READ_COMMANDS, namespace="Read")
    cli_runner.add_commands(WRITE_COMMANDS, namespace="Write")
    cli_runner.add_commands(hn_context.get_context_commands(), namespace="Cache")
    cli_runner.add_aliases({
        "fp": "get_front_page",
        "fps": "get_front_page -t SHOW",
        "fpa": "get_front_page -t ASK",
        "gt": "get_tree",
        "gu": "get_user -sn 10"
    })
    return cli_runner


def main():
    cli_runner = build_cli()
    cli_runner.run()


if __name__ == "__main__":
    main()
