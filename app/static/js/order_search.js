var search_orders = document.getElementById('search_orders');

search_orders.addEventListener("keyup", function () {
  var keyword = this.value.toUpperCase();
  var order_table = document.querySelectorAll(".order-table tr");

  order_table.forEach(function (row) {
    var cells = row.querySelectorAll("td");
    var rowText = Array.from(cells).map(cell => cell.textContent.toUpperCase()).join(" ");
    
    if (rowText.includes(keyword)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
});
