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

import imp, os, re
import openshiftlibs
from settings_example import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'weblate.db'),
        'ATOMIC_REQUESTS': True,
    }
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TIME_ZONE = None

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'wsgi', 'static')

default_keys = { 'SECRET_KEY': 'jm8fqjlg+5!#xu%e-oh#7!$aa7!6avf7ud*_v=chdrb9qdco6(' }
 
# Replace default keys with dynamic values if we are in OpenShift
use_keys = default_keys
use_keys = openshiftlibs.openshift_secure(default_keys)
 
SECRET_KEY = use_keys['SECRET_KEY']

GIT_ROOT = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'repos')

# Offload indexing: if the cron cartridge is installed the preconfigured job in .openshift/cron/minutely/update_index updates the index.
if os.environ.get('OPENSHIFT_CRON_DIR', False):
  OFFLOAD_INDEXING = True
else:
  OFFLOAD_INDEXING = False

# Where to put Whoosh index
WHOOSH_INDEX = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'whoosh-index')

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

if os.environ.get('OPENSHIFT_CLOUD_DOMAIN', False):
  SERVER_EMAIL = 'no-reply@%s' % os.environ['OPENSHIFT_CLOUD_DOMAIN']
  DEFAULT_FROM_EMAIL = 'no-reply@%s' % os.environ['OPENSHIFT_CLOUD_DOMAIN']

ALLOWED_HOSTS = [os.environ['OPENSHIFT_APP_DNS']]

os.environ['HOME'] = os.environ['OPENSHIFT_DATA_DIR']

# Import environment variables prefixed with WEBLATE_ as weblate settings
weblateVar = re.compile('^WEBLATE_[A-Za-z0-9_]+$')
for name, value in os.environ.items():
  if weblateVar.match(name):
    exec("%s=os.environ[name]" % name[8:])

#try:
#  from settings_local import *
#except ImportError:
#  pass

#try:
#  imp.load_source('settings_local2', os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'settings_local.py'))
#  from settings_local2 import *
#except IOError:
#  pass
