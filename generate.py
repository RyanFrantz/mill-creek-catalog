#!/usr/bin/env python3
"""Reads catalog.md and writes index.html."""

from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).parent
CATALOG = HERE / 'catalog.md'
OUTPUT = HERE / 'index.html'

SECTION_ORDER = [
    'amphibians-reptiles',
    'birds',
    'insects-arachnids',
    'mammals-fish',
    'mushrooms',
    'plants',
]

SECTION_NAMES = {
    'amphibians-reptiles': 'Amphibians and Reptiles',
    'birds': 'Birds',
    'insects-arachnids': 'Insects and Arachnids',
    'mammals-fish': 'Mammals and Fish',
    'mushrooms': 'Mushrooms',
    'plants': 'Plants',
}

SECTION_NOTES = {
    'mushrooms': (
        '      <p>There are several species of mushroom present around the creek, '
        'including agarics, boletes, jellies, polyspores, shelf, and more. '
        'The author is not experienced enough to identify them properly.</p>\n'
    ),
}

STATIC_HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mill Creek Catalog</title>
  <style>
    :root {
      --measure: 60ch;
      --color-text: #1c1c1c;
      --color-bg: #f8f7f2;
      --color-muted: #54534e;
      --color-border: #ccc9be;
      --color-accent: #3d5e3a;
      --color-th-bg: #eceae2;
    }

    * {
      box-sizing: border-box;
      max-inline-size: var(--measure);
    }

    html,
    body,
    div,
    header,
    nav,
    main,
    footer,
    search,
    section,
    details {
      max-inline-size: none;
    }

    body {
      font-family: system-ui, -apple-system, sans-serif;
      line-height: 1.6;
      color: var(--color-text);
      background: var(--color-bg);
      max-inline-size: 72rem;
      margin: 0 auto;
      padding: 2rem clamp(1rem, 4vw, 3rem);
    }

    header {
      margin-block-end: 3rem;
      padding-block-end: 1.5rem;
      border-block-end: 3px solid var(--color-accent);
    }

    h1 {
      font-size: clamp(1.75rem, 5vw, 2.75rem);
      line-height: 1.2;
      color: var(--color-accent);
      margin-block: 0 0.5rem;
    }

    header p {
      margin: 0;
      color: var(--color-muted);
    }

    search {
      display: block;
      margin-block-end: 2.5rem;
    }

    search label {
      display: block;
      font-size: 0.8rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--color-muted);
      margin-block-end: 0.4rem;
    }

    .search-row {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      max-inline-size: 30rem;
    }

    #search,
    #search-clear {
      padding: 0.5rem 0.75rem;
      font-size: 1rem;
      font-family: inherit;
      color: var(--color-text);
      background: var(--color-bg);
      border: 1px solid var(--color-border);
      border-radius: 0.25rem;
    }

    #search {
      inline-size: 100%;
    }

    #search-clear {
      cursor: pointer;
      color: var(--color-muted);
      flex-shrink: 0;
    }

    #search:focus,
    #search-clear:focus {
      outline: 2px solid var(--color-accent);
      outline-offset: 1px;
      border-color: var(--color-accent);
    }

    section {
      margin-block-end: 3rem;
    }

    h2 {
      font-size: 1.1rem;
      color: var(--color-accent);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      border-block-end: 2px solid var(--color-accent);
      padding-block-end: 0.25rem;
      margin-block-end: 0.75rem;
    }

    .catalog {
      display: grid;
      grid-template-columns: max-content max-content max-content;
      column-gap: 1.5rem;
      overflow-x: auto;
    }

    .catalog-header,
    .catalog-row {
      display: contents;
    }

    .catalog-row[hidden] {
      display: none;
    }

    .catalog-header > div {
      padding-block: 0.5rem;
      background: var(--color-th-bg);
      font-size: 0.8rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--color-muted);
      border-block-end: 2px solid var(--color-border);
      white-space: nowrap;
    }

    .catalog-row > div {
      padding-block: 0.45rem;
      border-block-end: 1px solid var(--color-border);
    }

    .catalog-row:last-child > div {
      border-block-end: none;
    }

    summary {
      cursor: pointer;
      list-style: none;
    }

    summary::-webkit-details-marker {
      display: none;
    }

    summary h2 {
      display: flex;
      align-items: center;
    }

    summary h2::after {
      content: '▸';
      font-size: 2em;
      margin-inline-start: 0.25em;
      opacity: 0.6;
    }

    details[open] summary h2::after {
      content: ' ▾';
    }

    details > .table-wrap {
      margin-block-start: 0.75rem;
    }


    .species {
      font-style: italic;
      color: var(--color-muted);
    }

    .observation {
      color: var(--color-muted);
      font-size: 0.9em;
      white-space: nowrap;
    }
  </style>
</head>
<body>

<header>
  <h1>Mill Creek Catalog</h1>
  <p>Species observed within and around Mill Creek in Arnold, Maryland.</p>
</header>

