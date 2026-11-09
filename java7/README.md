# Week 6: Supply Chain Inventory Deduplication

`dedup.py` finds new supplier listings that are probably the same product as an
inventory product or as another new listing.

```
python dedup.py                          # the assignment's example (built into the code)
python dedup.py inventory.csv new.csv    # CSV columns: product_id, brand, model, description, supplier_id
python checks.py                         # example output + edge cases
python scale_test.py                     # 120,000 products
```

`inventory.csv` and `new.csv` contain the assignment's example data.

## 1. Normalization

Every product becomes a key `(brand, model, sizes, colors)`.

| Attribute | Rule | Example |
|---|---|---|
| brand | lower case, punctuation and extra spaces removed, company words (`inc`, `ltd`, `co`, `electronics`, ...) dropped, aliases (`hewlett packard` → `hp`) | `"Samsung Electronics Co., Ltd."` → `samsung` |
| model | same cleaning, then all spaces removed. The brand at the start is dropped. `+` becomes `plus`, because `S21+` is a different phone than `S21` | `"WH-1000XM4"`, `"WH1000XM4"` → `wh1000xm4` |
| size | taken from the description: a number followed by a unit, with or without a space or hyphen. Units are unified (`"`, `in`, `inches` → `inch`). `G` alone is not a unit, so `5G` is not read as a size | `"128 GB"`, `"128GB"` → `128gb` |
| color | taken from the description, from a list of colors. Abbreviations are expanded (`BLK` → `black`, `Grey` → `gray`) and two-word colors are kept together (`rose gold`, `space gray`) | `"(Black)"`, `"Black Color"` → `black` |

Size and color are sets, so a description can mention several of each in any order: `"Gold 256 GB"` = `"256GB Gold"`.

## 2. Confidence levels

| Level | Rule | Justification |
|---|---|---|
| **HIGH** | brand, model, size and color are all equal after normalization. An attribute missing from both listings counts as equal | All four attributes agree, so only formatting differs. This is the assignment's own definition |
| **MEDIUM** | brand and model are equal, and size or color is given in only one listing. Nothing contradicts | Suppliers often leave out the color or size. Brand and model are the strongest identifiers and they agree, and nothing contradicts, so it is probably the same product. But the missing attribute could hide a different variant (the 128GB or the 256GB model?), so a person should check |
| **LOW** | brand, size and color are equal, and the model differs by exactly one letter (inserted, removed or replaced) | This is most likely a typo (`Galaxy S2l` vs `Galaxy S21`), but it could be a real model name (`iPhone 6` vs `iPhone 6s`). Because the model itself does not match, it is the weakest signal |

The following are **never** grouped:
- **A different color or size on both sides.** These are different variants of the same product, and merging them would mix stock that must stay separate.
- **A model where one digit differs or is added.** Examples: `WH-1000XM3` vs `XM4`, `S21` vs `S211`. In model names a changed digit is usually a different generation, not a typo.
- **A different brand.**

Every group must contain at least one new listing. Duplicates inside the inventory alone are not reported, because the task is to check the new batch.

MEDIUM and LOW groups are pairs of buckets and are never chained into bigger groups. A listing with no size could be the 128GB or the 256GB model. It then appears in two separate MEDIUM groups, and the 128GB and 256GB products are never put into the same group.

## 3. Hash tables and complexity

| Hash table | Key | Used for |
|---|---|---|
| `buckets` | full key `(brand, model, sizes, colors)` | HIGH. Products with the same key land in the same bucket, so a group can have any number of members |
| `byBrandModel` | `(brand, model)` | MEDIUM |
| `byFuzzy` | `(brand, sizes, colors, model with one character deleted)` | LOW. Two models one edit apart always share at least one such key, so no pair of products is ever compared directly |

For n products with model length L, building the tables takes O(n · L) and every lookup is O(1) on average. The total is about linear in n, not the O(n²) of comparing every pair.

On 120,000 products (100,000 inventory + 20,000 new), the run takes about 4 seconds. All 10,000 rewritten copies are found as HIGH, and all 10,000 truly new products are reported as unique.

## 4. Limitations

- **Colors and abbreviations:** only those in the lists are recognized. An unknown color name ("Phantom Violet") is not extracted, so it counts as a missing color.
- **Size units:** `1TB` and `1000GB` are not treated as the same size.
- **Brand misspellings:** a misspelled brand ("Samsnug") is not matched. Only the model allows a one-letter typo.
