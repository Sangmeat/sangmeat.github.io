# Bodil Poulsens strikkegalleri

En statisk GitHub Pages-side. Én produktmappe bliver til én række, og billederne i mappen vises som varianter. Ingen database eller frontend-framework.

## Billedstruktur

```text
billeder/
  profilbillede.png
  01 Stribede sweatre/
    01 Original.HEIC
  02 Fryd sweater/
    01 Original.HEIC
    02 Variant 1.HEIC
    03 Variant 2.HEIC
    04 Variant 3.jpeg
  03 Sweater med høj hals/
    01 Original.HEIC
  04 Hæklede trøjer/
    01 Flerfarvet cardigan.jpg
    02 Grøn trøje.jpg
  05 Slipover/
    01 Lys slipover.jpg
  06 Mønsterstrik/
    01 Blå med rosa mønster.jpg
    …
```

Overblikket under profilen dannes automatisk af produktmapper med billeder og linker til hver række.

Grupperne sorteres efter antal billeder, flest først. Ved samme antal bruges mappenavnenes rækkefølge. Mappenavn bliver produktnavn; filnavn bruges som tilgængelig billedbeskrivelse. Der vises ingen tekst under billederne. Tal i starten styrer billedernes indbyrdes rækkefølge og skjules på siden. Brug fx `04 Cardigan/01 Grøn.HEIC` til et nyt produkt. Hold ét produkt pr. mappe og læg billeder direkte i produktmappen. Tomme mapper og andre filtyper ignoreres.

JPEG, PNG, WebP og HEIC/HEIF understøttes. Bygningen konverterer til JPEG, retter orientering, begrænser størrelsen til 1600 px og fjerner metadata fra de publicerede billeder. Originalerne i `billeder/` bevares; i et offentligt GitHub-repo er originalerne også offentlige.

Navn og introtekst redigeres i `index.html`. Lorem Ipsum er foreløbig tekst. Design findes i `style.css`.

## Lokal visning

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest discover -s scripts -p 'test_*.py'
.venv/bin/python scripts/build.py
.venv/bin/python -m http.server 8000 --directory dist
```

Åbn http://localhost:8000. Kør bygningen igen efter ændringer.

## GitHub Pages

Vælg **Settings → Pages → Source → GitHub Actions**. Workflowet bygger og udgiver ved push til `main`. Se [GitHubs vejledning](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Uploadmappe og synkronisering fra fx OneDrive er bevidst ikke tilkoblet endnu. Strukturen er klar; i den nuværende version skal billeder være i repoets `billeder/`, før siden bygges.
