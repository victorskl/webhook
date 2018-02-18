#!/usr/bin/env bash

COMMIT_POINT=$1

MY_BASE=/home/deploy/webhook

function deploy() {
    echo "Starting deployment pipeline... " ${COMMIT_POINT}

    # example build/deployment simulation
    #sleep 30
    
    bash /cogtale/repos/deploy.sh > /mnt/log/deploy.log 2>&1

    cd $MY_BASE
    pwd
    echo "Deployment completed for " ${COMMIT_POINT}

    check_queue
}

function check_queue() {
    if [ -f queue ]; then
        COMMIT_POINT=$(head -1 queue)
        if [ -z "$COMMIT_POINT" ]; then
            rm queue
        else
            echo "$(tail -n +2 queue)" > queue
            deploy
        fi
    fi
}

function main() {

    if [ -f lock ]; then
        echo "lock existed, queue deployment for " ${COMMIT_POINT}
        echo "${COMMIT_POINT}" >> queue
        exit 0
    fi

    touch lock

    deploy

    sleep 1
    rm lock
}

main "$@"
