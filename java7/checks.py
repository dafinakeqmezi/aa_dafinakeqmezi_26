# Week 6 - Assignment checks: the example output, normalization, confidence levels

from dedup import (
    INVENTORY, NEW_PRODUCTS, findDuplicates, report,
    normBrand, normModel, extractSizes, extractColors,
)

EXPECTED = """DUPLICATE GROUPS FOUND:
Group 1 (Samsung Galaxy S21):
- PROD001 (Supplier: SUP-A)
- NEW001 (Supplier: SUP-C)
Confidence: HIGH

Group 2 (Sony WH-1000XM4):
- PROD003 (Supplier: SUP-B)
- NEW003 (Supplier: SUP-C)
Confidence: HIGH

Group 3 (Apple iPhone 13 Pro):
- NEW002 (Supplier: SUP-D)
- NEW005 (Supplier: SUP-E)
Confidence: HIGH

NEW UNIQUE PRODUCTS:
- NEW004 (LG OLED TV 55)"""


def check(call, real, expected):
    ok = "yes" if real == expected else "NO"
    if len(str(expected)) > 23:
        print(f"{call:<100}{ok}\n  expected {expected}\n  real     {real}")
    else:
        print(f"{call:<52}{str(expected):<24}{str(real):<24}{ok}")


def P(pid, brand, model, description, supplier="SUP-X"):
    return {"product_id": pid, "brand": brand, "model": model,
            "description": description, "supplier_id": supplier}


def summary(groups, unique):
    # [(confidence, [ids])...], [unique ids]
    return ([(g["confidence"], [p["product_id"] for p in g["members"]]) for g in groups],
            [p["product_id"] for p in unique])


if __name__ == "__main__":
    print(f"{'call':<52}{'expected':<24}{'real':<24}match")

    # the assignment's example, character for character
    check("example output == expected output",
          report(*findDuplicates(INVENTORY, NEW_PRODUCTS)) == EXPECTED, True)
    print()

    # formatting, extra spaces, abbreviations
    check("normBrand('Samsung Electronics Co., Ltd.')", normBrand("Samsung Electronics Co., Ltd."), "samsung")
    check("normBrand('  APPLE  inc ')", normBrand("  APPLE  inc "), "apple")
    check("normModel('WH-1000XM4', 'sony')", normModel("WH-1000XM4", "sony"), "wh1000xm4")
    check("normModel('Samsung Galaxy S21', 'samsung')", normModel("Samsung Galaxy S21", "samsung"), "galaxys21")
    check("normModel('Galaxy S21+') == 'Galaxy S21 Plus'",
          normModel("Galaxy S21+", "samsung") == normModel("Galaxy S21 Plus", "samsung"), True)
    check("normModel('Galaxy S21+') != 'Galaxy S21'",
          normModel("Galaxy S21+", "samsung") != normModel("Galaxy S21", "samsung"), True)
    check("extractSizes('128 GB - Black Color')", extractSizes("128 GB - Black Color"), ("128gb",))
    check("extractSizes('55\" 4K')", extractSizes('55" 4K'), ("55inch",))
    check("extractSizes('55-Inch UHD')", extractSizes("55-Inch UHD"), ("55inch",))
    check("extractSizes('Galaxy S21 5G')", extractSizes("Galaxy S21 5G"), ())
    check("extractSizes('2 in 1 laptop')", extractSizes("2 in 1 laptop"), ())
    check("extractSizes('8GB RAM, 256 GB')", extractSizes("8GB RAM, 256 GB"), ("256gb", "8gb"))
    check("extractColors('Space Grey')", extractColors("Space Grey"), ("space gray",))
    check("extractColors('(BLK)')", extractColors("(BLK)"), ("black",))
    check("extractColors('Navy Blue')", extractColors("Navy Blue"), ("navy",))
    check("extractColors('55 inch 4K')", extractColors("55 inch 4K"), ())
    print()

    inv = [
        P("PROD001", "Samsung", "Galaxy S21", "128GB Black", "SUP-A"),
        P("PROD002", "Sony", "WH-1000XM3", "Headphones Black", "SUP-B"),
    ]

    # three listings with the same normalized attributes form ONE group
    new = [
        P("NEW001", "SAMSUNG", "Galaxy S21", "128 GB - Black Color"),
        P("NEW002", "samsung  electronics", "galaxy-s21", "Black, 128gb"),
    ]
    check("3 members in one HIGH group", summary(*findDuplicates(inv, new)),
          ([("HIGH", ["PROD001", "NEW001", "NEW002"])], []))

    # two new listings, neither in inventory
    new = [P("NEW001", "Dell", "XPS 13", "16GB Silver"), P("NEW002", "DELL", "XPS-13", "Slvr 16 GB")]
    check("two new listings, no inventory", summary(*findDuplicates(inv, new)),
          ([("HIGH", ["NEW001", "NEW002"])], []))

    # a missing attribute on both sides counts as a match
    new = [P("NEW001", "Sony", "WH1000XM3", "Headphones (Black)")]
    check("size missing on both -> HIGH", summary(*findDuplicates(inv, new)),
          ([("HIGH", ["PROD002", "NEW001"])], []))

    # MEDIUM: same brand and model, size given in only one listing
    new = [P("NEW001", "Samsung", "Galaxy S21", "Black")]
    check("size missing on one side -> MEDIUM", summary(*findDuplicates(inv, new)),
          ([("MEDIUM", ["PROD001", "NEW001"])], []))

    # LOW: one letter typo in the model
    new = [P("NEW001", "Samsung", "Galaxy S2l", "128GB Black")]
    check("model typo S2l -> LOW", summary(*findDuplicates(inv, new)),
          ([("LOW", ["PROD001", "NEW001"])], []))

    # not duplicates
    new = [P("NEW001", "Sony", "WH-1000XM4", "Headphones Black")]
    check("XM3 vs XM4 (digit changed) -> unique", summary(*findDuplicates(inv, new)), ([], ["NEW001"]))
    new = [P("NEW001", "Samsung", "Galaxy S21", "128GB White")]
    check("other color -> unique", summary(*findDuplicates(inv, new)), ([], ["NEW001"]))
    new = [P("NEW001", "Samsung", "Galaxy S21", "256GB Black")]
    check("other size -> unique", summary(*findDuplicates(inv, new)), ([], ["NEW001"]))
    new = [P("NEW001", "Samsung", "Galaxy S21+", "128GB Black")]
    check("S21+ vs S21 -> unique", summary(*findDuplicates(inv, new)), ([], ["NEW001"]))
    new = [P("NEW001", "Apple", "Galaxy S21", "128GB Black")]
    check("other brand -> unique", summary(*findDuplicates(inv, new)), ([], ["NEW001"]))

    # duplicates inside the inventory alone are not reported (nothing new to check)
    inv2 = inv + [P("PROD003", "SAMSUNG", "Galaxy-S21", "128 GB Black")]
    check("inventory-only duplicates not reported", summary(*findDuplicates(inv2, [])), ([], []))
