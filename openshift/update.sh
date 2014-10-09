#! /bin/sh

# Split first argument with delimiter '#'
OLDIFS=$IFS
IFS='#'
set -- $1
IFS=$OLDIFS

URL="$1"
BRANCH="${2:-master}"

cd ${OPENSHIFT_HOMEDIR}/git/${OPENSHIFT_APP_NAME}.git
OLD_HEAD=`git rev-parse master`
git fetch --force "$URL" "$BRANCH":master
HEAD=`git rev-parse master`

if [ "$HEAD" == "$OLD_HEAD" ]; then
	echo "Already up-to-date."
  exit 0
fi

if ! git cat-file -e master:.openshift 2>/dev/null; then
  echo "Fatal error: Branch $BRANCH of repository at $URL doesn't contain an OpenShift configuration!" >&2
  exit 1
fi

gear deploy --hot-deploy master
