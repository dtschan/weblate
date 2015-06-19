FROM centos:centos7
MAINTAINER Daniel Tschan <tschan@puzzle.ch>

RUN yum -y update; yum clean all
RUN yum -y install epel-release
RUN yum -y install python-pip python-django python-gunicorn python-lxml python-pillow git sqlite libxml2-devel libxslt-devel gcc python-devel libjpeg-turbo-devel openjpeg-devel freetype-devel zlib-devel libtiff-devel gettext; yum clean all

ENV OPENSHIFT_DATA_DIR=/var/lib/weblate OPENSHIFT_REPO_DIR=/opt/weblate HOME=/opt/weblate

RUN groupadd -r default -f -g 1001 && useradd -u 1001 -r -g default -d ${HOME} -s /sbin/nologin -c "Default Application User" default && mkdir -p /opt/weblate /var/lib/weblate

ADD requirements*.txt setup.py README.rst /opt/weblate/
ADD weblate /opt/weblate/weblate/
ADD openshift /opt/weblate/openshift/
ADD locale /opt/weblate/locale/

RUN /opt/weblate/openshift/install.sh

RUN chown -R 1001:1001 /opt/weblate /var/lib/weblate

USER 1001

#run sed -e 's/Django[<>=]\+.*/Django>=1.8,<1.9/' /opt/weblate/requirements.txt >/tmp/requirements.txt

#run pip install -U -r /tmp/requirements.txt

# Install optional dependencies without failing if some can't be installed.
#run 'while read line; do \
#  if [[ $line != -r* ]] && [[ $line != \#* ]]; then \
#    echo pip install $line || true; \
#  fi; \
#done < requirements-optional.txt'

EXPOSE 8080

CMD ["/usr/bin/gunicorn", "openshift.wsgi", "--bind=0.0.0.0:8080", "--access-logfile=-"]
