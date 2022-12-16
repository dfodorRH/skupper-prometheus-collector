from collections.abc import Generator

import httpretty as httpretty_module
import pytest


@pytest.fixture()
def httpretty() -> Generator[httpretty_module, None, None]:
    with httpretty_module.enabled(allow_net_connect=False):
        httpretty_module.reset()
        yield httpretty_module
