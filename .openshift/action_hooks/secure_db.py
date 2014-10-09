#!/usr/bin/env python
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

# Copyright 2011-2014 Red Hat Inc. and/or its affiliates and other contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,  
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib, imp, os, sqlite3

# Load the OpenShift helper library
lib_path      = os.environ['OPENSHIFT_REPO_DIR'] + 'openshift/'
modinfo       = imp.find_module('openshiftlibs', [lib_path])
openshiftlibs = imp.load_module('openshiftlibs', modinfo[0], modinfo[1], modinfo[2])

# Open the database
conn = sqlite3.connect(os.environ['OPENSHIFT_DATA_DIR'] + '/weblate.db')
c    = conn.cursor()

# Grab the default security info
pw_info = 'sha1$9ddf7$465f37505d88fcf05961eab98d7e0a2eabbc9d70'

# The password is stored as [hashtype]$[salt]$[hashed]
pw_fields = pw_info.split("$")
hashtype  = pw_fields[0]
old_salt  = pw_fields[1]
old_pass  = pw_fields[2]

# Randomly generate a new password and a new salt
# The PASSWORD value below just sets the length (12)
# for the real new password.
old_keys = { 'SALT': old_salt, 'PASS': '123456789ABC' }
use_keys = openshiftlibs.openshift_secure(old_keys)

# Encrypt the new password
new_salt    = use_keys['SALT']
new_pass    = use_keys['PASS']
new_hashed  = hashlib.sha1(new_salt + new_pass).hexdigest()
new_pw_info = "$".join([hashtype,new_salt,new_hashed])

# Update the database
c.execute('UPDATE AUTH_USER SET password = ? WHERE username = ?', [new_pw_info, 'admin'])
conn.commit()
c.close()
conn.close()

# Print the new password info
print "Django application credentials:\n\tuser: admin\n\t" + new_pass
