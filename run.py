import contextlib

import uvicorn

from freyr.constants import constants


def main() -> None:
    with contextlib.suppress(KeyboardInterrupt):
        uvicorn.run(
            "freyr.__main__:app",
            host=constants.settings.website.host,
            port=constants.settings.website.port,
            use_colors=True,
            server_header=False,
            reload=constants.settings.website.reload,
            log_config=None,
        )


if __name__ == "__main__":
    main()
