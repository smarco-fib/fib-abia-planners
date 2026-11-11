# UPSTREAM

Pristine upstream sources. Downloaded 2026-11-10 from Jörg Hoffmann's official pages.

| Tarball | URL | SHA-256 |
|---|---|---|
| `FF-v2.3.tgz` | https://fai.cs.uni-saarland.de/hoffmann/ff/FF-v2.3.tgz | `3d80fa30bb64b14de3a5156e202fc764301efbbb777fe3b703e67139a6150c88` |
| `Metric-FF-v2.1.tgz` | https://fai.cs.uni-saarland.de/hoffmann/ff/Metric-FF-v2.1.tgz | `16bbbd755415638379cbced9c5869c9542f3d49a6475619089e088781705f212` |

Landing pages: https://fai.cs.uni-saarland.de/hoffmann/ff.html, https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html

## Licence

Both code bases: GNU GPL version 2 **or (at your option) any later version** (source headers, e.g. `src/ff/main.c`, `src/metric-ff/main.c`).
Copyright (C) 2001/2002 Albert Ludwigs University Freiburg, Institute of Computer Science. FF 2.3 additionally carries a JAIR "AS IS" disclaimer.
Files without a licence header: FF `*.l`, `*.y`, `makefile`, `README`; Metric-FF `makefile`. They are part of the same GPL distribution.

## Notes

- The Metric-FF-v2.1 tarball contains files dated January 2022 (`lex-*.l`, `scan-*.y`, `relax.c`): upstream refreshed the tarball after the 2012 release.
- FF-v2.3 `makefile` contains a 2016 change by rpg (`-ansi` → `-std=gnu99`).
- The extracted trees were committed verbatim in `src/ff/` and `src/metric-ff/` (commit "Import pristine upstream"). File modes as in the tarballs.

## Generated parsers

The flex/bison output is committed so that a normal build needs only CMake and a
C compiler: `src/{ff,metric-ff}/scan-fct_pddl.tab.c`, `scan-ops_pddl.tab.c`,
`lex.fct_pddl.c`, `lex.ops_pddl.c`. Regenerate with `tools/regen-parsers.sh`
(maintainers only).

| Tool | Version | Options |
|---|---|---|
| GNU Bison | 3.8.2 | `-pfct_pddl -bscan-fct_pddl`, `-pops_pddl -bscan-ops_pddl` (as upstream makefiles) |
| flex | 2.6.4 | `-Pfct_pddl`, `-Pops_pddl` (as upstream) plus `--nounistd --never-interactive` (PATCHES.md, P-GEN-1) |

Both grammars report one shift/reduce conflict each, as upstream.

## Per-file SHA-256 (pristine)

Checksums of the pristine import (commit `a9e3d7c`). Files changed since then
are listed in `PATCHES.md`; currently `metric-ff/scan-fct_pddl.y` (UB-1) and
`metric-ff/parse.c` (UB-2). Verify with `git diff a9e3d7c -- src/`.

