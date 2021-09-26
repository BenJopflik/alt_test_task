
orderbook_pricelevel_template = """
<tr>
    <td>{price}</td>
    <td>{volume}</td>
</tr>
"""

style = """
<style>

table.asks{
  border:3px solid red;
}

table.asks th, table.asks td {
  border:1px solid red;
}

table.bids {
  border:3px solid green;
}

table.bids th, table.bids td {
  border:1px solid green;
}
</style>
"""

orderbook_template = """
<!DOCTYPE html>
<html>

{style}

<head>
    <title></title>
    <meta http-equiv="refresh" content="10">
</head>
  
<body>
    <h2>{symbol} : {ts}</h2>

    <table class="asks">
    {asks}
    </table>

    <table class="bids">
    {bids}
    </table>

</body>
  
</html>
 
"""