# Week 6 - Assignment: Supply Chain Inventory Deduplication

import csv
import re
import sys
import unicodedata

# ---------- normalization ----------

COMPANY_WORDS = {"inc", "ltd", "llc", "co", "corp", "corporation", "company", "gmbh", "electronics"}
BRAND_ALIASES = {"hewlett packard": "hp"}

COLORS = {
    "black", "white", "blue", "red", "green", "gold", "silver", "gray", "pink", "purple",
    "yellow", "orange", "brown", "beige", "navy", "graphite", "midnight", "starlight",
    "bronze", "teal", "violet", "ivory",
}
MULTI_COLORS = {
    "rose gold": "rose gold", "space gray": "space gray", "sky blue": "sky blue",
    "navy blue": "navy", "jet black": "black",
}
COLOR_ABBREV = {
    "blk": "black", "bk": "black", "wht": "white", "grey": "gray", "gry": "gray",
    "slv": "silver", "slvr": "silver", "gld": "gold", "blu": "blue", "grn": "green",
    "pnk": "pink", "prpl": "purple", "ylw": "yellow", "brn": "brown",
}

# a number followed by a unit: "128GB", "128 GB", "55-inch", '55"', "1.5 l"
# "g" alone is not a unit, so "5G" (network) is not read as 5 grams
SIZE_RE = re.compile(
    r'(?<![a-z0-9.])(\d+(?:\.\d+)?)\s*-?\s*'
    r'(tb|gb|mb|inches|inch|in(?!\s*\d)|"|ml|litres?|liters?|l|oz|kg|grams?|gr|lbs?|mm|cm)'
    r'(?![a-z0-9])'
)
UNITS = {
    "inches": "inch", "in": "inch", '"': "inch",
    "litre": "l", "litres": "l", "liter": "l", "liters": "l",
    "gram": "g", "grams": "g", "gr": "g", "lbs": "lb",
}


def fold(s):
    # lower case, accents removed: "Señor" -> "senor"
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def clean(s):
    # every run of non-alphanumerics becomes one space:
    # "Noise-Cancelling  (Black)" -> "noise cancelling black"
    return re.sub(r"[^a-z0-9]+", " ", fold(s)).strip()


def normBrand(brand):
    words = [w for w in clean(brand).split() if w not in COMPANY_WORDS]
    b = " ".join(words)
    return BRAND_ALIASES.get(b, b)


def normModel(model, brand):
    # "+" carries meaning ("S21+" is not "S21"), so keep it as a word
    words = clean((model or "").replace("+", " plus ")).split()
    b = brand.split()
    if b and words[:len(b)] == b:  # "Samsung Galaxy S21" under brand Samsung
        words = words[len(b):]
    return "".join(words)  # "WH-1000XM4" and "WH1000XM4" -> "wh1000xm4"


def extractSizes(description):
    sizes = set()
    for value, unit in SIZE_RE.findall(fold(description)):
        v = float(value)
        v = str(int(v)) if v.is_integer() else str(v)
        sizes.add(v + UNITS.get(unit, unit))
    return tuple(sorted(sizes))


def extractColors(description):
    words = [COLOR_ABBREV.get(w, w) for w in clean(description).split()]
    colors = set()
    i = 0
    while i < len(words):
        pair = " ".join(words[i:i + 2])
        if pair in MULTI_COLORS:
            colors.add(MULTI_COLORS[pair])
            i += 2
            continue
        if words[i] in COLORS:
            colors.add(words[i])
        i += 1
    return tuple(sorted(colors))


def normalize(p):
    brand = normBrand(p.get("brand"))
    model = normModel(p.get("model"), brand)
    desc = p.get("description")
    return (brand, model, extractSizes(desc), extractColors(desc))


# ---------- matching rules for the lower levels ----------

def compatible(a, b):
    # sizes and colors may be missing on one side, but never different
    for x, y in ((a[2], b[2]), (a[3], b[3])):
        if x and y and x != y:
            return False
    return True


def deletes(model):
    # the model itself and every copy with one character removed
    out = {model}
    for i in range(len(model)):
        out.add(model[:i] + model[i + 1:])
    return out


def isTypo(a, b):
    # exactly one character inserted, removed or replaced, and the edit
    # neither turns a digit into another digit nor adds a digit
    if min(len(a), len(b)) < 4:
        return False
    if len(a) == len(b):
        diff = [i for i in range(len(a)) if a[i] != b[i]]
        return len(diff) == 1 and not (a[diff[0]].isdigit() and b[diff[0]].isdigit())
    if abs(len(a) - len(b)) != 1:
        return False
    longer, shorter = (a, b) if len(a) > len(b) else (b, a)
    i = 0
    while i < len(shorter) and longer[i] == shorter[i]:
        i += 1
    return longer[:i] + longer[i + 1:] == shorter and not longer[i].isdigit()


def missingSide(a, b):
    names = []
    if a[2] != b[2]:
        names.append("size")
    if a[3] != b[3]:
        names.append("color")
    return " and ".join(names)


# ---------- grouping ----------

