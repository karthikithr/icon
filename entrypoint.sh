#!/usr/bin/env bash

readonly AIRFLOW_SETUP_DIR='/usr/local/airflow'
readonly HOST_PORT_REGEX='(@|//)([^:]+):([0-9]+)'

die() { echo -e "$*" ; exit 1 ; }

wait_for_port() {
  local i
  local name=${1}
  local uri=${2}

  [[ "${uri}" =~ ${HOST_PORT_REGEX} ]] || \
    die "Unable to parse host/port from: ${uri}"

  read -r host port <<< "${BASH_REMATCH[@]:2}"

  for ((i=1;i<${MAX_WAIT_COUNT:=20};i++)); do
    nc -z "${host}" "${port}" > /dev/null 2>&1 && \
      return 0
    [[ ${i} -ge ${MAX_LOOP_COUNT} ]] && \
      die "$(date) - ${name} not reachable"
    echo "$(date) - waiting for ${name} (${i}/${MAX_LOOP_COUNT})"
    sleep 5
  done
}

wait_for_redis() {
  wait_for_port "Redis" "${AIRFLOW__CELERY__BROKER_URL}"
}

wait_for_postgres() {
  wait_for_port "Postgres" "${AIRFLOW__CORE__SQL_ALCHEMY_CONN}"
}

mkdir -p "${AIRFLOW_HOME}"/{config,plugins}

[[ -s "${AIRFLOW_HOME}/config/log_config.py" ]] || \
  cp ${AIRFLOW_SETUP_DIR}/log_config.py "${AIRFLOW_HOME}/config/"

cat > /airflow/plugins/plugins.py<<EOF
from custom_airflow_plugins import MyAirflowPlugin
EOF

[[ -d /airflow/dags ]] || \
  git clone \
    --single-branch \
    --branch master \
    --depth 1 \
    https://some.git.server/airflow-dags.git /airflow/dags

case "$1" in
  webserver)
    wait_for_postgres && wait_for_redis
    airflow initdb
    python3 ${AIRFLOW_SETUP_DIR}/setup_connections.py
    exec airflow webserver
    ;;
  worker|scheduler)
    wait_for_postgres && wait_for_redis
    wait_for_redis
    sleep 30 # pause to let webserver finish (initdb and setup_connections)
    exec airflow "$@"
    ;;
  flower)
    wait_for_redis
    exec airflow "$@"
    ;;
  version)
    exec airflow "$@"
    ;;
  *)
    exec "$@"
    ;;
esac
