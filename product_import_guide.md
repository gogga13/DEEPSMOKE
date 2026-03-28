# Product Import Guide

Use this file pair for manual filling in Google Sheets or Excel:

- `D:\Python\Deepsmoke\product_import_google_sheets_template.csv`
- `D:\Python\Deepsmoke\product_import_example.csv`

## Exact column names

The first row must stay exactly like this:

```text
id,category,name,brand,sku,description,price,image,is_active,variant_names,variant_images
```

## Current category names in the project

Use these exact values in the `category` column:

- `Pod system`
- `Liquids`
- `Disposables`
- `Cartridge`

If you use a new category name, the importer will create it automatically.

## What to put in each column

- `id`: leave empty for new products; fill only if you want to update an existing product by ID
- `category`: category name text
- `name`: product name
- `brand`: brand name
- `sku`: article / SKU; strongly recommended for stable repeated imports
- `description`: product description
- `price`: number only, for example `1299.00`
- `image`: optional path to an already uploaded image, for example `products/xros4-black.jpg`
- `is_active`: `1` for active, `0` for inactive
- `variant_names`: optional list of flavors / colors / options, separated by `|`
- `variant_images`: optional list of image paths for variants, also separated by `|`

## How to fill flavors and colors

If one product has multiple flavors or colors and the same price, use one row:

```text
,Liquids,Chaser Salt 30ml,Chaser,CHASER-SALT-30,Line of salt liquids,350.00,,1,Berry Mix|Mint|Mango,
```

or:

```text
,Pod system,Vaporesso XROS 4,Vaporesso,XROS4,Pod system line,1299.00,,1,Black|Silver|Blue,
```

If variants have different prices, create separate rows instead of using `variant_names`.

## Variant image rules

- `variant_images` is optional
- use the same order as in `variant_names`
- if you fill `variant_images`, the number of items must match `variant_names`

Example:

```text
Black|Silver|Blue
products/variants/xros4-black.jpg|products/variants/xros4-silver.jpg|products/variants/xros4-blue.jpg
```

## Fast workflow

1. Open `product_import_google_sheets_template.csv` in Google Sheets.
2. Replace the example rows with your real products.
3. Keep the header row unchanged.
4. Export from Google Sheets as `CSV` or `XLSX`.
5. Import the file in Django admin for `Product`.
