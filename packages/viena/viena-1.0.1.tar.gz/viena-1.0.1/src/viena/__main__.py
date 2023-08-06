# viena/__main__.py

from viena import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)
    # dataset.app(prog_name=__app_name__)
    # container.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()