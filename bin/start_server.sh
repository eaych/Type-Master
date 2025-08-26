# get the directory of the script
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

help() {
    cat <<EOF

Usage: 
    $0 <mode>

Description:
    Start a TypeMaster server in a supported mode.

Arguments:
    mode            Must be either "basic" or "advanced".
EOF
}

command="python -m TypeMaster"
if [ "$1" = "basic" ]; then
    PYTHONPATH="$SCRIPT_DIR/../src/" python -m TypeMaster.basic_server
elif [ "$1" = "advanced" ]; then
    PYTHONPATH="$SCRIPT_DIR/../src/" python -m TypeMaster.adv_server
else
    help
fi