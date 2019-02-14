#!/usr/bin/env bash
set -e
TAG="PERF-TEST"

function print_msg ()
{
    datetime=`date "+%Y-%m-%d %H:%M:%S"`
    echo "$datetime: $1"
}

function replace_generic_version ()
{
    file="$1"
    _line=`awk '/version:/{print NR;exit}' $file`
    replacement="version: $TAG"
    # Escape backslash, forward slash and ampersand for use as a sed replacement.
    replacement_escaped=$( echo "$replacement" | sed -e 's/[\/&]/\\&/g' )
    sed -i '' "${_line}s/.*/$replacement_escaped/" "$file"
}

function prepare_sck_charts ()
{
    print_msg "Preparing SCK charts for deployment"
    repos_array=( "../helm-chart/splunk-connect-for-kubernetes" "../helm-chart/splunk-kubernetes-logging"
                  "../helm-chart/splunk-kubernetes-metrics" "../helm-chart/splunk-kubernetes-objects" )
    sub_repos_array=( "../helm-chart/splunk-kubernetes-logging"
                  "../helm-chart/splunk-kubernetes-metrics" "../helm-chart/splunk-kubernetes-objects" )

    for repo in "${repos_array[@]}"
    do
      filename="${repo}/Chart.yaml"
      replace_generic_version $filename
    done

    mkdir ../helm-artifacts
    mkdir ../helm-chart/splunk-connect-for-kubernetes/charts

    for sub_repo in "${sub_repos_array[@]}"
    do
      cp -rp $sub_repo ../helm-chart/splunk-connect-for-kubernetes/charts
    done

    for repo in "${repos_array[@]}"
    do
      helm package -d ../helm-artifacts $repo
    done
}

function clean_artifacts ()
{
    print_msg "Cleaning all temporary build artifacts"
    rm -r ../helm-artifacts
    rm -r ../helm-chart/splunk-connect-for-kubernetes/charts
}

function deploy_sck ()
{
    print_msg "Deploying SCK"
    prepare_sck_charts
    print_msg "Installing the SCK build artifacts on the kubernetes cluster"
    helm install --name=perf-test -f perf_test_sck_values.yml ../helm-artifacts/splunk-connect-for-kubernetes*.tgz
    clean_artifacts
}

function clean_sck ()
{
    print_msg "Cleaning SCK"
    if [ "`helm ls`" == "" ]; then
       print_msg "Nothing to clean, ready for deployment"
    else
       helm delete --purge $(helm ls --short)
    fi
}

function usage ()
{
cat << EOF
Usage: $0 options
    OPTIONS:
    --help    # Show this message
    --deploy   # Deploy SCK
    --clean    # Clean SCK
EOF
exit 1
}

for arg in "$@"; do
    shift
    case "$arg" in
        "--help")
            set -- "$@" "-h"
            ;;
        "--deploy")
            set -- "$@" "-s"
            ;;
        "--clean")
            set -- "$@" "-p"
            ;;
        *)
            set -- "$@" "$arg"
    esac
done

cmd=

while getopts "hsropdlnc:i:" OPTION
do
    case $OPTION in
        h)
            usage
            ;;
        s)
            cmd="deploy"
            ;;
        p)
            cmd="clean"
            ;;
        *)
            usage
            ;;
    esac
done

if [[ "$cmd" == "deploy" ]]; then
    deploy_sck
elif [[ "$cmd" == "clean" ]]; then
    clean_sck
else
    usage
fi