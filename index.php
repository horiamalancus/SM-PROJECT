<html>
<head>

<?php
if (isset($_POST['bon']))
{
$myfile = fopen("onoff.txt","w") or die ("Unable to open file");
$txt = "true";
fwrite($myfile, $txt);
fclose($myfile);
}
if (isset($_POST['boff']))
{

$myfile = fopen("onoff.txt","w") or die ("Unable to open file");
$txt = "false";
fwrite($myfile, $txt);
fclose($myfile);
}
?>

  <title>Audio Visualizer using RaspberryPI  </title>
</head>
<body bgcolor= "silver">
<center>
<table witdh="800" heigth="1600" border="1"  bordercolor="blue">
<td>

<font face="verdana" color="navy">
<center>
Audio Visualizer using RaspberryPI
<br><br>
</font>


<center> <br>
<font color="white" face ="arial" size="2">
Light  the world from anywhere</font>
</font><br><br>
<img src="https://industrytoday.com/wp-content/uploads/2020/01/led-strip-lights.jpg" width="250" height="150"> </center>
<br>

<center>
<form method="post">
  <table
 style="width: 800px; heigth:800px; text-align: left; margin-left: auto; margin-right: auto;"
 border="1" cellpadding="2" cellspacing="2">
      <tr>
        <td  style="text-align: center;width : 100px ; heigth:200px;"><button name="bon"><font face="impact" color="blue">Led Strip ON</button></td></font>
        <td  style="text-align: center;width : 100px ; heigth:200px;"><button name="boff"><font face="impact" color="blue">Led Strip OFF</button></td></font>
      </tr>
    </tbody>
  </table>

</form>



<center>
</td>
</table>

</body>
</html>
