<!DOCTYPE html>
<html>

<head>
    <title>Chapter 5</title>
    <style type="text/css">

    html, body, #wrapper {
        width: 100%;
        height: 60%;
        margin: 0px;
    }

    .chart {
        font-family: Arial, sans-serif;
        font-size: 12px;
    }

    .axis path,
    .axis line {
        fill: none;
        stroke: #000;
        shape-rendering: crispEdges;
    }

    .bar {
        fill: #000000;
    }
    .bar0 {
        fill: #CC0000;
    }
    .bar1 {
        fill: #669900;
    }
    .bar2 {
        fill: #33b5e5;
    }
    .bar3 {
        fill: #ffbb33;
    }
    .barx0 {
        fill: #CD5252;
    }
    .barx1 {
        fill: #7B9A3D;
    }
    .barx2 {
        fill: #8ACEE6;
    }
    .barx3 {
        fill: #FFD785;
    }

    /*
    Pretty Table Styling
    CSS Tricks also has a nice writeup: http://css-tricks.com/feature-table-design/
    */

    table {
        overflow:hidden;
        border:1px solid #d3d3d3;
        background:#fefefe;
        width:70%;
        margin:5% auto 0;
        -moz-border-radius:5px; /* FF1+ */
        -webkit-border-radius:5px; /* Saf3-4 */
        border-radius:5px;
        -moz-box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
        -webkit-box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
    }

    th, td {padding:18px 28px 18px; text-align:center; }

    th {padding-top:22px; text-shadow: 1px 1px 1px #fff; background:#e8eaeb;}

    td {border-top:1px solid #e0e0e0; border-right:1px solid #e0e0e0;}

    tr.odd-row td {background:#f6f6f6;}

    td.first, th.first {text-align:left}

    td.last {border-right:none;}

    td {
        background: -moz-linear-gradient(100% 25% 90deg, #fefefe, #f9f9f9);
        background: -webkit-gradient(linear, 0% 0%, 0% 25%, from(#f9f9f9), to(#fefefe));
    }

    tr.odd-row td {
        background: -moz-linear-gradient(100% 25% 90deg, #f6f6f6, #f1f1f1);
        background: -webkit-gradient(linear, 0% 0%, 0% 25%, from(#f1f1f1), to(#f6f6f6));
    }

    th {
        background: -moz-linear-gradient(100% 20% 90deg, #e8eaeb, #ededed);
        background: -webkit-gradient(linear, 0% 0%, 0% 20%, from(#ededed), to(#e8eaeb));
    }

    tr:first-child th.first {
        -moz-border-radius-topleft:5px;
        -webkit-border-top-left-radius:5px; /* Saf3-4 */
    }

    tr:first-child th.last {
        -moz-border-radius-topright:5px;
        -webkit-border-top-right-radius:5px; /* Saf3-4 */
    }

    tr:last-child td.first {
        -moz-border-radius-bottomleft:5px;
        -webkit-border-bottom-left-radius:5px; /* Saf3-4 */
    }

    tr:last-child td.last {
        -moz-border-radius-bottomright:5px;
        -webkit-border-bottom-right-radius:5px; /* Saf3-4 */
    }
    </style>
</head>

<body>

    <h1>Known Skill Matching With States Queue From Measure</h1>
<div id="content">
    <table cellspacing="0">
    <tr><th>Perception ObjID</th><th>Skill ObjID</th><th>Real Name</th><th>Class</th><th>Skill Type</th><th>State Pose</th><th>State Parent</th><th>Skill Parent</th></tr>
{{INSERT_TBL1}}
    </table>

    <table cellspacing="0">
    <tr><th>Operation ID</th><th>Using Skill Primitive</th><th>Pre/Post</th><th>Matching</th><th>State ID</th></tr>
{{INSERT_TBL2}}
    </table>
</div>

    <h1>Unknown Skill Generate Through States Queue From Measure</h1>
    <script src="//cdn.bootcss.com/d3/3.5.12/d3.min.js"></script>
    <!-- <script src="http://d3js.org/d3.v3.min.js"></script> -->
    <script src="http://static.mentful.com/gantt-chart-d3v2.js"></script>
    <script>
{{INSERT_JS_DATA}}

    tasks.sort(function(a, b) {
        return a.endDate - b.endDate;
    });
    var maxDate = tasks[tasks.length - 1].endDate;
    tasks.sort(function(a, b) {
        return a.startDate - b.startDate;
    });
    var minDate = tasks[0].startDate;

    var format = "%H:%M";

    var gantt = d3.gantt().taskTypes(taskNames).taskStatus(taskStatus).tickFormat(format);
    gantt(tasks);

    /* Pretty Table Styling*/
    $(function() {
            /* For zebra striping */
            $("table tr:nth-child(odd)").addClass("odd-row");
            /* For cell text alignment */
            $("table td:first-child, table th:first-child").addClass("first");
            /* For removing the last border */
            $("table td:last-child, table th:last-child").addClass("last");
    });
</script>

</body>

</html>
