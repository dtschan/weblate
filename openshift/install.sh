#! /bin/sh

test -e $OPENSHIFT_DATA_DIR/.install && exit 0

touch $OPENSHIFT_DATA_DIR/.install

source $OPENSHIFT_HOMEDIR/python/virtenv/bin/activate

sed -e 's/Django[<>=].*/Django==1.6/' $OPENSHIFT_REPO_DIR/requirements.txt >/tmp/requirements.txt

> $OPENSHIFT_DATA_DIR/install.log

pip install -r /tmp/requirements.txt >$OPENSHIFT_DATA_DIR/install.log && \
ctl_all restart && \
touch $OPENSHIFT_DATA_DIR/.installed && \
rm OPENSHIFT_DATA_DIR/.install
