<?php
include("snmptable.php");

echo "<h1>Cards Accepted</h1>";
echo "<hr>";
$cardsAcceptedTable = snmptable("127.0.0.1", "private", ".1.3.6.1.4.1.12619.1.2.1") or die("error");
print_r($cardsAcceptedTable);
echo "<hr>";

echo "<br>";

echo "<h1>Interfaces</h1>";
echo "<hr>";
$ifTable = snmptable("127.0.0.1", "private", ".1.3.6.1.4.1.12619.1.5.4") or die("error");
print_r($ifTable);
echo "<hr>";
?>