<!DOCTYPE HTML>

<!-- Get data from DB -->
<?php

  // DB Constants
  include("db-settings.php");
  $database = "testing";

  // Create connection
  $con = mysqli_connect($servername, $username, $password, $database);
  unset($servername, $username, $password);

  // Check connection
  if (!$con) {
      die("Connection failed: " . mysqli_connect_error());
  } 
  //else {
  //  echo "Connected successfully";
  //}

  // Select data query
  $query = '
  SELECT timestamp, count FROM PeopleCounter ORDER BY timestamp ASC
  ';
  $result = mysqli_query($con, $query);

  // Setup data header (column names)
  //$chart_array[0] = array("Timestamp", "Count");

  // For each result
  $i = 0;
  while($currentResult = $result->fetch_assoc()) {
    $values = array_values($currentResult);
    //echo("Values: " . $values[0] . "\t" . $values[1]);
    //echo("<br>");

    // Append to data array
    $chart_array[$i] = array((string)$values[0], intval($values[1]));
    $i++;
  }
  // If no data was present in the results query, insert zero values
  if($i == 0) {
    $chart_array[0] = array("0000-00-00 00:00:00", 0);
  }

  // Encode data array to JSON for displaying in chart
  $PHPChartData = json_encode($chart_array);
  //echo("Data:");
  //echo("<br>");
  //echo($data);

?>

<!-- Display data -->
<html>

    <head>

      <!-- Import Google charts -->
      <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
      <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>

      <!-- Setup chart data -->
      <script type="text/javascript">

        // Load the chart and draw once
        //google.charts.load('current', {'packages':['corechart']});
        //google.charts.setOnLoadCallback(drawChart);

        // Load the chart and redraw on window resize
        google.charts.load('current', {
          callback: function () {
            drawChart();
            window.addEventListener('resize', drawChart, false);
          },
          packages:['corechart']
        });
  
        // The function defining how the chart is drawn
        function drawChart() {
          
          // Setup data array and chart data placeholder
          var rawData = <?php echo($PHPChartData); ?>;
          var chartData = new google.visualization.DataTable();

          // Add columns for X and Y values
          chartData.addColumn('datetime', 'Datetime');
          chartData.addColumn('number', 'Count');

          // May not need this
          var maxNumberOfDataPoints = 10000;
          var numberOfDataPoints = rawData.length;
          var incrementValue = Math.floor(Math.max(numberOfDataPoints / maxNumberOfDataPoints, 1));

          // The format that will be used for displaying x values 
          var timestampFormatString = 'YYYY-MM-dd HH:mm:ss';
          var timestampFormat = new google.visualization.DateFormat({
            pattern: timestampFormatString
          });

          // Insert each row of data into chart data
          for (var i = 0; i < numberOfDataPoints; i += incrementValue) {
            if(i >= numberOfDataPoints) { break; }

            // Get the current timestamp value as the 1st element of the array,
            // split the timestamp string into its parts,
            // and construct a Date object
            var timestampString = rawData[i][0];
            var timestampParts = timestampString.split(/[\s-:]+/);
            var timestampDate = new Date(timestampParts[0], timestampParts[1]-1, timestampParts[2], timestampParts[3], timestampParts[4], timestampParts[5]);

            var timestampValue = {
              v: timestampDate,
              f: timestampFormat.formatValue(timestampDate)
            };

            // Get the current count value as the 2nd element of the array
            var count = rawData[i][1];
            
            // add the current Date object and count to the chart data
            chartData.addRow([timestampValue, count]);

          }

          // Put data from DB into chart data
          //var chartData = new google.visualization.arrayToDataTable(rawData);
          
          // Specify chart options
          var options = {
            title: 'Devices Over Time',
            curveType: 'function',
            legend : "none",
            hAxis: {
              format: timestampFormatString
            }
            //legend: { position: 'bottom' }
          };
          
          // Construct a line chart and draw it
          //var chart = new google.visualization.LineChart(document.getElementById('line_chart'));
          //var chart = new google.visualization.ColumnChart(document.getElementById('line_chart'));
          var chart = new google.visualization.AreaChart(document.getElementById('line_chart'));
          chart.draw(chartData, options);

        }
      </script>

      <!-- TODO: move into CSS -->
      <style>
        .page-wrapper {
          width:1000px;
          margin:0 auto;
        }
      </style>

    </head>

    <!-- The chart on the page -->
    <body>
      <!-- <div id="line_chart" style="width: 900px; height: 500px; display: block; margin: 0 auto"></div> -->
      <div id="line_chart"></div>
    </body>
    
  </html>