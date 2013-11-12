<?php
	$agenteIP="192.168.0.105";

    echo "<h1> Dados do Fabricante do dispositivo</h1>";
    $generalGet_1 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.1.0");
    $general_1=str_replace("\"","",explode(": ",$generalGet_1)[1]);

    $generalGet_2 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.2.0");
    $general_2=str_replace("\"","",explode(": ",$generalGet_2)[1]);

    $generalGet_3 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.3.0");
    $general_3=str_replace("\"","",explode(": ",$generalGet_3)[1]);

    $generalGet_4 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.4.0");
    $general_4=str_replace("\"","",explode(": ",$generalGet_4)[1]);
    
    
    echo "<hr>";
    echo "<table border=0>";
    echo "<tr><td>Nome do dispositivo:</td> <td><input type=text value=\"".$general_1."\"/></td></tr>";
    echo "<tr><td>Firmware:</td>  <td><input type=text value=\"".$general_2."\"/><br></td></tr>";
    echo "<tr><td>Versao da firmware:</td> <td> <input type=text value=\"".$general_3."\"/></td></tr>";
    echo "<tr><td>Em funcionamento ha: </td><td> <input type=text value=\"".$general_4." \"/></td></tr>";
    echo "</table>";
    echo "<hr>";

?>

