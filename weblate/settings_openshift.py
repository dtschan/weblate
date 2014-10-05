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

import settings_example
import os

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'weblate.db'),
        # We want transactions on SQLite
        'ATOMIC_REQUESTS': True,
    }
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TIME_ZONE = None

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'wsgi', 'static')

default_keys = { 'SECRET_KEY': 'jm8fqjlg+5!#xu%e-oh#7!$aa7!6avf7ud*_v=chdrb9qdco6(' }
 
# Replace default keys with dynamic values if we are in OpenShift
use_keys = default_keys
imp.find_module('openshiftlibs')
import openshiftlibs
use_keys = openshiftlibs.openshift_secure(default_keys)
 
SECRET_KEY = use_keys['SECRET_KEY']

GIT_ROOT = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'repos')

# Offload indexing: if the cron cartridge is installed the preconfigured job in .openshift/cron/minutely/update_index updates the index.
if os.environ.get('OPENSHIFT_CRON_DIR', False):
  OFFLOAD_INDEXING = True
else:
  OFFLOAD_INDEXING = False

SOURCE_LANGUAGE = 'en-us'

# List of machine translations
MACHINE_TRANSLATION_SERVICES = (
#     'weblate.trans.machine.apertium.ApertiumTranslation',
#     'weblate.trans.machine.glosbe.GlosbeTranslation',
#     'weblate.trans.machine.google.GoogleTranslation',
#     'weblate.trans.machine.google.GoogleWebTranslation',
#     'weblate.trans.machine.microsoft.MicrosoftTranslation',
#     'weblate.trans.machine.mymemory.MyMemoryTranslation',
#     'weblate.trans.machine.opentran.OpenTranTranslation',
#     'weblate.trans.machine.tmserver.AmagamaTranslation',
#     'weblate.trans.machine.tmserver.TMServerTranslation',
     'weblate.trans.machine.weblatetm.WeblateSimilarTranslation',
     'weblate.trans.machine.weblatetm.WeblateTranslation',
)

SERVER_EMAIL = 'no-reply@%s' % os.environ['OPENSHIFT_CLOUD_DOMAIN']
DEFAULT_FROM_EMAIL = 'no-reply@%s' % os.environ['OPENSHIFT_CLOUD_DOMAIN']

ALLOWED_HOSTS = [os.environ['OPENSHIFT_APP_DNS']]

os.environ['HOME'] = os.environ['OPENSHIFT_DATA_DIR']
