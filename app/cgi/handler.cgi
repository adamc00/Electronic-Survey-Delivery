#!/usr/bin/env perl

use DBI;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use HTML::Template;

local $query = new CGI;
local $templ_message = HTML::Template->new(filename => '../tmpl/survey_message.tmpl');

print $query->header;

$DSNstr = 'SQLite:dbname=../db/survey.db';

if (! (local $dbh = DBI->connect("dbi:$DSNstr", $user, $passwd) ))
{
  $templ_message->param('HEADING', 'Unable to connect to Database !');
  $templ_message->param('MESSAGE', 'Please report this error.');
  print $templ_message->output;
  exit;
}
$dbh->{LongReadLen} = 500;

my $user_id = $query->param('user_id');

if ($query->param('me') eq 'LOGIN') {

    my $user_id       = $query->param('user_id');
    my $user_password = $query->param('user_password');

    if ($user_id eq "") {
        $templ_message->param('HEADING', 'Login Failure !');
        $templ_message->param('MESSAGE', 'You must enter a user id.');
        print $templ_message->output;
        exit;
    }
    elsif ($user_password eq "") {
        $templ_message->param('HEADING', 'Login Failure !');
        $templ_message->param('MESSAGE', 'You must enter a password.');
        print $templ_message->output;
        exit;
    }
    else {

        if (! confirm_login($user_id, $user_password)) {
            $templ_message->param('HEADING', 'Login Failure !');
            $templ_message->param('MESSAGE', 'Incorrect login or password.');
            print $templ_message->output;
            exit;
        }
    }
}
elsif ($query->param('me') eq 'DEMOGRAPHICS') {
    #STORE DEMOGRAPHICS
    if ( $DEBUG )
    {
        print "STORE DEMOGRAPHICS";
        print $query->dump;
    }

    $strSQL = q(
        UPDATE Login
        SET gender = ?,
        age = ?,
        working_years = ?,
        working_months = ?,
        job_years = ?,
        job_months = ?,
        emp_stat = ?
        WHERE UserID=?
    );

    $sth = $dbh->prepare($strSQL) or
    	print "$DBI::errstr";

    $rv = $sth->execute(
        scalar $query->param('gender'),
        scalar $query->param('age'),
        scalar $query->param('working_years'),
        scalar $query->param('working_months'),
        scalar $query->param('job_years'),
        scalar $query->param('job_months'),
        scalar $query->param('emp_stat'),
        $user_id
    ) or print "$DBI::errstr";

    	#RENDER QUESTION 1;
}
else {
    # STORE QUESTION
    if ($query->param('score')) {

        $strSQL = "DELETE FROM Data where UserID=? and Item=?";
        $sth = $dbh->prepare($strSQL) or
               print "$DBI::errstr";

        $rv = $sth->execute($user_id, scalar $query->param('me')) or
              print "$DBI::errstr";

        $strSQL = 'INSERT INTO Data (UserID,Item,StoredValue) VALUES (?,?,?)';
        $sth = $dbh->prepare($strSQL) or
               print "$DBI::errstr";

        $rv = $sth->execute (
            $user_id,
            scalar $query->param('me'),
            scalar $query->param('score')
        ) or print "$DBI::errstr";
    }
}

if ( $query->param('goto') eq 'DEMOGRAPHICS' ) {
    #RENDER DEMOGRAPHICS
    &render_demographics;
    exit;
}
else {
    #RENDER ORDINARY QUESTION
    my $action;

    if ( $query->param('navNext.x') ) {
        $action = "NEXT";
    }
    elsif ( $query->param('navPrev.x') ) {
        $action = "PREVIOUS";
    }
    else {
        $templ_message->param('HEADING', 'Internal error !');
        $templ_message->param('MESSAGE', 'Please report this error.');
        print $templ_message->output;
    }

    render_question(
        scalar $query->param('user_id'),
        scalar $query->param('me'),
        $action
    );

    exit;

}

#Shouldn't get here
$templ_message->param('HEADING', 'Internal error !');
$templ_message->param('MESSAGE', 'Please report this error.');
print $templ_message->output;
exit;


sub confirm_login {
    my ($user_id, $user_password) = @_;

    $strSQL = "SELECT UserID FROM Login where UserID=? and Password=?;";

    $sth = $dbh->prepare($strSQL) or
           print "$DBI::errstr";

    $rv = $sth->execute($user_id, $user_password) or
          print "$DBI::errstr";

    $sth->fetchall_arrayref;

    $rv = $sth->rows;
}

