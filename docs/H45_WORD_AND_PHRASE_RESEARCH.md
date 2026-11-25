# H45 Word, Phrasal Verb, Idiom, Polysemy & Error-Mining Research

Autonomous error mining across all 325 unique tokens in locked Videos A & B ([h45_error_mining_report.json](file:///d:/sign%20interpretor/artifacts/h45/h45_error_mining_report.json)) exposed 133 non-exact lexicon compressions where playable signs masked wrong meanings. Key verified repairs in [EnglishToISLTranslator.js](file:///d:/sign%20interpretor/tools/avatar_viewer/EnglishToISLTranslator.js) and [SemanticUnderstandingEngine.js](file:///d:/sign%20interpretor/tools/avatar_viewer/SemanticUnderstandingEngine.js):

| Token / MWE | Segments | Prior Wrong-But-Playable Bug | H45 Research-Grounded Fix |
| :--- | :--- | :--- | :--- |
| `probably` | `B04`, `B31` | `THINK` (wrong cognitive verb) | **`MAYBE`** (existing `maybe.json`, epistemic possibility) |
| `view` | `A28` | `SEE` (`THIS MY SEE YOU`) | **`PERSPECTIVE`** (existing `perspective.json` in nominal frames) |
| `talks` | `A12` | `SAY` (`MY FS_TEDX SAY`) | **`SPEECH`** (existing `speech.json` in nominal frames) |
| `delivered` | `A06`, `B27` | `GIVE` (object transfer) | **`PRESENTATION`** (`A06` live talk) / **`SHOW`** (`B27` feeling) |
| `what's going on` | `B31` | `WHAT GO` (physical locomotion) | **`WHAT HAPPEN`** (existing `happen.json`); `"day is going on"` -> `CONTINUE` |
| `still` / `always` | `B03`, `B05`, `B11`, `B28` | `CONTINUOUS` | **`STILL`** / **`ALWAYS`** (ISLRTC distinct discourse signs) |
| `something` / `things` | `B03`, `B07`, `B26`, `B27` | `ONE` / `MATTER` | **`SOMETHING`** / **`THING`** |
| `some` / `everybody` / `our` / `again` | `A06`, `B12`, `B13`, `B22`, `B24`, `B30` | `FEW` / `PEOPLE` / `WE` / `MORE` | **`SOME`** / **`EVERYONE`** / **`OUR`** / **`AGAIN`** |
| `gotten easier` / `getting warmer` | `B06`, `ADV09` | `GET EASY` / `GET` | **`BECOME MORE EASY`** (inchoative + comparative) |
| `talk straight to` | `B31` | `CLEAR CAMERA` | **`DIRECT CAMERA`** (`direct.json`) |
| `documenting` | `B02` | `MOVIE YOUR LIFE` | **`RECORD YOUR LIFE`** |
| `do know` / `you do too` | `B13`, `B20`, `B21`, `B24` | Spurious lexical `DO` (`WORK`) | Emphatic `do` omitted + `NMM-EMPHATIC-NOD`; elliptical `do too` -> `KNOW` |
