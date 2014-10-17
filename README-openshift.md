Weblate on OpenShift
====================

This repository contains a configuration for the OpenShift platform as a service product which facilitates easy installation
of Weblate on OpenShift Online (https://openshift.com), OpenShift Enterprise (https://www.openshift.com/products/enterprise)
and OpenShift Origin (https://www.openshift.com/products/origin).

Free hosting on openshift online

rhc add-cartridge cron-1.4

Updating:

Documentation
-------------

Detailed documentation for Weblate is available in ``docs`` directory in the sources.

The documentation can be also viewed online on
http://docs.weblate.org/.

TODO: OpenShift Documentation

Prerequisites
-------------

1. OpenShift account
2. OpenShift client tools

Installation
------------

The following section describes how to install Weblate on OpenShift Online.
Installation on OpenShift Enterprise and OpenShift Origin is carried out analogous.

rhc -a*APP* create -t python-2.7 --from-code https://github.com/nijel/weblate.git#*TAG*

Where *APP* is a name of your choosing, e.g. weblate, and *TAG* is used to identify the version of Weblate to install, e.g. weblate-2.0
A list of available versions is available here: https://github.com/nijel/weblate/tags. Please note that only version 2.0 and newer can
be installed on OpenShift, as older versions don't include the necessary configuration files.



Installation and setup instructions are provided in our manual, check
quick setup guide:

http://docs.weblate.org/en/latest/admin/quick.html

Configuration
-------------

After installation on OpenShift Weblate is ready to use and preconfigured as follows:

* SQLite embedded database (DATABASES)
* Random admin password
* Random Django secret key (SECRET_KEY)
* Indexing offloading if the cron cartridge is installed (OFFLOAD_INDEXING)
* Weblate machine translations for suggestions bases on previous translations (MACHINE_TRANSLATION_SERVICES)
* Source language for machine translations set to "en-us" (SOURCE_LANGUAGE)
* Weblate directories (STATIC_ROOT, GIT_ROOT, WHOOSH_INDEX, HOME, Avatar cache) set according to OpenShift requirements/conventions
* Django site name and ALLOWED_HOSTS set to DNS name of your OpenShift application
* Email sender addresses set to no-reply@*OPENSHIFT_CLOUD_DOMAIN*, where *OPENSHIFT_CLOUD_DOMAIN* is the domain OpenShift runs under. In case of OpenShift Online it's rhcloud.com.




Bugs
----

Please report bugs to https://github.com/nijel/weblate/issues.
