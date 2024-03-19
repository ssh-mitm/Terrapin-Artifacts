#!/bin/bash

function stop_and_delete_containers {
  echo "[+] Stopping and removing any remaining artifact containers"
  for container in "terrapin-artifacts-server" "terrapin-artifacts-poc" "terrapin-artifacts-client" "terrapin-artifacts-server-direct" "terrapin-artifacts-server-poc" "terrapin-artifacts-client-direct" "terrapin-artifacts-client-poc"
  do
    docker stop $container > /dev/null 2>&1
    docker rm $container > /dev/null 2>&1
  done
}

function remove_artifact_images {
  echo "[+] Removing artifact images"
  docker images --format "{{.Repository}}:{{.Tag}}" | grep terrapin-artifacts | xargs docker image rm "{}" > /dev/null 2>&1
}

stop_and_delete_containers
remove_artifact_images