#!/usr/bin/perl -Tw

use lib split /\s/, do './inc.pl';

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use ConfigReader::Simple;
use HTML::Template;

my $config = ConfigReader::Simple->new("../conf/db.conf", 
				[qw(dingid_db username password)])
				or croak "screwed key for config";
$config->parse() or croak "unable to parse";
       
local $conn = $config->get("dingid_db");
local $purse = $config->get("username");
local $psswd = $config->get("password");

local $query = new CGI;

local $templ_preferences = HTML::Template->new(filename => '../tmpl/preferences.tmpl');

local $templ_message = HTML::Template->new(filename => '../tmpl/dineguide_message.tmpl');


if (defined $query->param('build_preferences'))
{

  local $email_address = $query->param('email_address');
  local $user_password = $query->param('password');

  print $query->header;

  if ($email_address eq "")
    {
    $templ_message->param('HEADING', 'Dineguide Login Failure !');
    $templ_message->param('MESSAGE', 'You must enter an email address.');
    print $templ_message->output;

    }
  elsif ($user_password eq "")
    {
    $templ_message->param('HEADING', 'Dineguide Login Failure !');
    $templ_message->param('MESSAGE', 'You must enter a password.');
    print $templ_message->output;
    }

  if (existing_reg($email_address))
    {
    if (verify_password($email_address, $user_password))
      {
      $query_preferences = new CGI;

      my $cuisines;
      my $entertainment;
      my $kid_friendly;

      &build_user_preferences($email_address,\$cuisines,\$entertainment,\$kid_friendly);

      #---------------------
      my @pref_cuisines;
      if ($cuisines ne "")
        {
        @pref_cuisines = split /,/, $cuisines;
        }
      my %preferred_cuisines;
      foreach $cuizi (@pref_cuisines)
        {
	$preferred_cuisines{$cuizi}++;
        }
      #---------------------

      my @cuisine_names = &build_list_array("Cuisine");
      my %cuisine_hashed = &build_list_hash("Cuisine");

      foreach $cuiz (@cuisine_names)
        {
        my $checkbox_elem;
        if (defined $preferred_cuisines{$cuisine_hashed{$cuiz}})
	  {
          $checkbox_elem  = $query->checkbox(     -name=>"$cuiz",
                                                  -value=>$cuisine_hashed{$cuiz},
						  -checked=>'checked',
                                                  -label=>"$cuiz"
                                             );
	  }
	else
	  {
          $checkbox_elem  = $query->checkbox(     -name=>"$cuiz",
                                                  -value=>$cuisine_hashed{$cuiz},
                                                  -label=>"$cuiz"
                                             );
	  }

        $final_string = $final_string . $checkbox_elem . '<BR>';
        }


      $templ_preferences->param('CUISINE_CHECKBOXES', $final_string);


      if ($entertainment eq 'Yes')
        {
        $templ_preferences->param('ENTERTAINMENT_YES', 'checked');
        }
      elsif ($entertainment eq 'No')
	{
        $templ_preferences->param('ENTERTAINMENT_NO', 'checked');
	}
      else
	{
        $templ_preferences->param('ENTERTAINMENT_DONT_CARE', 'checked');
	}

      if ($kid_friendly eq 'Yes')
        {
        $templ_preferences->param('KID_FRIENDLY_YES', 'checked');
        }
      elsif ($kid_friendly eq 'No')
	{
        $templ_preferences->param('KID_FRIENDLY_NO', 'checked');
	}
      else
	{
        $templ_preferences->param('KID_FRIENDLY_DONT_CARE', 'checked');
	}

      $templ_preferences->param('EMAIL_ADDRESS', $email_address);


      print $templ_preferences->output;

      }
    else
      {
      $templ_message->param('HEADING', 'Dineguide Login Failure !');
      $templ_message->param('MESSAGE', 'Incorrect email address or password.');
      print $templ_message->output;
      }
    }
  else
    {
    $templ_message->param('HEADING', 'Dineguide Login Failure !');
    $templ_message->param('MESSAGE', 'Incorrect email address or password.');
    print $templ_message->output;
    }

}

