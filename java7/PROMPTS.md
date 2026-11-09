I have an assignment from Advanced Algorithms (Week 6): "Supply Chain Inventory Deduplication". Implement it in Python, using only the standard library. Please do the following:

1. Create a file dedup.py. A product has the fields product_id, brand, model, description and supplier_id. Put the assignment's example data in the file (inventory PROD001–PROD003, new products NEW001–NEW005). Also add loadCsv(path) so the program can run as python dedup.py inventory.csv new.csv, and create inventory.csv and new.csv with the example data.

2. Normalize every product into a composite key (brand, model, sizes, colors):
   - normBrand(brand): lower case, remove punctuation and extra spaces, drop company words (inc, ltd, co, corp, electronics, ...), map aliases (hewlett packard -> hp).
   - normModel(model, brand): same cleaning, then remove all spaces so "WH-1000XM4" and "WH1000XM4" become "wh1000xm4". Drop the brand if the model starts with it. Keep every letter and digit, so "iPhone 13" and "iPhone 14" stay different, and turn "+" into "plus" so "S21+" is not "S21".
   - extractSizes(description): size is not a separate field, so take it from the description: a number followed by a unit (GB, TB, MB, inch, inches, in, ", ml, l, oz, kg, lb, ...), with or without a space or hyphen. "128GB" and "128 GB" -> "128gb". "5G" and "2 in 1" are not sizes.
   - extractColors(description): color is not a separate field either. Find colors anywhere in the description, expand abbreviations (BLK -> black, Grey -> gray) and keep two-word colors together (rose gold, space gray).
   - normalize(p) returns the key.

3. Use hash tables (Python dicts) as the core of the solution, never comparing every pair (no O(N^2)):
   - buckets: full key -> every product with that key. A new product meets its inventory twin and its twins in the same batch in one lookup, and all products with the same key form ONE group, so a group can have more than two members.
   - byBrandModel: (brand, model) -> keys, for MEDIUM candidates.
   - byFuzzy: (brand, sizes, colors, model with one character deleted) -> keys, for LOW candidates (one-letter typos).

4. Confidence levels. Define each rule and justify it:
   - HIGH: brand, model, size and color are identical after normalization. An attribute missing from both listings counts as identical.
   - MEDIUM: brand and model are identical, size or color is given in only one listing, and nothing contradicts.
   - LOW: brand, size and color are identical and the model differs by exactly one letter (a likely typo, e.g. "Galaxy S2l" / "Galaxy S21"). A changed or added digit is never a typo (XM3 vs XM4).
   - Never group products whose size or color differ (different variants) or whose brand differs.
   - Every group must contain at least one new product. Lower-level groups are pairs of buckets and are never chained into bigger groups.

5. findDuplicates(inventory, newProducts) returns the groups and the new products that have no duplicate. report(groups, unique) prints them exactly in the assignment's format: "DUPLICATE GROUPS FOUND:", each "Group n (Brand Model):" with "- ID (Supplier: ...)" lines and "Confidence: ...", a "Reason: ..." line for MEDIUM and LOW, then "NEW UNIQUE PRODUCTS:".

6. Testing:
   - checks.py: check that the example output is exactly the assignment's expected output, then check normalization (capitalization, extra spaces, punctuation, abbreviations, units, 5G, "2 in 1") and the grouping rules (3 members in one group, duplicates only in the new batch, size missing in both -> HIGH, size missing in one -> MEDIUM, typo -> LOW, different size / color / brand / XM3 vs XM4 / S21 vs S21+ -> unique, duplicates only inside the inventory are not reported).
   - scale_test.py: 100,000 inventory products plus 20,000 new ones (10,000 rewritten copies with different formatting, 10,000 truly new). Every copy must be in a HIGH group with its own original, every new product must be unique. Print the time.

7. Write a README.md with how to run the program, the normalization rules, the confidence levels with a justification for each rule (why MEDIUM and LOW were chosen and why different sizes or colors are never grouped), the hash tables and the time complexity, and the limitations.

8. Run python dedup.py, python checks.py and python scale_test.py, show me the full output, tell me if any result differs from the expected one, and briefly explain how normalization, the hash tables and the confidence levels work and why the solution scales to 100,000+ products.
