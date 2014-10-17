#! /bin/sh

# Split first argument with delimiter '#'
OLDIFS=$IFS
IFS='#'
set -- $1
IFS=$OLDIFS

URL="$1"
BRANCH="${2:-master}"

OLD_HEAD=`git rev-parse "$BRANCH"`
cd ${OPENSHIFT_HOMEDIR}/git/${OPENSHIFT_APP_NAME}.git
echo git fetch "$URL" "$BRANCH"
pwd

exit 0

if ! git cat-file -e "$BRANCH":.openshift 2>/dev/null; then
  echo "Fatal error: Branch $BRANCH of repository at $URL doesn't contain an OpenShift configuration!" >&2
  exit 1
fi

gear deploy --hot-deploy "$BRANCH"
