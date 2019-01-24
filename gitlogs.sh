#!/usr/bin/env bash

# Gets gitlogs from repositories. Adds header, appends to the same file, if the same repo, otherwise creates new file.
# Saved in ${path_to_file}/Taxbreak/year/month/

### Functions ###

help_vars(){
    echo -e "\nList of supported paramerters:"
    echo "--path_to_repo: Path to the repository."
    echo "--path_to_file: Path with filename where the git log should be saved, i.e. ${HOME} or /home/user/desiredfolder"
    echo "--user_email: Users email. Used for getting the git logs from that author, i.e. helpme@withgitpls.nokia.com"
    echo "--since_date: Date since when the git logs should be gathered, i.e. 01.12.2018"
    echo -e "--branch: Optional, should the branch be changed in repository folder.\n"
}

pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}


### Main ###

for arg in "$@"
do
    case "${arg}" in
            --path_to_repo=*)
                path_to_repo="${arg#*=}"
                shift
                ;;
            --path_to_file=*)
                path_to_file="${arg#*=}"
                shift
                ;;
            --user_email=*)
                user_email="${arg#*=}"
                shift
                ;;
            --since_date=*)
                since_date="${arg#*=}"
                shift
                ;;
            --branch=*)
                branch="${arg#*=}"
                shift
                ;;
            --help)
                help_vars
                shift
                ;;
            *)
                echo "Unknown parameter: ${arg%=*}"
                help_vars
                exit 1
                ;;
    esac
done

pushd "${path_to_repo}"

echo "Current repository folder: $(pwd)"
git_url=$(git config --get remote.origin.url)
repo_name=$(basename git rev-parse --show-toplevel)
if [[ ! -z branch ]]; then git checkout "${branch}"; fi

git_branch=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: ${git_branch} on repository: ${git_url}"
git_log=$(git log -p --author="${user_email}" --since="${since_date}")

tag=$(printf '#%.0s' {1..100})

filename="gitlog_${repo_name}_$(date +%m-%Y).txt"
filelocation="${path_to_file}/Taxbreak/$(date +%Y)/$(date +%b)/"

if [[ ! -d $"filelocation" ]]; then mkdir -p ${filelocation}; fi

{
    echo "${tag}"
    echo "url:${git_url}"
    echo "branch:${git_branch}"
    echo "${tag}"
    echo ""
    echo "${git_log}"
    echo ""
} >> "${filelocation}/${filename}"

popd