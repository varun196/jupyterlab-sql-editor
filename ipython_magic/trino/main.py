import pathlib
import shutil
import subprocess
import sys
import logging
from jupyter_lsp.specs.config import load_config_schema
from jupyter_lsp.types import LanguageServerManagerAPI

NODE_LOCATION = (
    shutil.which("node") or
    shutil.which("node.exe") or
    shutil.which("node.cmd")
)
NODE = str(pathlib.Path(NODE_LOCATION).resolve())
mgr = LanguageServerManagerAPI()
# If jupyterlab-lsp has difficulty finding your sql-language-server
# installation, specify additional node_modules paths
mgr.extra_node_roots = ["/usr/local/lib/"]
NODE_MODULE = KEY = "sql-language-server"
SCRIPTS = ["dist", "bin", "cli.js"]
PATH_TO_BIN_JS = mgr.find_node_module(NODE_MODULE, *SCRIPTS)


def main():
    logging.info(NODE)
    logging.info(PATH_TO_BIN_JS)
    p = subprocess.Popen(
        [NODE, PATH_TO_BIN_JS, *sys.argv[1:]],
        stdin=sys.stdin, stdout=sys.stdout
    )
    sys.exit(p.wait())


def load(app):
    logging.info(NODE)
    logging.info(PATH_TO_BIN_JS)
    return {
        "trino-language-server": {
            "version": 2,
            "argv": ["trino_language_server", "up", "--method", "stdio"],
            "languages": ["trino"],
            "display_name": "Trino language server",
            "mime_types": [
                "application/trino", "application/x-trino"
            ],
            "config_schema": load_config_schema(KEY),
        }
    }


if __name__ == "__main__":
    main()