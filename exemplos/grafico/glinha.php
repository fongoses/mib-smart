<?php
include("../../lib/phplot-6.1.0/phplot.php");

// Definimos os dados do gráfico
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
$grafico->SetTitle("Gráfico de exemplo");
$grafico->SetXTitle("Eixo X - Meses");
$grafico->SetYTitle("Eixo Y - Valores");

// Indica os Dados a serem usados
$grafico->SetDataValues($dados);

// Exibimos o gráfico
$grafico->DrawGraph();

// ATENÇÃO:
// Como é gerado um binário da imagem, não pode ter nenhum espaço nem nova linha depois do fim de script php
?>