#! /bin/sh

export INSTALL=1
gear deploy >$OPENSHIFT_DATA_DIR/install.log && touch $OPENSHIFT_DATA_DIR/.installed
