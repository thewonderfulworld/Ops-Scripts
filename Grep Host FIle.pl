#!/usr/bin/perl
#
# Simple script to read the host file
# This file was created on 6/7/2015
#
use strict;
use warnings;

my $target;
my @array;
my @resultarray;


$target = "/tmp/hosts";

# Open file and read contents into single array
open FILE, "<", $target or die $!;
@array = <FILE>;

# Grep for the local host in the array
@resultarray = grep /127.0.0.1/, @array;

print "@resultarray\n";

