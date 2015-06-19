#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 Daniel Tschan <tschan@puzzle.ch>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'weblate'))
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'openshift'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'weblate.settings_openshift'

#execfile(os.path.join(
#    os.environ['OPENSHIFT_REPO_DIR'], 'openshift', 'virtualenv.py'
#))

application = get_wsgi_application()
