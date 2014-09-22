#! /bin/sh

touch $OPENSHIFT_DATA_DIR/.install
> $OPENSHIFT_DATA_DIR/install.log
gear build >$OPENSHIFT_DATA_DIR/install.log && gear stop && gear start && touch $OPENSHIFT_DATA_DIR/.installed && rm OPENSHIFT_DATA_DIR/.install
