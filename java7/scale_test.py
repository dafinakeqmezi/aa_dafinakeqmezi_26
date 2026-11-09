# Week 6 - Assignment: scale test with 100,000+ products
#
# 100,000 inventory products, then 20,000 new ones:
#   10,000 are the same as an inventory product, written differently
#   10,000 are new products that match nothing
# Every rewritten copy must land in a HIGH group, every new product must be unique.

import random
import time

from dedup import findDuplicates

random.seed(7)

BRANDS = ["Samsung", "Apple", "Sony", "LG", "Dell", "Lenovo", "Asus", "Acer", "Xiaomi", "Bose",
          "Philips", "Panasonic", "Canon", "Nikon", "Huawei", "Motorola", "Logitech", "JBL"]
SERIES = ["Galaxy", "iPhone", "Bravia", "OLED TV", "XPS", "ThinkPad", "ZenBook", "Aspire",
          "Redmi", "QuietComfort", "Hue", "Lumix", "EOS", "Coolpix", "Mate", "Moto", "MX", "Flip"]
COLORS = ["Black", "White", "Blue", "Silver", "Gold", "Space Gray", "Red", "Green"]
SHORT = {"Black": "BLK", "White": "WHT", "Silver": "Slvr", "Gold": "Gld",
         "Space Gray": "Space Grey", "Blue": "Blu", "Red": "Red", "Green": "Grn"}
SIZES = [("64", "GB"), ("128", "GB"), ("256", "GB"), ("512", "GB"), ("55", "inch"), ("65", "inch")]


def product(pid, n, supplier):
    color = random.choice(COLORS)
    value, unit = random.choice(SIZES)
    p = {"product_id": pid, "brand": random.choice(BRANDS),
         "model": f"{random.choice(SERIES)} {n}",
         "description": f"{value}{unit} {color}", "supplier_id": supplier}
    return p, (value, unit, color)


def rewrite(p, parts, pid):
    # same product, another supplier's formatting
    value, unit, color = parts
    model = p["model"].replace(" ", random.choice(["-", "  ", ""]))
    description = random.choice([
        f"{value} {unit} - {color} Color",
        f"{SHORT[color]}, {value}{unit.lower()}",
        f"({color.upper()})   {value} {unit}",
    ])
    return {"product_id": pid, "brand": random.choice([p["brand"].upper(), p["brand"].lower() + " Inc."]),
            "model": model, "description": description, "supplier_id": "SUP-NEW"}


inventory, parts = [], []
for i in range(100_000):
    p, x = product(f"PROD{i:06d}", i, f"SUP-{i % 1000:03d}")
    inventory.append(p)
    parts.append(x)

picked = random.sample(range(len(inventory)), 10_000)
new = [rewrite(inventory[j], parts[j], f"NEWD{k:05d}") for k, j in enumerate(picked)]
new += [product(f"NEWU{k:05d}", 100_000 + k, "SUP-NEW")[0] for k in range(10_000)]
random.shuffle(new)

start = time.perf_counter()
groups, unique = findDuplicates(inventory, new)
seconds = time.perf_counter() - start

high = [g for g in groups if g["confidence"] == "HIGH"]
correct = all(
    len(g["members"]) == 2
    and g["members"][0]["product_id"] == f"PROD{picked[int(g['members'][1]['product_id'][4:])]:06d}"
    for g in high
)

print(f"products checked:   {len(inventory) + len(new):,}")
print(f"time:               {seconds:.2f} s")
print(f"HIGH groups:        {len(high):,}  (expected 10,000)")
print(f"MEDIUM/LOW groups:  {len(groups) - len(high):,}  (expected 0)")
print(f"unique new:         {len(unique):,}  (expected 10,000)")
print(f"every copy paired with its own original: {correct}")
print(f"every unique one is a real new product:  {all(p['product_id'].startswith('NEWU') for p in unique)}")
