# Иллюстрации к «Осколкам Бездны» — промпты для ручной генерации

Стиль серии: **«листы картографа»** — сепия-тушь, гравюрный штрих, полевые таблицы
натуралиста XIX века. Предметы и места. Лиц внутри сцен нет (фигуры — только со
спины или силуэтом). Единственный цветовой акцент всей серии — красная нить на
свёртке (В5).

Пробы, которые получились у меня, лежат вне репозитория (папка
`illustrations_archive` в рабочей области) — можно использовать как референсы,
но генератор тянет качество посредственно, так что они скорее черновики.

---

## Общие правила

### Базовый стилевой блок — добавлять в начало КАЖДОГО промпта, не меняя

```
Antique book illustration on aged cream paper, sepia ink, fine copperplate
engraving crosshatching, 19th-century naturalist expedition sketchbook,
cartographer's field plate aesthetic, muted brown-ochre monochrome, soft
uneven plate edges, wide margins, no text, no letters, no numbers, no watermark
```

Единообразие серии держится именно на неизменном базовом блоке и одинаковых
пропорциях кадра — не меняй их между картинками одной главы.

### Негатив-промпт (если генератор поддерживает)

```
color, photorealism, 3d render, cartoon, anime, modern objects, faces,
close-up portrait, text, letters, watermark
```

### Пропорции

- Таблички (панорамы, «полные пластины»): **3:2 горизонталь**.
- Виньетки (предметные, мягко растворяются в полях): **3:2 или квадрат**,
  добавляй в промпт `vignette composition fading into blank paper`.
- Карта: **3:2**.

### Про текст внутри картинок

Генераторы путают буквы. Надёжнее просить `no text, no letters, no numbers`
и добавлять начерно:
- цифры «2-14» на двери (В6) — потом вписать шрифтом (у меня прочитались,
  но это лотерея);
- подписи на карте — потом наложить кириллическим шрифтом самому;
- этикетки на банках в Т2 — попросить `blank labels`, иначе будет псевдо-вязь
  (выглядит, впрочем, терпимо).

---

## Глава 1 — список и места вставок

Номера абзацев — от начала главы, в тексте, где каждая виньетка ложится по смыслу.

### Т1. Порт днём — панорама с лестницы
**Место:** после первого подъёма Кайра, когда город впервые открывается весь (~абз. 196).

```
[БАЗОВЫЙ БЛОК], panoramic view of a small northern harbor town seen from the
top of a long stone staircase climbing a steep cliff: fishermen's rooftops
below, nine wooden piers jutting into a calm bay, sailing ships and rowing
boats, a ribbed wooden skeleton of an unfinished ship on a slipway near the
middle piers, a lighthouse on a rocky islet, gulls, distant hills, one lonely
figure in a headscarf on the steps seen from behind, face not visible, soft
morning light
```

Замечание: каркас недостроенного корабля («парус»-остов) в моей пробе не
прочитался — если он важен, усиль это место промпта; если мешает — убери клаузу.

### Т2. Ладонь над горлышком — весовая
**Место:** после сцены у весовой, где «…муть, которая через минуту сядет на дно» (~абз. 671).

```
[БАЗОВЫЙ БЛОК], interior of a harbor weigher's and herbalist's stall: wooden
counter, brass balance scales, glass flask with murky sediment at the bottom,
mortar and pestle, scattered dry herbs and splashes on the boards, shelves of
glass jars and bottles with blank labels behind; one hand in a worn jacket
sleeve held flat over the mouth of the flask, no people beyond the hand
```

### В1. Заставка главы — натюрморт новобранца
**Место:** под заголовком главы (~абз. 81).

```
[БАЗОВЫЙ БЛОК], still life on a rough wooden table in a tiny rented room:
a wax writing tablet, a short pencil, an open tin box with two stacks of coins
(three large silver coins in one, twelve small copper in the other), a coiled
worn leather belt with a brass buckle, a candle stub in a tin candlestick,
a narrow cot and a small window in the background, quiet morning
```

Замечание: количество монет (3 и 12) генератор, скорее всего, не выдержит —
если точность не нужна, убери числа.

### В2. Ниша с зелёным камнем
**Место:** первый уличный маршрут Кайра (~абз. 127).

```
[БАЗОВЫЙ БЛОК], a small stone shrine recessed into a rough masonry street
wall: at the back a dark green polished stone slab carved with a single
stylized wave, a low copper bowl with a few coins on the stone shelf, an empty
wrought-iron bracket above, cobblestones below, vignette composition fading
into blank paper
```

