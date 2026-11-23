# news-image-20261122 v2 — working notes (23 Nov 2026)

Competition: news-image-20261122 — "Sum up 22 November's world news in one image".
Pot $100 (1st $20, top 50 share). Deadline 2026-11-24T00:00:00Z (24 Nov 07:00 WIB).
v1 (6 stories) was submitted 23 Nov 10:21 WIB and scored; v2 supersedes it.

## Why v2
Winner formula, researched from the public submissions list of
news-image-20261118 (18,017 entries; analysis in
~/workspace/makefun/analysis-news-image-winners-20261118.md): the rank-2
poster held 52 stories — 4 illustrated leads + 12 grid + 36 numbered —
with a UTC timeline, a world map, a BY FIELD bar, a confidence label on
every story, and a DATE CHECK box. Our v1 had 6 stories and none of that
(rank 5,395/18,017). A rank-20 entry cost $0.00 to build: structure beats
compute. v2 applies the formula at 24 stories.

## The 24 stories (each verified against 2+ sources dated 22 Nov 2026)

LEADS
1. ANTALYA — COP31 ends with no deal (CONFIRMED). CNN 22 Nov; Reuters 22 Nov;
   UN News 22 Nov. EU rejected a draft omitting fossil fuels; longest COP ever.
2. BENGHAZI — Russian warship sunk (REPORTED). Reuters 22 Nov; AP 22 Nov;
   CNN 22 Nov. Suspected Ukrainian sea drones hit corvette Merkury; it capsized
   and sank; a second ship (Ascalon) also hit; 10 injured.
3. WASHINGTON — Democrats clinch 258 House seats (CONFIRMED). AP 22 Nov;
   Reuters 22 Nov. Hubbard beat Foxx in NC; largest majority since 1992; +44.
4. BAHRAIN — Iran strikes US bases (CONFIRMED). Xinhua 22 Nov 00:15Z; Reuters
   22 Nov. IRGC claims missile + drone strikes on Al-Riffa and Awali; Bahrain
   confirms an industrial plant hit and 2 injured.

GRID
5. DYMER — drone flattens apartment block, 1 dead, 14 missing (CONFIRMED).
   Reuters 22 Nov; Euronews 22 Nov.
6. MERCURY — BepiColombo enters orbit (CONFIRMED). AP 22 Nov; Reuters 22 Nov.
   Burn was Sat 21 Nov ~18:25 UTC; ESA confirmation came Sun 22 Nov.
7. CIKANDE — candy factory fire, 3 dead, 37 missing (CONFIRMED). AP 22 Nov;
   Euronews 22 Nov.
8. PORTIMAO — Marquez eighth MotoGP crown (CONFIRMED). Reuters 22 Nov;
   motogp.com 22 Nov. P8 seals it; level with Agostini.
9. TURIN — Alcaraz beats Zverev 6-2, 7-6, first ATP Finals title (CONFIRMED).
   BBC 22 Nov; Guardian 22 Nov.
10. LIVERPOOL — Liverpool 4-0 Man Utd (CONFIRMED). Reuters 22 Nov; Sky 22 Nov.
    Pochettino's debut; Yoro sent off 8'; Szoboszlai, Wirtz, Ngumoha, Munoz.
11. RABIGH — Houthis claim refinery hit (CLAIM). Reuters 22 Nov; ISW 22 Nov.
    Group claims a direct hit; Saudi has not confirmed; coalition intercepted
    a missile.
12. RAMALLAH — settlers torch 12 vehicles (CONFIRMED). AP 22 Nov; Euronews
    22 Nov. Homes also burned; Israel opens inquiry.
13. SHANGHAI — China cuts margin ratio to 80% (CONFIRMED). Reuters 22 Nov;
    Xinhua 22 Nov. Announced Sun 22 Nov, effective 30 Nov.
14. LAS VEGAS — Verstappen wins Las Vegas GP (CONFIRMED). FIA classification;
    Reuters round-up 22 Nov.

ALSO ON
15. KC Current win first NWSL title 2-1 (CONFIRMED). Al Jazeera 22 Nov;
    One Turn 22 Nov.
