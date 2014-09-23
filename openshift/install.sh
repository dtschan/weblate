#! /bin/sh

set -e
trap "rm $OPENSHIFT_DATA_DIR/.install" EXIT

test -e $OPENSHIFT_DATA_DIR/.install && exit 0

touch $OPENSHIFT_DATA_DIR/.install

source $OPENSHIFT_HOMEDIR/python/virtenv/bin/activate

sed -e 's/Django[<>=].*/Django==1.6/' $OPENSHIFT_REPO_DIR/requirements-mandatory.txt >/tmp/requirements.txt

pip install -r /tmp/requirements.txt &&

if [ ! -s $OPENSHIFT_DATA_DIR/weblate.db ]; then
  rm -f ${OPENSHIFT_DATA_DIR}/CREDENTIALS
fi

if [ ! -s $OPENSHIFT_REPO_DIR/weblate/fixtures/initial_data.json ]; then
  mkdir -p $OPENSHIFT_REPO_DIR/weblate/fixtures
  cat <<-EOF >$OPENSHIFT_REPO_DIR/weblate/fixtures/initial_data.json
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

echo "Executing 'python $OPENSHIFT_REPO_DIR/openshift/manage.py syncdb --noinput'"
python "$OPENSHIFT_REPO_DIR"openshift/manage.py syncdb --noinput

echo "Executing 'python $OPENSHIFT_REPO_DIR/openshift/manage.py migrate'"
python "$OPENSHIFT_REPO_DIR"openshift/manage.py migrate

echo "Executing 'python $OPENSHIFT_REPO_DIR/openshift/manage.py collectstatic --noinput'"
python "$OPENSHIFT_REPO_DIR"openshift/manage.py collectstatic --noinput

if [ ! -s $OPENSHIFT_DATA_DIR/CREDENTIALS ]; then
  echo "Executing 'python $OPENSHIFT_REPO_DIR/openshift/manage.py createadmin'"
  python "$OPENSHIFT_REPO_DIR"openshift/manage.py createadmin

  echo "Generating Django Admin credentials and writing them to ${OPENSHIFT_DATA_DIR}/CREDENTIALS"
  python "$OPENSHIFT_REPO_DIR".openshift/action_hooks/secure_db.py | tee ${OPENSHIFT_DATA_DIR}/CREDENTIALS
fi

ln -sf $OPENSHIFT_REPO_DIR/openshift/wsgi.py $OPENSHIFT_REPO_DIR/wsgi/application
touch $OPENSHIFT_DATA_DIR/.installed

gear stop
gear start
