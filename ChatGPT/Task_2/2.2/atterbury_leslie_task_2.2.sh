#!/bin/bash

# use to quickly change which version is being tested
COMPILERNAME="USER INPUT"
read -p "Enter compiler name: " COMPILERNAME

# delete old data
rm -rf "$COMPILERNAME"Results >/dev/null &

wait

# make the files and move them around
mkdir "$COMPILERNAME"Results

mkdir {Espresso,Espresso_Plus,Espresso_Star}

mkdir {Good,Bad}
mv Good Espresso
mv Bad Espresso

mkdir {Good,Bad}
mv Good Espresso_Plus
mv Bad Espresso_Plus

mkdir {Good,Bad}
mv Good Espresso_Star
mv Bad Espresso_Star

mv Espresso 		"$COMPILERNAME"Results
mv Espresso_Plus 	"$COMPILERNAME"Results
mv Espresso_Star 	"$COMPILERNAME"Results

# $1 is the test file name (GoodTests or BadTests)
# $2 is the compiler name
# $3 is the output file path
# $4 is the espresso version type
doTests () {
	# checks if there are tests in the directory. if there are none, say so
	if [ "$(ls -A ./tests/$4/$1)" ]; then
		# iterates through the tests and writes the output to a designated text file
		for i in ./tests/$4/$1/*
		do
			FILENAME="${i##*/}"
			TESTNAME="${FILENAME%%.*}"
			FILENAME="$TESTNAME"
			
			echo ""$2" is doing test $TESTNAME."
			
			touch "$FILENAME".txt
			./$2 "$i" > "$FILENAME".txt
			mv "$FILENAME".txt $3
		done
	else
		echo "No tests in ./tests/$4/$1 were found."
	fi
} 

# get all the results from the tests

doTests GoodTests $COMPILERNAME "$COMPILERNAME"Results/Espresso/Good Espresso
doTests BadTests $COMPILERNAME "$COMPILERNAME"Results/Espresso/Bad Espresso
doTests GoodTests $COMPILERNAME "$COMPILERNAME"Results/Espresso_Plus/Good Espresso_Plus
doTests BadTests $COMPILERNAME "$COMPILERNAME"Results/Espresso_Plus/Bad Espresso_Plus
doTests GoodTests $COMPILERNAME "$COMPILERNAME"Results/Espresso_Star/Good Espresso_Star
doTests BadTests $COMPILERNAME "$COMPILERNAME"Results/Espresso_Star/Bad Espresso_Star