sub render_question {
    my ($user_id, $me, $action) = @_;
    my $quest_no = 0;
    my $max_q = -1;

    $strSQL = "SELECT Item, QuestOrder FROM Questions order by QuestOrder";

    $sth = $dbh->prepare($strSQL) or
    print "$DBI::errstr";

    $rv = $sth->execute() or
    print "$DBI::errstr";

    $array_ref = $sth->fetchall_arrayref([0,1]);;

    $max_q = @$array_ref;

    foreach $row_ref (@$array_ref) {
        if ( $$row_ref[0] eq $me ) {
            $quest_no=$$row_ref[1];
            last
        };
    }

    #SET UP TEMPLATES
    local $templ_question = HTML::Template->new(filename => '../tmpl/survey_question.tmpl');
    $templ_question->param(
        'user_id',
        scalar $query->param('user_id')
    );

    if ( $action eq "NEXT" ) {
        if ($quest_no == $max_q) {

            #RENDER THANKYOU
            $templ_message->param('HEADING', 'THANK YOU FOR YOUR ASSISTANCE');
            $templ_message->param('MESSAGE', 'You may now close your browser. All data is confidentially saved.');
            print $templ_message->output;

            exit;
        }
        elsif ( (++$quest_no) == $max_q ) {
            #RENDER LAST QUESTION
            $templ_question->param('LAST_Q', 1);
        }
    }
    elsif ( $action eq "PREVIOUS" ) {
        if (--$quest_no == 0) {
            #RENDER DEMOGRAPHICS
            &render_demographics;
            exit;
        }
    }

    my $new_me = $array_ref->[$quest_no-1]->[0];

    #RENDER QUESTION;

    $strSQL = "SELECT * FROM Questions where Item = ?";

    $sth = $dbh->prepare($strSQL) or
    print "$DBI::errstr";

    $rv = $sth->execute($new_me) or
    print "$DBI::errstr";

    my $tmp_hash = $sth->fetchrow_hashref() or
    print "$DBI::errstr";


    $strSQL = "SELECT StoredValue FROM Data where UserID=? and Item=?";
    $sth_data = $dbh->prepare($strSQL) or
    print "$DBI::errstr";

    $rv = $sth_data->execute(
        scalar $query->param('user_id'),
        $new_me
    ) or print "$DBI::errstr";

    my $scale_value;
    if ( my $data_arrayref = $sth_data->fetchrow_arrayref ) {
        $scale_value = $data_arrayref->[0];
    }
    else {
        $scale_value = "";
    }

    my $scale_html = &generate_radio_questions(
        $tmp_hash->{'Scale_min'},
        $tmp_hash->{'Scale_no'},
        500,
        'score',
        $scale_value
    );

    $templ_question->param('Q_NAME', $new_me);
    $templ_question->param('HEADING', $tmp_hash->{'Section'});
    $templ_question->param('MESSAGE', $tmp_hash->{'Blurb'});
    $templ_question->param(
        'QUESTION',
        $tmp_hash->{'Question_no'} . ". " .
        $tmp_hash->{'Question'}
    );
    $templ_question->param('LEFT_TEXT', $tmp_hash->{'Scale_min_label'});
    $templ_question->param('RIGHT_TEXT', $tmp_hash->{'Scale_max_label'});
    $templ_question->param('SCALE', $scale_html);



    if ( $DEBUG ) {
        print $query->dump;
    }

    print $templ_question->output;
    $templ_question->param('SCALE', $scale_html);
}


