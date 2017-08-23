#!/bin/bash 

# =--------------------------------------------------------------------------= #
# This should start with a fully operational server and (optionally) new code 
# to deoploy.
# =--------------------------------------------------------------------------= #
echo "Hello, I'm the gitlab update script."
MODULE="rpc-explorer"
BASEDIR="/bs"
BSD="${BASEDIR}/${MODULE}"
SCAFFOLD="${BASEDIR}/.scaffold/${MODULE}"

# start with an assumption of success...

RETURN=0

export PATH=$PATH:/usr/local/bin

# =--------------------------------------------------------------------------= #
# First, let's check and see who the hell I am and that I know what I am doing.
# =--------------------------------------------------------------------------= #

# initally, this is just set here.
ROLE="prod"
CLASS="gitlab"

OUTDIR=$(mktemp -d /tmp/update-XXXXXXXX)

# exec > >(tee $OUTDIR/update.log|logger -t user-data -s 2>/dev/console) 2>&1

printf "class: $CLASS\nrole: $ROLE\ndate: $(date)\n" >> $OUTDIR/info.txt

echo "I am a ${CLASS} ${ROLE} server."

if [ -z "$CLASS" ] || [ -z "$ROLE" ]; then
    echo "ERROR: I have no idea who I am, I'm out of here."
    exit 1
fi

there_are_changes() {
    # optional single argument "branch"

    UPSTREAM=${1:-'@{u}'}

    git remote update &>/dev/null 
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse "$UPSTREAM")
    BASE=$(git merge-base @ "$UPSTREAM")
    
    if [ $LOCAL = $REMOTE ]; then
        R=0
    elif [ $LOCAL = $BASE ]; then
        R=2
    else
        R=1
    fi

    return $R
}

# =--------------------------------------------------------------------------= #
# Great, I know who I am. Let's see if cf/roles knows who I am...
# =--------------------------------------------------------------------------= #
echo -n "Checking for changes in config: ";
CHANGES=0;

cd ${SCAFFOLD}/MASTER;
mkdir -p ${SCAFFOLD}/release_logs

B=0

there_are_changes &>/dev/null
B=$?
if [ $B -eq 0 ]; then
    # nothing to do
    echo "Nothing new."
elif [ $B -eq 2 ]; then
    echo "Changes!"
    CHANGES=1    
    # changes! simple pull:
    git pull &>/dev/null

    LUPDATE="${MODULE}:$(git rev-parse @)"

    cd ${SCAFFOLD}/releases

    DS=$(date +%Y%m%d%H%M%S)

    cd ${SCAFFOLD}/releases
    git clone ${SCAFFOLD}/MASTER ${MODULE}-${DS} &>/dev/null

    rm ${BSD}
    ln -s ${SCAFFOLD}/releases/${MODULE}-${DS} ${BSD}
    for F in ${BSD}/bs/update/*; do
            T=$OUTDIR/$(basename $F).out
            echo -n "Running $F: ";
            $F > $T 2>&1
            if [ $? -gt 0 ]; then
                    echo "FAILED"
                    echo " ~---=: OUT & ERR :=---~"
                    cat $T
                    echo " ~---=: <<<< >>>> :=---~"
            else
                    echo "OK"
            fi
    done
    tar -cvzf ${SCAFFOLD}/release_logs/${MODULE}-${DS}.tgz $OUTDIR
else
    echo "ERROR"
    RETURN=1
fi

rm -rf $OUTDIR

exit

