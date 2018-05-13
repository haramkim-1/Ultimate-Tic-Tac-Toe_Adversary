#!/usr/bin/env bash

for path in *; do #loop over all isoRMSD directories
    	[ -d "${path}" ] || continue # if not a directory, skip
    	[ "old" != "${path}" ] || continue # skip old files directory
	[ "plots" != "${path}" ] || continue # skip old files directory
	dirname="$(basename "${path}")"	

	echo "$path"

	#copy gnuplot script into directory
	cp gnuplotPlottingScript.gp $dirname

	#enter directory
	cd $dirname

	#generate plotting data
	cat stdout_log.txt | grep "Best fitness:" | awk '{ print $3 }' > best_fitness.tsv
	cat stdout_log.txt | grep "average fitness:" | awk '{ print $4 ,"\t", $6 }' > average_fitness.tsv
	
	#run plotting script
	gnuplot gnuplotPlottingScript.gp

	#move output to plots directory
	#mv best.png ../plots/$(echo $dirname | sed -e 's/.*_//')_best.png
	#mv average.png ../plots/$(echo $dirname | sed -e 's/.*_//')_average.png
	mv combined.png ../plots/$(echo $dirname | sed -e 's/.*_//')_combined.png
	
	#remove script
	rm gnuplotPlottingScript.gp

	#leave
	cd ..
done
