print &generate_radio_questions(1,5,500,'set1');


sub generate_radio_questions
{
my ($start_value, $num_choices, $table_width, $button_names) = @_;

local $generated_html;
local $top_line_colspan = $num_choices + ($num_choices - 3);
local $spacer_width = ($table_width - ((24*2) + ($num_choices - 1)))/$num_choices;

$generated_html = qq(
<table border="0" cellspacing="0" cellpadding="0" align="center">
  <tr valign="bottom"> 
    <td align="right"><img src="images/lineend.gif" width="12" height="1"></td>
    <td colspan="$top_line_colspan" align="center" bgcolor="#000000"><img src="images/spacer.gif" width="50" height="1"></td>
    <td align="left"><img src="images/lineend.gif" width="12" height="1"></td>
  </tr>
  <tr align="center" valign="top">
    <td align="right"><img src="images/zeromark.gif" width="12" height="10"></td>
    <td><img src="images/spacer.gif" width="$spacer_width" height="10"></td>
);

for ($x=$start_value;$x < ($start_value+$num_choices)-2;$x++)
  {
  $generated_html .= qq(
  <td><img src="images/spacerblack.gif" width="1" height="10"></td>
  <td><img src="images/spacer.gif" width="$spacer_width" height="10"></td>
  );
  }

$generated_html .= qq(
    <td align="left"><img src="images/fullmark.gif" width="12" height="10"></td>
  </tr>
  <tr> 
    <td align="center"> 
      <input type="radio" name="$button_names" value="radiobutton$start_value">
    </td>
    <td><img src="images/spacer.gif" height="15"></td>
);

for ($x=$start_value+1;$x < ($start_value+$num_choices)-1;$x++)
  {
  $generated_html .= qq (
    <td> 
      <input type="radio" name="$button_names" value="radiobutton$x">
    </td>
    <td><img src="images/spacer.gif"  height="15"></td>
  );
  }


$generated_html .= qq(
    <td align="center"> 
      <input type="radio" name="$button_names" value="radiobutton$x">
    </td>
  </tr>
  <tr align="center" valign="middle"> 
);

$generated_html .= qq(
    <td>$start_value</td>
);

for ($x=$start_value+1;$x < $start_value+$num_choices;$x++)
  {
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