def findDuplicates(inventory, newProducts):
    records = [{"p": p, "isNew": False} for p in inventory]
    records += [{"p": p, "isNew": True} for p in newProducts]

    # hash table 1: full normalized key -> every product with that key (HIGH)
    buckets = {}
    for i, r in enumerate(records):
        r["key"] = normalize(r["p"])
        buckets.setdefault(r["key"], []).append(i)

    # hash table 2: (brand, model) -> keys (MEDIUM)
    # hash table 3: (brand, sizes, colors, model with one char deleted) -> keys (LOW)
    byBrandModel = {}
    byFuzzy = {}
    for key in buckets:
        brand, model, sizes, colors = key
        byBrandModel.setdefault((brand, model), []).append(key)
        if model:
            for d in deletes(model):
                byFuzzy.setdefault((brand, sizes, colors, d), []).append(key)

    def hasNew(key):
        return any(records[i]["isNew"] for i in buckets[key])

    groups = []
    for key, members in buckets.items():
        if len(members) >= 2 and hasNew(key):
            groups.append({"confidence": "HIGH", "members": members, "reason": ""})

    seen = set()
    lower = []
    for key in buckets:
        if not hasNew(key) or not key[0] or not key[1]:
            continue
        brand, model, sizes, colors = key

        for other in byBrandModel[(brand, model)]:
            pair = frozenset((key, other))
            if other != key and pair not in seen and compatible(key, other):
                seen.add(pair)
                lower.append({
                    "confidence": "MEDIUM",
                    "members": sorted(buckets[key] + buckets[other]),
                    "reason": f"same brand and model, {missingSide(key, other)} "
                              f"given in only one listing",
                })

        for d in deletes(model):
            for other in byFuzzy.get((brand, sizes, colors, d), ()):
                pair = frozenset((key, other))
                if other[1] != model and pair not in seen and isTypo(model, other[1]):
                    seen.add(pair)
                    lower.append({
                        "confidence": "LOW",
                        "members": sorted(buckets[key] + buckets[other]),
                        "reason": f"same brand, size and color; model differs by one "
                                  f"character ({min(model, other[1])} / {max(model, other[1])})",
                    })

    rank = {"MEDIUM": 0, "LOW": 1}
    lower.sort(key=lambda g: (rank[g["confidence"]], g["members"][0]))
    groups += lower

    grouped = set()
    for g in groups:
        g["name"] = displayName(records[g["members"][0]]["p"])
        grouped.update(g["members"])
        g["members"] = [records[i]["p"] for i in g["members"]]
    unique = [r["p"] for i, r in enumerate(records) if r["isNew"] and i not in grouped]
    return groups, unique


def displayName(p):
    return " ".join(f"{p.get('brand') or ''} {p.get('model') or ''}".split())


# ---------- input / output ----------

def report(groups, unique):
    lines = ["DUPLICATE GROUPS FOUND:"]
    if not groups:
        lines.append("(none)")
    for n, g in enumerate(groups, 1):
        lines.append(f"Group {n} ({g['name']}):")
        for p in g["members"]:
            lines.append(f"- {p['product_id']} (Supplier: {p['supplier_id']})")
        lines.append(f"Confidence: {g['confidence']}")
        if g["reason"]:
            lines.append(f"Reason: {g['reason']}")
        lines.append("")
    lines.append("NEW UNIQUE PRODUCTS:")
    if not unique:
        lines.append("(none)")
    for p in unique:
        lines.append(f"- {p['product_id']} ({displayName(p)})")
    return "\n".join(lines)


def loadCsv(path):
    # columns: product_id, brand, model, description, supplier_id
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


INVENTORY = [
    {"product_id": "PROD001", "brand": "Samsung", "model": "Galaxy S21",
     "description": "128GB Black", "supplier_id": "SUP-A"},
    {"product_id": "PROD002", "brand": "Apple", "model": "iPhone 13",
     "description": "256GB Blue", "supplier_id": "SUP-A"},
    {"product_id": "PROD003", "brand": "Sony", "model": "WH-1000XM4",
     "description": "Noise Cancelling Headphones Black", "supplier_id": "SUP-B"},
]

NEW_PRODUCTS = [
    {"product_id": "NEW001", "brand": "SAMSUNG", "model": "Galaxy S21",
     "description": "128 GB - Black Color", "supplier_id": "SUP-C"},
    {"product_id": "NEW002", "brand": "Apple", "model": "iPhone 13 Pro",
     "description": "256GB Gold", "supplier_id": "SUP-D"},
    {"product_id": "NEW003", "brand": "Sony", "model": "WH1000XM4",
     "description": "Noise-Cancelling Headphones (Black)", "supplier_id": "SUP-C"},
    {"product_id": "NEW004", "brand": "LG", "model": "OLED TV 55",
     "description": "55 inch 4K", "supplier_id": "SUP-D"},
    {"product_id": "NEW005", "brand": "APPLE", "model": "iPhone 13 Pro",
     "description": "Gold 256 GB", "supplier_id": "SUP-E"},
]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        inventory, newProducts = loadCsv(sys.argv[1]), loadCsv(sys.argv[2])
    else:
        inventory, newProducts = INVENTORY, NEW_PRODUCTS
    print(report(*findDuplicates(inventory, newProducts)))