Замечание: можно дать плите еле живой зеленоватый тон (`a faint hint of green
on the stone, everything else strictly sepia`) — но тогда это будет второе
цветное пятно серии после красной нити. На твой вкус.

### В3. Рыбина
**Место:** сцена у Мизу (~абз. 463).

```
[БАЗОВЫЙ БЛОК], interior corner of a fisherman's hut: a large prized dried
fish hanging by a rope loop from a nail on a dark plank wall, wooden shelves
with clay pots, a kettle, cups, a bundle of dried herbs, a wicker basket and
a sack on the floor, vignette composition fading into blank paper
```

### В4. Канатный двор
**Место:** встреча/эпизод у канатного двора (~абз. 165).

```
[БАЗОВЫЙ БЛОК], a rope-maker's yard behind a wooden gate in an old northern
town: coils of rope hanging under a lean-to shed, rope stretched on a wooden
sawhorse, mallets on a chopping block, a broad oak beam leaning beside the
gate post, cobblestones, stone houses behind; a shaggy dog sitting small by
a chain post, seen from behind, silhouette only
```

### В5. Свёрток с красной нитью
**Место:** перед «Идти было дольше…» (~абз. 722).

```
[БАЗОВЫЙ БЛОК], a small parcel wrapped in plain paper tied with a RED thread
in a neat bow, lying on a worn wooden table, a small corked glass vial beside
it, the red thread is the only colored element in the strictly sepia drawing,
vignette composition fading into blank paper
```

Замечание: если генератор разольёт красное за пределы нити — перегенерируй
с `everything else strictly sepia monochrome, only the thread is red`.

### В6. Дверь 2-14 — концовка главы
**Место:** финал главы (~абз. 806).

```
[БАЗОВЫЙ БЛОК], a dim boarding-house corridor, oval vignette: an old dark
wooden door with a blank brass number plate, a thin warm line of light under
the door, worn floorboards; an open notebook in the foreground covered in
unreadable scribbled shorthand with one clean horizontal stroke, everything
else in darkness
```

Замечание: я просил настоящие «2-14» — прочиталось, но это везение. Надёжнее
`blank brass number plate` и вписать цифры после. Письмо в тетради должно
остаться нечитаемой псевдо-вязью (`unreadable scribble`) — настоящий текст не нужен.

---

## Бонусные листы (задел, не в чистовой список)

### Лестница ночью (линия Агнис, ~абз. 584)

```
[БАЗОВЫЙ БЛОК], night scene on a very long switchback stone staircase hugging
a cliff above a dark northern harbor: a slight girl in a headscarf carrying
a knot-bundle climbing the steps, seen from behind at a distance, small
lanterns along the piers below, moored ships with lights, heavy dark sky,
quiet lonely mood
```

Замечание: в моей пробе внизу кадра сдвоился пролёт лестницы — смотри
геометрию ступеней при отборе.

### Белая ниша (та же линия Агнис)

```
[БАЗОВЫЙ БЛОК], a small whitewashed stone niche with a little pitched wooden
roof set into a cobbled street corner: inside on the shelf a rounded white
loaf-shaped white stone draped with a string of beads, a copper bowl with
coins, vignette composition fading into blank paper
```

Замечание: предметное наполнение ставил по памяти сцены — сверь с текстом
и поправь список предметов, если наврал.

### Карта города (форзац/конверт, к кириллическим подписям)

```
[БАЗОВЫЙ БЛОК], antique engraved bird's-eye map of a small northern port
town: a bay with nine wooden piers and ships, dense fishermen's quarter along
one main street climbing from the harbor, a long stone staircase up a steep
cliff to a walled house on the plateau, fields and scattered farms beyond,
a lighthouse on a point, a compass rose, a small engraved sea serpent in the
corner of the sea, no labels, no text
```

Замечания:
- Подписи (причалы, Ткацкая, Мучная, Бочарная и т. д.) наложить кириллицей после.
- Прежде чем делать чистовую карту, сверим географию с текстом (девять
  причалов, порядок третьего/четвёртого, где весовая, где «Ржавый якорь» и
  «Серебряная ложка») — отдельным разговором.

---

## Глава 2

Список составлю по тому же протоколу: места вставок → обсуждение → промпты.
Скажи «поехали» — соберу.