elsif (defined $query->param('preferences'))
{

  $cgi_params_ref = $query->Vars;

  &update_preferences($cgi_params_ref);

  print $query->header;
  $templ_message->param('HEADING', 'Dineguide Preferences Updated !');
  $templ_message->param('MESSAGE', "Your dineguide preferences have been successfully updated.");
  print $templ_message->output;

}
else
{
my $first_name = $query->param('first_name');
my $last_name = $query->param('last_name');
my $email_address = $query->param('email_address');
my $postcode = $query->param('postcode');
my $age = $query->param('age');
my $sex = $query->param('sex');
my $user_password = $query->param('password');
my $user_password2 = $query->param('password2');



$query_message = new CGI;
print $query_message->header;

if ($first_name eq "")
  {
$back_to_mainpage = $query_message->a({href=>"http://dineguide"}, "blah");

  $templ_message->param('HEADING', 'Dineguide Subscription Failure !');
  $templ_message->param('MESSAGE', "You must enter a first name.");

print $templ_message->output;

  }
elsif ($last_name eq "")
  {
  $templ_message->param('HEADING', 'Dineguide Subscription Failure !');
  $templ_message->param('MESSAGE', 'You must enter a last name.');
print $templ_message->output;
  
  }
elsif ($email_address eq "")
  {
  $templ_message->param('HEADING', 'Dineguide Subscription Failure !');
  $templ_message->param('MESSAGE', 'You must enter an email address.');
print $templ_message->output;

  }
elsif ($user_password eq "")
  {
  $templ_message->param('HEADING', 'Dineguide Subscription Failure !');
  $templ_message->param('MESSAGE', 'You must enter a password.');
print $templ_message->output;
  
  }
elsif ($user_password2 eq "")
  {
  $templ_message->param('HEADING', 'Dineguide Subscription Failure !');
  $templ_message->param('MESSAGE', 'Please re-enter your password.');
print $templ_message->output;
  
  }
else
  {
  if ($user_password eq $user_password2)
  {

  if (existing_reg($email_address))
    {
    $templ_message->param('HEADING', 'Dineguide Subscription Failure !');
    $templ_message->param('MESSAGE', 'There is an existing registration with that email address.');
print $templ_message->output;

    }
  else
    {
    register_user($first_name,$last_name,$email_address,$user_password,$age,$sex,$postcode);
    send_registration_confirm($email_address, $user_password);

#-----------------------------------------------------------------------------
# Now we begin muhuhahahaha

    $query_preferences = new CGI;

    my @cuisine_names = &build_list_array("Cuisine");
    my %cuisine_hashed = &build_list_hash("Cuisine");

    foreach $cuiz (@cuisine_names)
      {
      my $checkbox_elem  = $query->checkbox(	-name=>"$cuiz",
                                		-value=>$cuisine_hashed{$cuiz},
                                		-label=>"$cuiz"
					   );

      $final_string = $final_string . $checkbox_elem . '<BR>';
      }


    $templ_preferences->param('CUISINE_CHECKBOXES', $final_string);

    $templ_preferences->param('ENTERTAINMENT_DONT_CARE', 'checked');
    $templ_preferences->param('KID_FRIENDLY_DONT_CARE', 'checked');
    $templ_preferences->param('EMAIL_ADDRESS', $email_address);
    $templ_preferences->param('REGO', 1);

    print $templ_preferences->output;

    }
  }

  else
  {
    $templ_message->param('HEADING', 'Dineguide Subscription Failure !');
    $templ_message->param('MESSAGE', 'Password fields don\'t match, please re-enter your password.');
print $templ_message->output;
    
  }

}

} # This brace belongs to the else part


sub register_user
{
  my ($first_name, $last_name, $email_address, $user_password,$age,$sex,$postcode) = @_;

  my $user = $purse;
  my $password = $psswd;

  $dbh->{RaiseError} = 1;
  $dbh = DBI->connect("DBI:mysql:$conn", $user, $password) or 
  	               print "$DBI::errstr";

  $strSQL = "insert into Subscriber (FirstName, LastName, Age, Sex, Email, Password, Postcode) " .
			    "values ('$first_name', " .
			            "'$last_name', " .
			            "'$age', " .
			            "'$sex', " .
				    "'$email_address', " .
				    "'$user_password', " .
				    "'$postcode');";

  $sth = $dbh->prepare($strSQL) or
	               print "$DBI::errstr";

  $rv = $sth->execute or
	      print "$DBI::errstr";
  
}

sub existing_reg 
{
  my ($email_address) = @_;

  use DBI;

  my $user = $purse;
  my $password = $psswd;

  $dbh->{RaiseError} = 1;
  $dbh = DBI->connect("DBI:mysql:$conn", $user, $password) or 
  	               print "$DBI::errstr";

  $strSQL = "SELECT SubscrID FROM Subscriber where Email='$email_address';";

  $sth = $dbh->prepare($strSQL) or
	               print "$DBI::errstr";

  $rv = $sth->execute or
	      print "$DBI::errstr";
  
  $rv = $sth->rows;

}

