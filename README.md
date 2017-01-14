<p align="center">
  <a href="docs/images/logo.png">
    <img src="docs/images/logo.png" height="300" />
  </a>
  <br><br>
</p>

Alizon: Cut out the Middleman
===========================
Alizon lets you know if an Amazon item is not actually an Amazon item at all. Don't be fooled by the vague descriptions, unreliable pictures, and fake reviews; you are likely seeing a generic product from the Chinese website AliExpress.com that has been extravagently marked up for American consumers. Laptop chargers selling for $0.82 on AliExpress are advertised on Amazon for $14.95. Amazon resellers sell clothes hangers for $12.99/dozen, but you can find the identical item on AliExpress for $11.32/100. Trendy clothing is given a fancy description and a 300% premium for uninformed Westerners. Alizon protects you from predatory price gouging by letting you know if the Amazon item you're vieiwng can be purchased directly from the seller at AliExpress. Save money, save time, and cut out the middleman.

<img src="docs/images/comparison.png" />

Finding a Match
----------------------
Alizon extracts an Amazon product's ASIN (Amazon Standard Identification Number) and uses the Amazon API to find more information about the product such as the title, price, and image. It then proceeds to conduct an exhaustive search of the item on AliExpress to find products with equivalent titles. Alizon uses the Python Imaging Library to intelligently find matches between the product images from Amazon and AliExpress, with images over a 95% match being considered the most seriously. An algorithm computes a confidence value of a match based on these results and returns the duplicate AliExpress item.

Deploying the Software
------------------------------
TODO

<p align="center">
  <a href="docs/images/logo_shiny.png">
    <img src="docs/images/logo_shiny.png" height="100" />
  </a>
</p>
