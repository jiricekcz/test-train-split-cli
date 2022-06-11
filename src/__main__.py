from pre_run import pre_cli_only, pre_use


pre_use()
if __name__ == "__main__":
    pre_cli_only()
    from cli import CLI
    cli = CLI()
    cli.run()

