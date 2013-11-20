<?php
$dados = snmpwalk('localhost', 'private', '1.3.6.1.4.1.12619');

var_dump($dados);
?>