<search>
  <label for="search">Search species</label>
  <div class="search-row">
    <input type="search" id="search" placeholder="Common or species name…">
    <button type="button" id="search-clear" title="Clear search" aria-label="Clear search">&times;</button>
  </div>
</search>

<main>
"""

STATIC_FOOT = """\
</main>

<script>
  const searchInput = document.querySelector('#search');
  const searchClear = document.querySelector('#search-clear');
  const searchLabel = document.querySelector('label[for="search"]');

  // Compute section totals and search label count from the DOM.
  document.querySelectorAll('section').forEach(section => {
    const h2 = section.querySelector('summary h2');
    const count = section.querySelectorAll('.catalog-row').length;
    h2.dataset.baseLabel = h2.textContent.trim();
    h2.textContent = `${h2.dataset.baseLabel} (${count})`;
  });

  const totalCount = document.querySelectorAll('.catalog-row').length;
  searchLabel.textContent = `Search ${totalCount} species`;

  searchClear.addEventListener('click', () => {
    searchInput.value = '';
    searchInput.dispatchEvent(new Event('input'));
    searchInput.focus();
  });

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();

    document.querySelectorAll('section').forEach(section => {
      const rows = section.querySelectorAll('.catalog-row');
      const h2 = section.querySelector('summary h2');
      const totalRows = rows.length;

      let matchCount = 0;

      rows.forEach(row => {
        const commonName = row.children[0].textContent.toLowerCase();
        const speciesName = row.children[1].textContent.toLowerCase();
        const matches = !query || commonName.includes(query) || speciesName.includes(query);
        row.hidden = !matches;
        if (matches) matchCount++;
      });

      if (query) {
        section.hidden = matchCount === 0;
        if (matchCount > 0) section.querySelector('details').open = true;
        h2.textContent = `${h2.dataset.baseLabel} (${matchCount})`;
      } else {
        section.hidden = false;
        rows.forEach(row => row.hidden = false);
        h2.textContent = `${h2.dataset.baseLabel} (${totalRows})`;
      }
    });
  });
</script>
</body>
</html>
"""


def render_species(value):
    """Return the HTML <div> for a species field value."""
    if not value or value == 'N/A':
        return '<div></div>'
    # Biological family names (e.g. Lycosidae) are not italicised.
    if value.endswith('idae') or value.endswith('aceae'):
        return f'<div>{value}</div>'
    # Genus-level identification: italicise the genus, leave " sp." plain.
    if value.endswith(' sp.'):
        genus = value[:-4]
        return f'<div><i class="species">{genus}</i> sp.</div>'
    return f'<div><i class="species">{value}</i></div>'


def parse_catalog(path):
    lines = Path(path).read_text(encoding='utf-8').splitlines()
    rows = []
    for line in lines[2:]:  # skip header row and separator row
        if not line.startswith('|'):
            continue
        # Split on | with a limit so the observation field can contain HTML.
        parts = [p.strip() for p in line.strip('|').split('|', 3)]
        if len(parts) == 4:
            rows.append({
                'common': parts[0],
                'species': parts[1],
                'observation': parts[2],
                'category': parts[3],
            })
    return rows


def render_section(cat, rows):
    heading_id = f'heading-{cat}'
    name = SECTION_NAMES[cat]
    out = []
    out.append(f'  <section aria-labelledby="{heading_id}">\n')
    out.append(f'    <details>\n')
    out.append(f'      <summary><h2 id="{heading_id}">{name}</h2></summary>\n')
    if cat in SECTION_NOTES:
        out.append(SECTION_NOTES[cat])
    out.append(f'      <div class="catalog">\n')
    out.append(f'        <div class="catalog-header">\n')
    out.append(f'          <div>Common Name</div>\n')
    out.append(f'          <div>Species</div>\n')
    out.append(f'          <div>Observation Type</div>\n')
    out.append(f'        </div>\n')
    for row in rows:
        species_html = render_species(row['species'])
        obs = row['observation']
        out.append(
            f'          <div class="catalog-row">'
            f'<div>{row["common"]}</div>'
            f'{species_html}'
            f'<div class="observation">{obs}</div>'
            f'</div>\n'
        )
    out.append(f'      </div>\n')
    out.append(f'    </details>\n')
    out.append(f'  </section>\n')
    return ''.join(out)


def main():
    rows = parse_catalog(CATALOG)

    by_cat = defaultdict(list)
    for row in rows:
        by_cat[row['category']].append(row)

    for cat in SECTION_ORDER:
        by_cat[cat].sort(key=lambda r: r['common'].lower())

    sections = []
    for cat in SECTION_ORDER:
        sections.append(render_section(cat, by_cat[cat]))
        sections.append('\n')  # blank line after each section

    OUTPUT.write_text(STATIC_HEAD + '\n' + ''.join(sections) + STATIC_FOOT, encoding='utf-8')
    print(f'Wrote {OUTPUT}')


if __name__ == '__main__':
    main()
