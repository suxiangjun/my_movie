#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "junesu"
# Date: 2018-07-20
from app.models import Auth
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
a="123456"
hash_a=generate_password_hash(a)
print(len(hash_a))
b="pbkdf2:sha256:50000$hkvCmlOL$039"
print(b)
