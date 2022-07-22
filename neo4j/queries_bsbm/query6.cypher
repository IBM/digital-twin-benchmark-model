//Return product and its label where label = "word"

MATCH(product:ns2__ProductType1)
WHERE product.rdfs__label =~ '.*word.*'
RETURN product.uri, product.rdfs__label
