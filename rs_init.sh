#!/bin/sh

if [ -z "$1" ]; then
	echo "Please provide domain user name like burak.ovali"
	exit
fi

git remote add rs-di_remote ssh://$1@git.corp.airties.com:29418/rs-di

#git subtree add --prefix=rs-di/ rs-di_remote master


