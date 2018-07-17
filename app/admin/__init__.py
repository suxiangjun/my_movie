#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "junesu"
# Date: 2018-07-05
from flask import Blueprint

admin=Blueprint("admin",__name__)

import app.admin.views
