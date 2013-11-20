<?php
	
	
	
	echo "<!DOCTYPE html>";
	echo "<html lang='en'>";
	echo "<head>";
	echo "<script src='js/jquery.js'></script>";
	echo "<script src='js/jquery-ui.js'></script>";
	echo "</head>";
	
	include("gerente.conf.php");	
	include("graficosnmp.php");
	
	echo 'IP Agente: '.$agenteIP;
	//general
	echo "<body>";
	echo "<hr>";
    echo "<h1> Dados do Fabricante do dispositivo</h1>";
    $generalGet_1 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.1.0");
    $general_1=str_replace("\"","",explode(": ",$generalGet_1)[1]);

    $generalGet_2 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.2.0");
    $general_2=str_replace("\"","",explode(": ",$generalGet_2)[1]);

    $generalGet_3 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.3.0");
    $general_3=str_replace("\"","",explode(": ",$generalGet_3)[1]);

    $generalGet_4 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.4.0");
    $general_4=str_replace("\"","",explode(": ",$generalGet_4)[1]);
    
    $generalGet_5 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.5.0");
    $general_5=str_replace("\"","",explode(": ",$generalGet_5)[1]);        
    
    $generalGet_6 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.6.0");
    $general_6=str_replace("\"","",explode(": ",$generalGet_6)[1]);
    
    $generalGet_7 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.7.0");
    $general_7=str_replace("\"","",explode(": ",$generalGet_7)[1]);
    
    $generalGet_8 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.8.0");
    $general_8=str_replace("\"","",explode(": ",$generalGet_8)[1]);
    
    $generalGet_9 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.9.0");
    $general_9=str_replace("\"","",explode(": ",$generalGet_9)[1]);
    
    
    
    echo "<table border=0>";
    echo "<tr><td>Nome do dispositivo:</td> <td><input type=text value=\"".$general_1."\"/></td></tr>";
    echo "<tr><td>Firmware:</td>  <td><input type=text value=\"".$general_2."\"/><br></td></tr>";
    echo "<tr><td>Versao da firmware:</td> <td> <input type=text value=\"".$general_3."\"/></td></tr>";
    echo "<tr><td>Em funcionamento ha: </td><td> <input type=text value=\"".$general_4." \"/></td></tr>";
    echo "<tr><td>Ultima inicializacao: </td><td> <input type=text value=\"".$general_5." \"/></td></tr>";    
    
    echo "<form name='formGeneral6' method=post action=setgeneral6.php>";  	
    	echo "<tr><td>Tempo de permanencia em aberto: </td><td> <input type=text name=general6 value=\"".$general_6." \"onclick=this.value=\"\" /></td><td><input type=submit value=Alterar></td></tr>";
	echo "</form>";
    
    echo "<tr><td>Status da cancela: </td><td> <input type=text value=\"".($general_7?"Aberta":"Fechada")." \"/></td><td></tr>";
    echo "<tr><td>Carro em frente a cancela: </td><td> <input type=text value=\"".($general_8?"Sim":"Nao")." \"/></td></tr>";
    echo "<tr><td>Codigo ultimo erro: </td><td> <input type=text value=\"".$general_9." \"/></td></tr>";
    echo "</table>";    
    echo "<hr>";    
        
    //cards
    echo "<h1> Dados dos pagamentos realizados nesse dispositivo</h1>";
    $cardsWalk = snmpwalk($agenteIP, "private", "1.3.6.1.4.1.12619.1.2.1");
    $cardsColumnsNumber=3;
    $cardsRowsNumber=sizeof($cardsWalk)/$cardsColumnsNumber;    
    echo "<table border=1>";
    echo "<tr><td> <b>Codigo do pagamento</b></td> <td><b>Descricao tipo de pagamento</b></td><td><b>Numero de Utilizacoes</b></td></tr>";
    for($row=0;$row<$cardsRowsNumber;$row+=1)    	
    	echo '<tr><td>'.str_replace("\"","",explode(": ",$cardsWalk[$row])[1]).'</td><td>'.str_replace("\"","",explode(": ",$cardsWalk[$row+$cardsRowsNumber])[1]).'</td><td>'.str_replace("\"","",explode(": ",$cardsWalk[$row+$cardsRowsNumber*2])[1]).'</td></tr>';
    echo "</table>";
    echo "<hr>";
    

	//stats
    echo "<h1> Estatisticas atuais da cancela</h1>";
    $statsGet_1 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.3.1.0");
    $stats_1=str_replace("\"","",explode(": ",$statsGet_1)[1]);

    $statsGet_2 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.3.2.0");
    $stats_2=str_replace("\"","",explode(": ",$statsGet_2)[1]);

    $statsGet_3 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.3.3.0");
    $stats_3=str_replace("\"","",explode(": ",$statsGet_3)[1]);    
    
    $statsGet_4 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.3.4.0");    
    $stats_4=str_replace("\"","",explode(": ",$statsGet_4)[1]);

    

    echo "<table border=0>";
    echo "<tr><td>Numero de aberturas: </td> <td><input type=text value=\"".$stats_1."\"/></td></tr>";
    echo "<tr><td>Numero de fechadas: </td>  <td><input type=text value=\"".$stats_2."\"/><br></td></tr>";
    echo "<tr><td>Numero de carros que passaram pelo sensor:</td> <td> <input type=text value=\"".$stats_3."\"/></td></tr>";
    echo "<tr><td>Numero de panes/travamentos na cancela:</td> <td> <input type=text value=\"".$stats_4."\"/></td></tr>";
    
    echo "</table>";
    echo "<hr>";
	    
	//hw
    echo "<h1> Informacoes do hardware da cancela</h1>";
    $hwGet_1 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.4.1.0");
    $hw_1=str_replace("\"","",explode(": ",$hwGet_1)[1]);

    $hwGet_2 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.4.2.0");
    $hw_2=str_replace("\"","",explode(": ",$hwGet_2)[1]);

    $hwGet_3 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.4.3.0");
    $hw_3=str_replace("\"","",explode(": ",$hwGet_3)[1]);
    
    $hwGet_4 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.4.4.0");    
    $hw_4=str_replace("\"","",explode(": ",$hwGet_4)[1]);

	$hwGet_5 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.4.5.0");    
    $hw_5=str_replace("\"","",explode(": ",$hwGet_5)[1]);    

    echo "<table border=0>";
    echo "<tr><td>Tempo necessario para abertura da cancela: </td> <td><input type=text value=\"".$hw_1."\"/></td></tr>";
    echo "<tr><td>Voltagem do dispositivo controlador: </td>  <td><input type=text value=\"".$hw_2."\"/><br></td></tr>";
    echo	 "<tr><td>Voltagem do motor:</td> <td> <input type=text value=\"".$hw_3."\"/></td></tr>";
    echo "<tr><td>Potencia do sinal da interface NFC:</td> <td> <input type=text value=\"".$hw_4."\"/></td></tr>";
    echo "<tr><td>Potencia do sinal da interface de bluetooth:</td> <td> <input type=text value=\"".$hw_5."\"/></td></tr>";
    echo "</table>";
    echo "<hr>";
	
	
	//network
    echo "<h1> Informacoes da rede ligada a cancela</h1>";
    $networkGet_1 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.5.1.0");
    $network_1=str_replace("\"","",explode(": ",$networkGet_1)[1]);
	
    $networkGet_2 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.5.2.0");
    $network_2=str_replace("\"","",explode(": ",$networkGet_2)[1]);

    $networkGet_3 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.5.3.0");
    $network_3=str_replace("\"","",explode(": ",$networkGet_3)[1]);
    
    //tabela de interfacess
    //$networkGet_4 = snmpget($agenteIP, "private", "1.3.6.1.4.1.12619.1.5.4.0");    
    //$network_4=str_replace("\"","",explode(": ",$networkGet_4)[1]);


    echo "<table border=0>";
    echo "<tr><td>Mac Address da Interface Bluetooth: </td> <td><input type=text value=\"".$network_1."\"/></td></tr>";
    
    echo "<form name='formNetwork2' method=post action=setnetwork2.php>";  	
    	echo "<tr><td>Pin da Interface Bluetooth: </td><td> <input type=text name=network2 value=\"".$network_2." \"/></td><td><input type=submit value=Alterar></td></tr>";
	echo "</form>";
	
    echo "<tr><td>Numero Total de Interfaces de rede: </td><td> <input type=text value=\"".$network_3." \"/></td></tr>";	
    echo "</table>";
    echo "<h2>Interfaces de rede</h2>";
    echo "<table border=1>";
    echo "<tr><td> <b>Id da interface</b></td> <td><b>Endereco MAC</b></td><td><b>Tipo de Interface</b></td></tr>";    
    
    $ifTableWalk = snmpwalk($agenteIP, "private", "1.3.6.1.4.1.12619.1.5.4.1");    
    $ifTableColumnsNumber=3;
    $ifTableRowsNumber=sizeof($ifTableWalk)/$ifTableColumnsNumber;
        
    for($row=0;$row<$ifTableRowsNumber;$row+=1)    	
    	echo '<tr><td>'.str_replace("\"","",explode(": ",$ifTableWalk[$row])[1]).'</td><td>'.str_replace("\"","",explode(": ",$ifTableWalk[$row+$ifTableRowsNumber])[1]).'</td><td>'.(str_replace("\"","",explode(": ",$ifTableWalk[$row+$ifTableRowsNumber*2])[1])?"Wifi":"Ethernet").'</td></tr>';
    echo "</table>";
    echo "<hr>";
    echo "</body>";
    
    
    //Graficos
    echo "<h1>Graficos</h1>";
   	
	plota();
    
    
    

?>

