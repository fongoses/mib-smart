<?php
include("gerente.conf.php");
include("../lib/phplot-6.1.0/phplot.php");

function plota() {

    global $agenteIP;

    flush();
    ob_flush();
    $intervalo = 5; // 1s

    $community = "private";

    $oid_1 = "1.3.6.1.4.1.12619.1.3.1.0"; // Número de Aberturas
    $oid_2 = "1.3.6.1.4.1.12619.1.3.2.0"; // Número de Fechadas
    $oid_3 = "1.3.6.1.4.1.12619.1.3.3.0"; // Carros que passaram pelo sensor
    $oid_4 = "1.3.6.1.4.1.12619.1.3.4.0"; // Número de panes/travamentos

    $titulo1 = "Estatisticas de Aberturas/Fechaduras";
    $titulo2 = "Estatisticas de Carros e Panes";
    $eixoX = "Tempo (s)";
    $eixoY = "Quantidade";


    // Definimos os dados do gráfico
    $inicialAberturas =0;
    $inicialFechadas =0;
    $inicialPassaram =0;
    $inicialPane =0;
    $dados1 = array();
    $dados2 = array();

    $anteriorAberturas = $inicialPassaram;
    $anteriorFechadas = $inicialPane;
    $anteriorPassaram = $inicialPassaram;
    $anteriorPane = $inicialPane;

    $i=0;

    while(true){
        $msgAberturas = snmpget($agenteIP, $community, $oid_1);
        $msgFechadas = snmpget($agenteIP, $community, $oid_2);
        $msgPassaram = snmpget($agenteIP, $community, $oid_3);
        $msgPane = snmpget($agenteIP, $community, $oid_4);

        $valorAberturas = intval(str_replace("\"", "", explode(": ", $msgAberturas)[1]));
        $valorFechadas = intval(str_replace("\"", "", explode(": ", $msgFechadas)[1]));
        $valorPassaram = intval(str_replace("\"", "", explode(": ", $msgPassaram)[1]));
        $valorPane = intval(str_replace("\"", "", explode(": ", $msgPane)[1]));


        $dados1[] = array($i,$valorAberturas-$anteriorAberturas, $valorFechadas-$anteriorFechadas);
        $dados2[] = array($i,$valorPassaram-$anteriorPassaram,$valorPane-$anteriorPane);

        $anteriorAberturas=$valorAberturas;
        $anteriorFechadas=$valorFechadas;
        $anteriorPassaram=$valorPassaram;
        $anteriorPane=$valorPane;



        // Cria a imagem para o gráfico de passagens de carros
        $grafico1 = new PHPlot(400,300);
        $grafico1->SetFileFormat("png");

        // Indicamos o título do gráfico e o título dos dados no eixo X e Y do mesmo
        $grafico1->SetFailureImage(False); // Sem imagens de erro
        $grafico1->SetPrintImage(False); // Nao exibe imagem automaticamente
        $grafico1->SetTitle($titulo1);
        $grafico1->SetXTitle("Eixo X - Tempo");
        $grafico1->SetYTitle("Eixo Y - Quantidade");
        $grafico1->SetLegend(array('Numero Aberturas', 'Numero Fechadas'));

        // Indica os Dados a serem usados
        $grafico1->SetDataValues($dados1);
        // Exibimos o gráfico
        $grafico1->DrawGraph();


        // Cria a imagem para o gráfico de passagens de Panes
        $grafico2 = new PHPlot(400,300);
        $grafico2->SetFileFormat("png");

        // Indicamos o título do gráfico e o título dos dados no eixo X e Y do mesmo
        $grafico2->SetFailureImage(False); // Sem imagens de erro
        $grafico2->SetPrintImage(False); // Nao exibe imagem automaticamente
        $grafico2->SetTitle($titulo2);
        $grafico2->SetXTitle("Eixo X - Tempo");
        $grafico2->SetYTitle("Eixo Y - Quantidade");
        $grafico2->SetLegend(array('Numero Carros', 'Numero Panes'));
        // Indica os Dados a serem usados
        $grafico2->SetDataValues($dados2);
        // Exibimos o gráfico
        $grafico2->DrawGraph();




        // ATENÇÃO:
        // Como é feito o encoding da imagem não é necessário obedecer a regra de não poder
        // ter nenhum espaço nem nova linha depois do fim de script php
        echo "<img src=\"".$grafico1->EncodeImage()."\" id=\"grafico1\" />"; //exibe imagem
        echo "<img src=\"".$grafico2->EncodeImage()."\" id=\"grafico2\" />"; //exibe imagem

        flush();
        ob_flush();
        $i+=$intervalo;
        sleep($intervalo);

        echo "<script type='text/javascript'>$('#grafico1').remove();</script>";
        echo "<script type='text/javascript'>$('#grafico2').remove();</script>";


    }
}
?>