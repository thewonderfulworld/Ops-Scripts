#!/bin/bash
#
# Simple script to make the passwd file readable
# This file was created on 6/7/2015
#

# Std core stuff
echo $(basename $0)
FILE=/tmp/awk_pass
trap 'rm -f $FILE;' EXIT
trap 'echo "SIG 15 deteted $0 is terminating" ; exit 2' ; 15

cp /etc/passwd $FILE

# Example formatting
#Prints rows 1 to 10 on display
#awk -F":"  ' NR==1, NR==10  { print $1,$3 } ' /etc/passwd

#Print Length of word in column 1
#awk -F":"  ' NR==1, NR==10  { print length($1),$3 } ' /etc/passwd

#Format Print Header and then Length of word in column 1
#awk -F":"  '
#BEGIN { printf "%-8s %3s\n", "User", "UID" }
#NR==1, NR==10  { printf "%-8s %3d\n", $1,$3 } ' /etc/passwd

# Let's Do It
#Format Print Header and then Length of word in column 1
awk -F":"  '
BEGIN {
printf "=============================================================================\n"
printf "%-15s %4s %6s %28s %18s\n", "User", "UID", "GID", "Home", "Shell"
printf "=============================================================================\n"
}
{ printf "%-15s %4d %6s %28s %18s\n", $1,$3,$4,$6,$7 } ' $FILE


exit 0