```
d0f794292d80588d7211b8a3f71479ff3b80642cd84b941717fbd591f0e0628b  ff/ff.h
e484ffee20fa54b6466c4a7ea3ace1c1bb5b198c54a27e9d8bd543d05938545a  ff/inst_easy.c
db456e0cae7c47e523157d367a5035f995e95aa5d0d136bc72918d62d1cb5d74  ff/inst_easy.h
f2f56b51759114e6d2adfdac4115d025eb0990759b0b8bf4f4aef6f156a0b7ac  ff/inst_final.c
6b911b6be0018cf20065f385818346f664b8f0e34ee981e3ae70b0bc3d378a54  ff/inst_final.h
2eef106d1b983292c42ffbaf2b1d69a1061a0d5affc86f8fd906febf17def779  ff/inst_hard.c
dc644ed600b8fbe060e9776a2df9c156a01a10ce3e6d430ee0f5e42ac361fbec  ff/inst_hard.h
e0abb8dbb885be6a8f3f60732f5bbaeccb5b6858d1f968d84eb4eb79e6592b79  ff/inst_pre.c
cc1cfbd0dc508b7d78aff95a9c9cfeef76c17a9e94ea66cbc7c0d33ad5f62e4b  ff/inst_pre.h
2af28e7323719d4bac0d16e5bec48df64ab75a5df3dc2f7a131c5d74bb945ab6  ff/lex-fct_pddl.l
93b0dcdf7cae1384e0f4a94714280083bcee193994a65521efe4ef1904827830  ff/lex-ops_pddl.l
740cc6f0613452ecff5c5b73e5dbadc7f14eea442a65bf5fb5ae2deda97ad02d  ff/main.c
57cdb82c945f251ce38a79e4c19f4ab3d47d744570044c2cab9c499b407ba5f0  ff/makefile
8a3bdde2e65581d57fe778a4ce0e138244b14909575cc46cb69842606dda1f67  ff/memory.c
d5370e2ad34f32c9505d9486e4f69f8bc3f00a38c1a9f91b71de2922b4503db3  ff/memory.h
2105821427033fc4b6c007e1b3d4fafc390ae66426b3d3bbd4ab94fad17564b3  ff/orderings.c
c85b8d83ee0162ab1a591ab6d675d5dc00dda79e689ee061ba94db9e1d7efa2c  ff/orderings.h
3aa51a96b8594921ca95aabf075f5fabc109a24d66bf48c988e8b7387bed83a4  ff/output.c
24c0b09c9453dcbb2dce4a0ed50d1d4180f13d059380f7283fc157c05012c732  ff/output.h
5bb05b7ed1e02bd1b6773e0fac2f50247e74e93bce9dcf0e06e0a027f922f060  ff/parse.c
062681c7d889bce8995a11b7d486bbe4a9e00745307fa892049babb1c91a40ca  ff/parse.h
811bcb2b6487eab7771a4f71a343f6361c77ae1864095ec16b524665087cc19e  ff/README
106120708b22eb1b2800265c699f718876faaed8c2de6db55bce3a6a7a979340  ff/relax.c
3bedd924d19ff15b527a41d1050b7e834530e471f16b5b0f68eafb6cc123ccfe  ff/relax.h
b4ebb12bc423afafade8bbe4cf7cfb5cefbe1bae6685b33ffb61d5fec00d8e01  ff/scan-fct_pddl.y
be459b7f1c9b54d191eda28f4e640e6d1d0f5e1a80bccb3c36548e55d67add30  ff/scan-ops_pddl.y
6024a4c3d4863b39ada551ae438c3dff89471b4e7f474f60f5893fb04cd9327f  ff/search.c
d75cf5670a8182a2d8661deda2fc7d2fc980561270c3f0847a83b1ddaf8b7abc  ff/search.h
1bb78c7ff43cd82f55b3844f75384ddaa428ff8bc4d63be0767cd19bc5058a1c  metric-ff/expressions.c
a97827facb1584cf2066c0efa229c148f8e61fe338168e58dd7114ad0a77b664  metric-ff/expressions.h
9f2ed55eb8faf117d28280b2ae7be774fbc68c59bf2fc0af9480f39d1a7bf940  metric-ff/ff.h
c685bc50813fbf75f421ed181b65f42a0bb817769a20914674ce7634a66bf0c1  metric-ff/inst_easy.c
a2c6d834895ce80d91057b641c5293da12debaac43a1db29e400f39dc4888a37  metric-ff/inst_easy.h
c2955736aea04b24ceedc2006e00b8bac6195b096f40586cef093be31d20bcb6  metric-ff/inst_final.c
a7de43c5c35fb32b9fa2ab3a07dc76cce3bf3cd36c9edcff8379652385f2f447  metric-ff/inst_final.h
aeb06450bd08d5df9dd3534f5a76919162a54b4e502190653c4dcb505ab1ed47  metric-ff/inst_hard.c
4ab88a1da6bf3d7e43b4d1005b6b072e9a07e73a0d628143f288051e6389391e  metric-ff/inst_hard.h
98ff48e87e70afb7a5862be35df46726fbd19bc51241d2e5befbb8a1ebe80b57  metric-ff/inst_pre.c
25927b2e8685f0a06ac0b162c2308637b5b9b8a978bd7db260170998c423bdad  metric-ff/inst_pre.h
8840986c41f12cf5be652a985328896bc6ddf1b233a5d8de78dbab828aa580a4  metric-ff/lex-fct_pddl.l
c8f169d51ad6fdde84a47fb699d5b55744f5333f7eea332b708cb6a1c864b69b  metric-ff/lex-ops_pddl.l
44f60cd4bef9e87fedf7f0e87848df028fab85b757887ef4e7136a8ddcb6963e  metric-ff/main.c
50a71fe32b2418acfb74bd18c96bab33f44a3e1c106325cf107827f7e07aa2a3  metric-ff/makefile
beed429a781337a08d4a8bd648d951ef1f5a7bbec334e827c692d308c8a49bb3  metric-ff/memory.c
9d08f8c07bdd1533690fa5aabf1380da355a3c598c83847bb8b75e4509722d4a  metric-ff/memory.h
75699bfa4f3b8c7265db86a584077db26ee9c8675da9906fe8adaa6e5ec73eb4  metric-ff/output.c
8e8e35098bd383586d3f749bb0260dbb1ddd00a6f06a18d79ab79f53844e8bd3  metric-ff/output.h
57688ce7c9f0391bb01eab4bf8801fe4ab6215f4c76d7d5e6dba64fd004ffac7  metric-ff/parse.c
2f4c3c0b635deda5c4b7278fdfd34535c6fdc1a305dcdcc894bec27650f655f1  metric-ff/parse.h
44652cd7a0d5cea341c2fb99cccfae1651dd7f5d6e14b2533a5e9b4d9f9f98ef  metric-ff/relax.c
6daf941247008e606f58153971c003fe7bc090a3bc6108b0049ffe7682316e4a  metric-ff/relax.h
e442cd29e517023ebbdc0f9ba18af1bc67653bd0ad7f191f2aba3d980e716e57  metric-ff/scan-fct_pddl.y
912529583889a4b018f4af92129efc88865d0bc783ed9796e372f51c1a36ae60  metric-ff/scan-ops_pddl.y
b26f6ffd4635b3a4000eeb969dce658fb73f0db06d7a568bef63ec529ad67de8  metric-ff/search.c
3afff2be08d179ea12b2caf2079c92ff9a2c2ef281a48b9cd523e4c5cc06e121  metric-ff/search.h
```
