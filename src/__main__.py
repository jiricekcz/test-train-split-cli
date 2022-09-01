from pre_run import pre_cli_only, pre_use
from cli import CLI 
from api import SplitManager # Exported for use in other modules
pre_use()
if __name__ == "__main__":
    pre_cli_only()
    cli = CLI()
    cli.run()
