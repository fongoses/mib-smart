<?php
include('gerente.conf.php');

$generalValor_6=$_POST['general6'];

if(!strchr($generalValor_6,':')){
    $generalSet_6 = snmpset($agenteIP, "private", "1.3.6.1.4.1.12619.1.1.6.0" , "t","".$generalValor_6);
    $general_6=str_replace("\"","",explode(": ",$generalSet_6)[1]);
    echo $general_6;
    echo "<script type='text/javascript'>alert('Alterado');location.href='gerente.php';</script>";
    return;
}
echo "<script type='text/javascript'>location.href='gerente.php';</script>";
?>