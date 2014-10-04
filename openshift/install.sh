#! /bin/sh

# Log and execute given command, identing its output for easy filtering.
function sh {
  echo "Executing '$1'"
  /bin/sh -c "$1" 2>&1 | sed -e 's/^/  /'
}

set -e
trap "rm $OPENSHIFT_DATA_DIR/.install" EXIT

test -e $OPENSHIFT_DATA_DIR/.install && exit 0

touch $OPENSHIFT_DATA_DIR/.install

source $OPENSHIFT_HOMEDIR/python/virtenv/bin/activate
export PYTHONUNBUFFERED=1

sed -e 's/Django[<>=].*/Django==1.7/' $OPENSHIFT_REPO_DIR/requirements-mandatory.txt >/tmp/requirements.txt

pip install -r /tmp/requirements.txt &&

if [ ! -s $OPENSHIFT_DATA_DIR/weblate.db ]; then
  rm -f ${OPENSHIFT_DATA_DIR}/CREDENTIALS
fi

if [ ! -s $OPENSHIFT_REPO_DIR/weblate/fixtures/site_data.json ]; then
  mkdir -p $OPENSHIFT_REPO_DIR/weblate/fixtures
  cat <<-EOF >$OPENSHIFT_REPO_DIR/weblate/fixtures/site_data.json
    [{
        "pk": 1,
        "model": "sites.site",
        "fields": {
            "name": "${OPENSHIFT_APP_DNS}",
            "domain":"${OPENSHIFT_APP_DNS}"
        }
    }]
	EOF
fi

sh "python ${OPENSHIFT_REPO_DIR}/openshift/manage.py syncdb --noinput"

sh "python ${OPENSHIFT_REPO_DIR}/openshift/manage.py migrate"

sh "python ${OPENSHIFT_REPO_DIR}/openshift/manage.py loaddata site_data"

sh "python ${OPENSHIFT_REPO_DIR}/openshift/manage.py collectstatic --noinput"

if [ ! -s $OPENSHIFT_DATA_DIR/CREDENTIALS ]; then
  echo "Generating Django Admin credentials and writing them to ${OPENSHIFT_DATA_DIR}/CREDENTIALS"
  sh "python ${OPENSHIFT_REPO_DIR}/openshift/manage.py createadmin"
  sh "python ${OPENSHIFT_REPO_DIR}/.openshift/action_hooks/secure_db.py | tee ${OPENSHIFT_DATA_DIR}/CREDENTIALS"
fi

ln -sf $OPENSHIFT_REPO_DIR/openshift/wsgi.py $OPENSHIFT_REPO_DIR/wsgi/application
touch $OPENSHIFT_DATA_DIR/.installed

gear stop
gear start
