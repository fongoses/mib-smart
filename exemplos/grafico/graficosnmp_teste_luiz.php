<?php
include("../../lib/phplot-6.1.0/phplot.php");

$intervalo = 1; // 1s
$amostras = 10;

$community = "private";

//$oid = "1.3.6.1.4.1.12619.1.3.1.0"; // Número de Aberturas
//$oid = "1.3.6.1.4.1.12619.1.3.2.0"; // Número de Fechadas
$oid = "1.3.6.1.4.1.12619.1.3.3.0"; // Carros que passaram pelo sensor
//$oid = "1.3.6.1.4.1.12619.1.3.4.0"; // Número de panes/travamentos

$titulo = "Carros que passaram pelo sensor";
$eixoX = "Tempo (s)";
$eixoY = "Numero de Carros";


// Definimos os dados do gráfico
$msg = snmpget($agenteIP, $community, $oid);
$inicial = intval(str_replace("\"", "", explode(": ", $msg)[1]));

$dados = array();

$anterior = $inicial;
for($i = 0; $i < $amostras; $i++) {
    $msg = snmpget($agenteIP, $community, $oid);
    $valor = intval(str_replace("\"", "", explode(": ", $msg)[1]));
    $valor_grafico =
    $dados[] = array("tempo", $valor);
    sleep($intervalo);
}


$dados = array(
        array('Janeiro', 10),
        array('Fevereiro', 5),
        array('Março', 4),
        array('Abril', 8),
        array('Maio', 7),
        array('Junho', 5),
);

// Cria a imagem para o gráfico
$grafico = new PHPlot();
$grafico->SetFileFormat("png");

// Indicamos o título do gráfico e o título dos dados no eixo X e Y do mesmo
$grafico->SetTitle($titulo);
$grafico->SetXTitle("Eixo X - Meses");
$grafico->SetYTitle("Eixo Y - Valores");

// Indica os Dados a serem usados
$grafico->SetDataValues($dados);

// Exibimos o gráfico
$grafico->DrawGraph();

// ATENÇÃO:
// Como é gerado um binário da imagem, não pode ter nenhum espaço nem nova linha depois do fim de script php
?>