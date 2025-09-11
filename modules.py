import requests
from bs4 import BeautifulSoup

# URL and DOM parsing setup
url = "https://wiki.pro-tanki.com/en/Paints"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
paint_cards = soup.find_all('div', class_='item-card paint-card')


turret_map = {
    1: "Smoky",
    2: "Flamethrower",
    3: "Twins",
    4: "Railgun",
    5: "Isida",
    6: "Thunder",
    7: "Hammer",
    8: "Freeze",
    9: "Ricochet",
    10: "Vulcan",
    11: "Shaft"
}


def select_turret():
    print("Select a turret by number:")
    for num, turret in turret_map.items():
        print(f"{num}. {turret}")
    try:
        choice = int(input("Enter number: "))
        if 1 <= choice <= len(turret_map):
            return turret_map[choice]
    except:
        pass
    print("Invalid. Try again.")
    return select_turret()

def find_missing_turrets(selected_turret):
    all_turrets = set(turret_map.values())
    seen_turrets = set()

    for card in paint_cards:
        prot_table = card.find('table', class_='wikitable paint-card__protections')
        if not prot_table:
            continue

        has_selected = False
        turrets_in_paint = set()

        for td in prot_table.find_all('td'):
            span = td.find('span')
            if not span:
                continue

            turret_name = span.get('data-resist', '').capitalize()
            text = td.get_text(strip=True)

            if text.endswith('%'):
                try:
                    protection_value = int(text[:-1])
                except ValueError:
                    continue

                if protection_value > 15:
                    turrets_in_paint.add(turret_name)
                    if turret_name == selected_turret:
                        has_selected = True

        if has_selected:
            seen_turrets.update(turrets_in_paint)

    # Turrets never appearing with the selected one
    missing = all_turrets - seen_turrets
    # Optionally remove the selected turret itself
    missing.discard(selected_turret)
    return missing

def main():
    while True:
        chosen = select_turret()
        missing = find_missing_turrets(chosen)

        print(f"\nThe following turrets have no protection with and or have no combined modules over 15% with {chosen}:")
        if missing:
            for t in sorted(missing):
                print(f"- {t}")
        else:
            print("  All turrets appear at least once with the selected turret.")

        cont = input("\nContinue? (y/n): ").lower()
        if cont != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
