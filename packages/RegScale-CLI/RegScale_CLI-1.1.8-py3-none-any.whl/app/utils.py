#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports
from app.application import Application
from app.login import is_licensed
from exceptions.license_exception import LicenseException


def check_license():
    """_summary_

    Raises:
        LicenseException: _description_

    Returns:
        Application: application instance
    """
    app = Application()
    if not is_licensed(app):
        raise LicenseException(
            "This feature is limited to RegScale Enterprise, please check RegScale license"
        )
    return app
