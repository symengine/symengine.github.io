#!/usr/bin/env bash
if ! [[ $1 =~ .*rake.* ]]; then
	echo "Provide a rake command"
elif ! $2; then
	echo "Wrap your command in a string"
else
	start_time=$(date +%s)
	$1
	end_time=$(date +%s)
	echo execution time was $(($end_time - $start_time)) s, which is $(bc <<<"scale=3; $(($end_time - $start_time))/60") minutes.
fi
