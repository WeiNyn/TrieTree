import pandas as pd

df = pd.read_csv("new_merged_csv.csv")


def check_input(words: str) -> str:
    texts = words.replace("\r", " ") \
        .replace("\n", " ") \
        .replace("- ", "-") \
        .replace(" -", "-") \
        .split(",")

    new_texts = []
    for text in texts:
        if not text.strip().isdigit() and 3 < len(text.strip()) < 50 \
                and "hs code" not in text.lower() \
                and "phone" not in text.lower() \
                and "fax" not in text.lower() \
                and "no." not in text.lower() \
                and "tax" not in text.lower() \
                and "hs-code" not in text.lower():
            new_texts.append(text)

    return ",".join(new_texts)


print(df.size)
df["DESC_BKG"] = df["DESC_BKG"].apply(check_input)
print(df.head(5))
df = df[df["DESC_BKG"].map(len) > 0]
print(df.size)

print(df.head(10))

print(check_input("NECTARINES\nHS CODE: 080930"), "----------")

df.to_csv("new_merged_csv_removed.csv")
