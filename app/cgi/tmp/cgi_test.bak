#!C:\perl\bin\perl.exe -Tw

use DBI;    
use CGI;

local $query = new CGI;

print $query->header;

my $user = "kaled";

$dbh->{RaiseError} = 1;
$dbh = DBI->connect("DBI:mysql:DineGuide;mercury;3306", $user, $password);

$strSQL = "SELECT * from Cuisine;";
$sth = $dbh->prepare($strSQL);

$rv = $sth->execute;


while($tmp_hash = $sth->fetchrow_hashref)
  {
  print "$tmp_hash->{'Name'}", "<BR>";

  }
