import pam
import os
import utils
from functools import cache
import logging


class auth:
    def __init__(self):
        if os.uname().sysname != "Linux":
            raise RuntimeError("auth_pam only work on linux")
        if os.getuid() != 0:
            logging.warning("Run as a non-root user,pam may not work")

    @cache
    def do_auth(self, user, passwd):
        if user == "" or passwd == "":
            return False
        return pam.authenticate(user, passwd)


PROVIDE = {"auth": auth}
