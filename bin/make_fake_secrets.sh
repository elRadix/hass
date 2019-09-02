#!/usr/bin/env sh
#
# This script parse real secrets.yaml-file and based on it
# generate fake one for testing reasons.
#
# Copyright (c) 2019, Andrey "Limych" Khrolenok <andrey@khrolenok.ru>
# Creative Commons BY-NC-SA 4.0 International Public License
# (see LICENSE.md or https://creativecommons.org/licenses/by-nc-sa/4.0/)
#

WDIR=$(cd `dirname $0` && pwd)
ROOT=$(dirname ${WDIR})
SEED=$$

# Define faker callback
faker() {
  local key=$3 value=$4

  if [ "$key" == "ssl_certificate" ]; then
    value='tests/example.com.fake_crt'
  elif [ "$key" == "ssl_key" ]; then
    value='tests/example.com.fake_key'
  elif [ "$key" == "time_zone" ]; then
    value='America/Los_Angeles'
  elif echo ${key} | grep -q '_\(login\|username\|password\)$'; then
    value='super_5EcREt'
  elif echo ${key} | grep -q '_\(lat\|lon\|latitude\|longitude\)$'; then
    value='00.000000'
  else
    SEED=$(expr ${SEED} + 1)
    value=$(echo ${value} | awk 'BEGIN {srand('${SEED}'); OFS = ""} { n = split($0, a, ""); for (i = 1; i <= n; i++) { if (a[i] ~ /[[:digit:]]/) { new = new int(rand() * 10) } else if (a[i] ~ /[[:alpha:]]/) { new = new sprintf("%c", int(rand() * 26 + 97)) } else { new = new a[i] } }; $0 = new; print }')
  fi

  echo "$key: \"$value\""
}



# Include parse_yaml function
. ${WDIR}/_parse_yaml.sh

# Read real yaml file and make fake one
FPATH=${ROOT}/fake_secrets.yaml
>${FPATH}
echo "#" >>${FPATH}
echo "# ATTENTION! This is autogenerated fake file. All values filled random characters." >>${FPATH}
echo "# Don't edit this file -- all changes will be lost on next file auto generation." >>${FPATH}
echo "#" >>${FPATH}
eval $(parse_yaml ${ROOT}/secrets.yaml '' 'faker \"%s\" \"%s\" \"%s\" \"%s\";') >>${FPATH}

exit
