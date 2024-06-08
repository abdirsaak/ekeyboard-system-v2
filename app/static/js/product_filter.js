var searchBox_3 = document.getElementById('searchBox_3');

searchBox_3.addEventListener("keyup", function () {
  var keyword = this.value.toUpperCase();
  var products = document.querySelectorAll(".product_container");

  var filteredProducts = Array.from(products).filter(function (product) {
    var productName = product.getAttribute('data-name')?.toUpperCase();
    return productName && productName.indexOf(keyword) > -1;
  });

  filteredProducts.forEach(function (product) {
    product.style.display = "";
  });

  // Hide products not in filteredProducts (optional)
  products.forEach(function (product) {
    if (!filteredProducts.includes(product)) {
      product.style.display = "none";
    }
  });
});
