# Week 3 - Task 1: Trace (predicted vs real order of c1, c2, c3)

from counting import c1, c2, c3, six, g

# Predicted before seeing the code of c1, c2 and c3: only the names and
# grades were known, so the grades are sorted 5, 6, 6, 9, 9, 9 and the order
# of equal grades was guessed.
predicted = {
    "c1(six, g)": "Gent Blend Fjolla Arta Dita Edon",
    "c2(six, g, 5, 10)": "Gent Fjolla Blend Edon Dita Arta",
    "c3(six, g, 5, 10)": "Gent Blend Fjolla Arta Dita Edon",
}


def names(rs):
    return " ".join(r["name"] for r in rs)


if __name__ == "__main__":
    real = {
        "c1(six, g)": names(c1(six, g)),
        "c2(six, g, 5, 10)": names(c2(six, g, 5, 10)),
        "c3(six, g, 5, 10)": names(c3(six, g, 5, 10)),
    }
    print(f"{'call':<20}{'predicted order':<36}{'real order':<36}match")
    for call in predicted:
        ok = "yes" if predicted[call] == real[call] else "NO"
        print(f"{call:<20}{predicted[call]:<36}{real[call]:<36}{ok}")
