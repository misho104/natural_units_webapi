#!/usr/bin/perl

use strict;
use warnings;
use JSON qw/ encode_json /;

our $COMMAND = 'units -v -f /home/natural.units';

my $query = decode($ENV{QUERY_STRING});
if($query =~ /@.*@/){ error("invalid syntax"); }
if(length($query) > 200){ error("query too long"); }

my ($from, $to) = split(/@/, $query);
strip($from, $to);

my $result = ($to eq '') ? `$COMMAND "$from"` : `$COMMAND "$from" "$to"`;

if($ENV{REQUEST_URI} =~ /\/text\?/){ # plain text output
  my $header = ($to eq '') ? "$from" : "$from @ $to";
  print "Content-type: text/plain\n\n$header:\n$result";
}else{ # json output
  print "Content-type: application/json\n\n";
  print encode_json({ from => $from, to => $to, result => $result});
}
exit 0;

sub decode { # and sanitize
  my $s = shift;
  $s =~ s/%([2-7][\dA-Fa-f])/chr hex $1/eg;

  my $tmp = $s;
  $tmp =~ s/[\w \-\*\/\+^\(\)\|@]//g;
  if($tmp ne ''){
    error("Unallowed letters are used: " . join(" ", split(//, $tmp)));
  }
  return $s;
}

sub strip{
  foreach(@_){ s/^\s+//; s/\s+$//; s/\s+/ /g; }
}

sub error{
  print "Content-type: text/plain\n\n$_[0]";
  exit 0;
}
