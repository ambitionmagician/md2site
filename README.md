# Md2Site

by Dr. Brent Allen Jensen

Turn a folder of Markdown files into a small static website: one HTML
page per file, wrapped in a clean minimal template, plus an index
page linking them all. No build system, no JavaScript, no tracking —
just files you can host anywhere.

## Quickstart

```bash
pip install -r requirements.txt        # just `markdown`

python3 md2site.py notes/ site/
python3 md2site.py docs/ public/ --site-title "Field Notes"
```

Each page's title comes from its first `#` heading, falling back to
the filename. Subfolders are mirrored in the output, and the index
lists every page by relative path.

## Options

| Flag | Default | Meaning |
|---|---|---|
| `--site-title` | `Site` | Used in the index heading and page footers |
| `--css FILE` | — | Link this external stylesheet instead of the tiny inline default |

## Requirements

- Python 3.10+, `markdown`

## Notes

- Relative links between your Markdown files that point at other
  `.md` files are rewritten to the generated `.html` names.
- Non-Markdown files (images and the like) are not copied; reference
  them with paths that work in the output tree, or copy them alongside.
- The output is deliberately plain. It loads instantly, prints
  cleanly, and will still render in twenty years.

## Support this work

If this tool saved you time or taught you something, donations keep the work going:

- BTC: 15McijPo79Zx58NGyEf2PvaPtGqGmpztWn
- ETH: 0x8C25164E9234E6A30b8E44485B79c5cE8419cF2B

## License

MIT — see [LICENSE](LICENSE).