sub verify_password
{
  my ($email_address,$user_password) = @_;

  use DBI;

  my $user = $purse;
  my $password = $psswd;

  $dbh->{RaiseError} = 1;
  $dbh = DBI->connect("DBI:mysql:$conn", $user, $password) or
                       print "$DBI::errstr";

  $strSQL = "SELECT Password FROM Subscriber where Email='$email_address';";

  $sth = $dbh->prepare($strSQL) or
                       print "$DBI::errstr";

  $rv = $sth->execute or
              print "$DBI::errstr";
 
  my $tmp_hash = $sth->fetchrow_hashref;
  my $db_password = $tmp_hash->{'Password'};

  return ($user_password eq $db_password);
}

sub send_registration_confirm
{
my ($mail_address, $user_passwd) = @_;

use Mail::Sendmail;

%mail = ( 	
		To	=> "$mail_address",
		From    => "Automailer\@DineGuide.com.au",
		Subject => "Successful DineGuide Registration.",
		Message => "You have been successfully registered on the " .
			   "DineGuide subscriber list. \nYour password is : " .
			   "$user_passwd.\n\n This is an auto-generated mail ".
			   "message so please do not reply to this address, " .
			   "instead send your messages to Subscriptions\@" .
			   "DineGuide.com.au."

	);

sendmail(%mail) or die $Mail::Sendmail::error;

}

sub build_list_hash
{
  my ($table_name) = shift @_;

  my $user = $purse;
  my $password = $psswd;

  $dbh->{RaiseError} = 1;
  $dbh = DBI->connect("DBI:mysql:$conn", $user, $password) or
                        print "$DBI::errstr";

  $strSQL = "SELECT * FROM $table_name;";
  $sth = $dbh->prepare($strSQL) or print "$DBI::errstr";
  $sth->execute;

  my %return_hash;
  while ($tmp_hash = $sth->fetchrow_hashref)
    {
    $return_hash{$tmp_hash->{'Name'}} = $tmp_hash->{'CuisineID'};
    }

  return %return_hash;
}


sub build_list_array
{
  my ($table_name) = shift @_;

  my $user = $purse;
  my $password = $psswd;

  $dbh->{RaiseError} = 1;
  $dbh = DBI->connect("DBI:mysql:$conn", $user, $password) or 
                        print "$DBI::errstr";

  $strSQL = "SELECT * FROM $table_name;"; 
  $sth = $dbh->prepare($strSQL) or print "$DBI::errstr";
  $sth->execute;

  my @list_array;
  while (@tmp_array = $sth->fetchrow_array)
    {
    push (@list_array, $tmp_array[1]);
#    $list_hash{sprintf("%03u", $tmp_array[0])} = $tmp_array[1];
    }

  return @list_array;
}

sub update_preferences

{

  my ($param_ref) = shift @_;

  my $user = $purse;
  my $password = $psswd;

  $email_address = $param_ref->{'email_address'};
  $entertainment = $param_ref->{'entertainment'};
  $kid_friendly = $param_ref->{'kid_friendly'};

  $dbh->{RaiseError} = 1;
  $dbh = DBI->connect("DBI:mysql:$conn", $user, $password) or 
                        print "$DBI::errstr";

  my $strSQL = "UPDATE Subscriber SET Cuisine_preferences=?, Entertainment=? " .
	       ",Kid_friendly=? WHERE Email=?;";
  my $sth = $dbh->prepare($strSQL) or print "$DBI::errstr";
  
  @cuisine_list =  &build_list_array("Cuisine");

  local @cuisine_preferences;
  foreach $elem (@cuisine_list)
    {
    if (defined $param_ref->{$elem})
      {
      push (@cuisine_preferences, $param_ref->{$elem});
      }
    }

  my $pref_string = join (",", @cuisine_preferences);

  $sth->execute ($pref_string, $entertainment, $kid_friendly, $email_address);

}

sub build_user_preferences
{
  my ($email_address,$cuisines_ref,$entertainment_ref,$kid_friendly_ref) = @_;
  my $user = $purse;
  my $password = $psswd;


  $dbh->{RaiseError} = 1;
  $dbh = DBI->connect("DBI:mysql:$conn", $user, $password) or
                        print "$DBI::errstr";

  my $strSQL = "SELECT Cuisine_preferences,Entertainment,Kid_friendly FROM " .
	       "Subscriber WHERE Email=?";
  my $sth = $dbh->prepare($strSQL) or print "$DBI::errstr";

  $sth->execute ($email_address);

  $tmp_hash = $sth->fetchrow_hashref;
  $$cuisines_ref 	= $tmp_hash->{'Cuisine_preferences'};
  $$entertainment_ref 	= $tmp_hash->{'Entertainment'};
  $$kid_friendly_ref	= $tmp_hash->{'Kid_friendly'};

}