16. Gerwyn Price wins Grand Slam of Darts 16-11 (CONFIRMED). BBC 22 Nov;
    One Turn 22 Nov.
17. Thitikul wins LPGA finale, 3rd year running (CONFIRMED). BBC 22 Nov;
    One Turn 22 Nov.
18. UK set to host 2035 Women's World Cup (FORECAST). BBC 22 Nov; One Turn
    22 Nov. FIFA to confirm on Monday.
19. Boca Juniors win Copa Sudamericana 2-0 (CONFIRMED). One Turn 22 Nov;
    AppiSToS 22 Nov. First international trophy in 18 years.
20. POLAND — Russia tried twice to kill rapper Kyivstoner (CONFIRMED).
    AP 22 Nov (Polish MFA spokesman); Finwire 22 Nov. August attempt in
    Poland revealed on Sunday; Danish plot was Sept.
21. S. AFRICA — flags at half-mast for Mlambo-Ngcuka (CONFIRMED).
    SA Presidency via SA Health News 22 Nov; AP 22 Nov. Died Fri 20 Nov;
    state funeral 28 Nov; flags half-mast from Sun 22 Nov.
22. FINLAND — Russia towing drone-hit cargo ship (CONFIRMED). Euronews
    22 Nov; WSJ 22 Nov. Sparta II hit in the Baltic on Saturday.
23. NEW YORK — Skubal agrees $450M Mets deal (REPORTED). Reuters 22 Nov;
    CNN 22 Nov. Record for a pitcher; $50M/yr; pending a physical.
24. HULL — McBurnie double earns Hull win over Brighton (CONFIRMED).
    BBC 22 Nov; The Times 22 Nov.

## Dropped / not used
- Argentina LNG approval — announced Fri 20 Nov (AFP 21 Nov), not 22 Nov.
- El Chapo Isidro captured — raid Fri 20 Nov, announced Sat 21 Nov.
- EU-Indonesia trade deal — signed Sat 21 Nov.
- Trump-Xi-Putin Shenzhen summit — 19-20 Nov.
- ICJ Myanmar verdict — delivered Fri 20 Nov.
- Nigeria funeral boat, 24 dead — capsized Fri 20 Nov.
- S&P 500 correction — Friday 20 Nov sell-off.

## Build status
- compose_poster.py + main.py written fresh in this session (scratch dir:
  the init-created entry dir's tool result failed an execution-risk check,
  so files were built in ~/workspace/makefun/news-image-20261122-v2-scratch/
  and must be copied into the beacon repo by the parent after Zaki's
  go-ahead — see parent report).
- Anchor (init, this session): makefun anchor
  4961185ce7cea754a15c8e1b8aac545cb0422ce7 round 34200391.
- entry.png: 1024x1024, target < 1 MiB; sha256 recorded after verification.
- FINAL VERIFICATION (23 Nov ~10:37 WIB): compose_poster.py run twice ->
  byte-identical, sha256
  f344a03f25fa5c89c303da862bac4e5db7e56c48c80bf25512ae01d9ae31e641,
  203,582 bytes (< 1 MiB). main.py copies entry.png with the same sha256.
  Visual inspection (3 rounds): masthead, BY FIELD bar, UTC timeline, 4
  illustrated leads, 10 grid cards, ALSO ON 15-24, WHERE IT HAPPENED,
  HOW SURE legend, DATE CHECK box, sources footer — all inside the canvas,
  no overlaps, no cut-off text. All 24 stories dated 22 Nov 2026.
- COMMIT: NOT DONE — no commit SHA exists. The init step's tool result was
  flagged (execution-risk), so no git commands were run in the entry dir and
  no files were copied into it. Files are complete in this scratch dir;
  the parent must ask Zaki whether to place them into the beacon repo and
  commit (see parent report for the exact question).
- Confidence on ALSO items 15-24 is carried by the number circle's colour
  (green CONFIRMED, amber REPORTED, red CLAIM, grey FORECAST) — the HOW SURE
  legend explains it. Leads and grid items carry a full text chip.
