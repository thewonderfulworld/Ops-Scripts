#!/usr/bin/perl
#
# Simple script to read the host file
# This file was created on 6/7/2015
#
use File::Copy;

# Std core stuff
print "$0\n";

$FILE = "/tmp/hosts";

copy( "/etc/hosts", $FILE ) or die "The copy operation failed: $!";

open (file, $FILE);

while ( <file> ) {
    print "$_\n";
}

close (file);

exit;
