# get the directory of the script
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

help() {
    cat <<EOF

Usage: 
    $0 [-h,--help]

Description:
    Start a TypeMaster client.

Options:
    -h, --help          Display this message
EOF
}

if [ $# -ge 1 ]; then
    help
    exit 0
else
    PYTHONPATH="$SCRIPT_DIR/../src/" python -m TypeMaster.client
    echo "Client running"
fi