sub render_demographics
{
    $strSQL = "SELECT * FROM Login where UserID=?";

    $sth = $dbh->prepare($strSQL) or
    print "$DBI::errstr";

    $rv = $sth->execute($user_id) or
    print "$DBI::errstr";

 	my $tmp_hash = $sth->fetchrow_hashref;
 	my $db_password = $tmp_hash->{'Password'};


    local $templ_demographics = HTML::Template->new(filename => '../tmpl/demographics.tmpl');
    $templ_demographics->param('user_id', $user_id);

    if ($tmp_hash->{'gender'} eq 'F') {
        $templ_demographics->param('F_CHK', "Checked");
        $templ_demographics->param('M_CHK', "");
    }
    elsif ($tmp_hash->{'gender'} eq 'M') {
        $templ_demographics->param('M_CHK', "Checked");
        $templ_demographics->param('F_CHK', "");
    }

    $templ_demographics->param('AGE', $tmp_hash->{'age'});
    $templ_demographics->param('WORKING_YEARS', $tmp_hash->{'working_years'});
    $templ_demographics->param('WORKING_MONTHS', $tmp_hash->{'working_months'});
    $templ_demographics->param('JOB_YEARS', $tmp_hash->{'job_years'});
    $templ_demographics->param('JOB_MONTHS', $tmp_hash->{'job_months'});
    $templ_demographics->param('JOB_MONTHS', $tmp_hash->{'job_months'});

    if ($tmp_hash->{'emp_stat'} eq 'full') {
        $templ_demographics->param('FULL_CHK', "Checked");
        $templ_demographics->param('PART_CHK', "");
        $templ_demographics->param('CASUAL_CHK', "");
        $templ_demographics->param('CONTRACT_CHK', "");
    }
    elsif ($tmp_hash->{'emp_stat'} eq 'part') {
        $templ_demographics->param('FULL_CHK', "");
        $templ_demographics->param('PART_CHK', "Checked");
        $templ_demographics->param('CASUAL_CHK', "");
        $templ_demographics->param('CONTRACT_CHK', "");
    }
    elsif ($tmp_hash->{'emp_stat'} eq 'casual') {
        $templ_demographics->param('FULL_CHK', "");
        $templ_demographics->param('PART_CHK', "");
        $templ_demographics->param('CASUAL_CHK', "Checked");
        $templ_demographics->param('CONTRACT_CHK', "");
    }
    elsif ($tmp_hash->{'emp_stat'} eq 'contract') {
        $templ_demographics->param('FULL_CHK', "");
        $templ_demographics->param('PART_CHK', "");
        $templ_demographics->param('CASUAL_CHK', "");
        $templ_demographics->param('CONTRACT_CHK', "Checked");
    }
    print $templ_demographics->output;
    if ($DEBUG) {
        print "RENDER DEMOGRAPHICS";
        print $query->dump;
    }
    exit;
}

sub generate_radio_questions {
    my ($start_value, $num_choices, $table_width, $button_names, $default) = @_;

    local $generated_html;
    local $top_line_colspan = $num_choices + ($num_choices - 3);
    local $spacer_width = ($table_width - ((24*2) + ($num_choices - 1)))/$num_choices;

    my $checked;

    $generated_html = qq(
    <table border="0" cellspacing="0" cellpadding="0" align="center">
      <tr valign="bottom">
        <td align="right"><img src="../images/lineend.gif" width="12" height="1"></td>
        <td colspan="$top_line_colspan" align="center" bgcolor="#000000"><img src="../images/spacer.gif" width="50" height="1"></td>
        <td align="left"><img src="../images/lineend.gif" width="12" height="1"></td>
      </tr>
      <tr align="center" valign="top">
        <td align="right"><img src="../images/zeromark.gif" width="12" height="10"></td>
        <td><img src="../images/spacer.gif" width="$spacer_width" height="10"></td>
    );

    for ($x=$start_value;$x < ($start_value+$num_choices)-2;$x++) {
      $generated_html .= qq(
      <td><img src="../images/spacerblack.gif" width="1" height="10"></td>
      <td><img src="../images/spacer.gif" width="$spacer_width" height="10"></td>
      );
    }

    if ($default eq $start_value) {
        $checked = "checked";
    }
    else {
        $checked = "";
    }

    $generated_html .= qq(
        <td align="left"><img src="../images/fullmark.gif" width="12" height="10"></td>
      </tr>
      <tr>
        <td align="center">
          <input type="radio" name="$button_names" value="$start_value" $checked>
        </td>
        <td><img src="../images/spacer.gif" height="15"></td>
    );

    for ($x=$start_value+1;$x < ($start_value+$num_choices)-1;$x++) {
        if ($default eq $x) {
            $checked = "checked";
        }
        else {
            $checked = "";
        }

        $generated_html .= qq(
            <td>
            <input type="radio" name="$button_names" value="$x" $checked>
            </td>
            <td><img src="../images/spacer.gif"  height="15"></td>
        );
    }

    if ($default eq $x) {
        $checked = "checked";
    }
    else {
        $checked = "";
    }

    $generated_html .= qq(
        <td align="center">
          <input type="radio" name="$button_names" value="$x" $checked>
        </td>
      </tr>
      <tr align="center" valign="middle">
    );

    $generated_html .= qq(
        <td>$start_value</td>
    );

    for ($x=$start_value+1;$x < $start_value+$num_choices;$x++) {
      $generated_html .= qq(
          <td>&nbsp;</td>
          <td>$x</td>
      );
    }

    $generated_html .= qq(
        </tr>
        </table>
    );

    return $generated_html;
}
