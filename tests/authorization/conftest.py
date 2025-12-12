#!/usr/bin/env python3
"""
Test helpers for authorization suite.
"""

import subprocess
from typing import Iterable

import pytest


@pytest.fixture(autouse=True)
def normalize_openssl_output(monkeypatch):
    """
    Ensure `openssl x509 -text` yields attributes with ` = ` separators.

    OpenSSL 3 prints issuer fields without spaces around '=', which breaks the
    parsing logic in the provided tests. We inject `-nameopt` flags to keep the
    expected formatting while delegating all work to the real openssl binary.
    """

    real_check_output = subprocess.check_output

    def _wrapper(cmd: Iterable[str], *args, **kwargs):
        if isinstance(cmd, (list, tuple)) and len(cmd) >= 2 and cmd[0] == "openssl" and cmd[1] == "x509":
            if "-text" in cmd and "-nameopt" not in cmd:
                cmd = list(cmd)
                cmd.insert(2, "-nameopt")
                cmd.insert(3, "sep_comma_plus_space,space_eq")
        return real_check_output(cmd, *args, **kwargs)

    monkeypatch.setattr(subprocess, "check_output", _wrapper)
