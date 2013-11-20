<?php
include('gerente.conf.php');

$networkValor_2=$_POST['network2'];

if($networkValor_2){
    $networkSet_2 = snmpset($agenteIP, "private", "1.3.6.1.4.1.12619.1.5.2.0" , "s","".$networkValor_2);
    $network_2=str_replace("\"","",explode(": ",$networkSet_5)[1]);
    echo "<script type='text/javascript'>alert('Alterado');location.href='gerente.php';</script>";
    return;
}
echo "<script type='text/javascript'>location.href='gerente.php';</script>";
?>