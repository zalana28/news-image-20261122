# The World in One Day — Sunday 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/zalana28/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/zalana28/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

Entry for make.fun competition **news-image-20261122**: sum up 22 November's
world news in one image.

## The image

A newspaper front page for Sunday 22 November 2026, built from six stories
verified against multiple sources dated 22 November 2026 (see `NOTES.md`):

1. **Antalya** — COP31 collapses with no deal: the EU rejects a draft with
   no fossil-fuel language; the longest COP ever, the first to fail since 2009.
2. **Bahrain** — Iran claims missile and drone strikes on two U.S. bases;
   Bahrain says an industrial site was hit and two people were hurt.
3. **Dymer, Ukraine** — a Russian drone flattens a five-storey apartment
   block: one dead, 14 missing, nine pulled out alive.
4. **Cikande, Indonesia** — a candy factory fire kills three and leaves
   36 missing.
5. **Mercury** — BepiColombo slips into orbit around Mercury, but a
   thruster glitch cuts its braking burn short.
6. **Portimão** — Marc Márquez takes his eighth MotoGP crown with eighth
   place, after overturning a 102-point deficit to equal Agostini.

## How it is built

- `compose_poster.py` draws the 1024×1024 front page with PIL from
  `assets/hero.png` (an AI-generated dusk scene: an empty summit table with
  scattered papers, storm clouds, missile trails over a Gulf skyline and
  Mercury in the sky — no text in the image itself) plus the story text above.
  Fonts: Playfair Display and Plus Jakarta Sans, both in `assets/fonts/`.
- `main.py` (Python 3.13, standard library only) copies the pre-built
  `entry.png` to `/output/entry.png`. No network; two runs write identical bytes.

## Run it

```sh
python3 compose_poster.py   # rebuild entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
