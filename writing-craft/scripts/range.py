#!/usr/bin/env python3
"""Квоты на разнообразие: то, чего в главе должно БЫТЬ.

Все прочие детекторы ищут превышение. Этот ищет недобор — то есть
сужение палитры, из-за которого текст, безупречный в каждой строке,
читается ровно и не запоминается.

    python3 range.py <файл.docx|txt> [--list]
"""
import re
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import text as T

# --- регистры подачи -------------------------------------------------------
RE_INDIRECT = re.compile(
    r'\b(сказал[а]?|ответил[а]?|спросил[а]?|говорил[а]?|объяснил[а]?|'
    r'заметил[а]?|велел[а]?|обещал[а]?|призналс[яь]|пожаловалс[яь])\b'
    r'[^.!?]{0,30}\bчто\b|\bспросил[а]?\b[^.!?]{0,20}\bне\s|\bсказал[а]?\b'
    r'[^.!?]{0,20}\bчтобы\b', re.I)

RE_SUMMARY = re.compile(
    r'\b(обычно|каждый\s+(?:день|раз|вечер|год)|по\s+утрам|всю\s+зиму|'
    r'весь\s+день|годами|каждую\s+декаду|раз\s+в\s+год|с\s+тех\s+пор|'
    r'до\s+сих\s+пор|всегда|никогда\s+не|второй\s+год|третий\s+год)\b', re.I)

RE_COUNT_POV = re.compile(
    r'\b(я\s+(?:по)?считала|я\s+насчитала|я\s+отмерила|шагов|ступен|'
    r'я\s+знала,?\s+что|я\s+прикинула|в\s+уме|сажен)\b', re.I)

# --- обязательные элементы -------------------------------------------------
RE_ELLIPSIS = re.compile(r'\.\.\.|…')

RE_ENV_BODY = re.compile(
    r'\b(пахло|запах|холод|жар|тепло|сыро|мокр|дуло|ветер|сквозняк|'
    r'ладон|пальц|плеч|шея|спина|колен|горло|в\s+груди|под\s+ворот|'
    r'озябл|окоченел|обожгл|скольз)\w*', re.I)

RE_POV_DOUBT = re.compile(
    r'\b(кажется|казалось|наверное|может\s+быть|может,|возможно|'
    r'я\s+не\s+знала|я\s+не\s+поняла|или\s+просто|а\s+может|'
    r'мне\s+показалось|я\s+так\s+и\s+не|плохо\s+читала|'
    r'не\s+могу\s+сказать|не\s+бралась\s+судить)\b', re.I)

RE_FAILED_ACTION = re.compile(
    r'\b(попыталась|попытался|не\s+получилось|не\s+вышло|со\s+второго\s+раза|'
    r'сорвал\w*|соскольз\w*|промахн\w*|уронил\w*|не\s+сразу|'
    r'пришлось\s+(?:пере|за)\w+|сломал\w*|заело|не\s+поддал\w*)\b', re.I)

# нормы начал абзацев: посчитаны по принятому тексту (топ-3 = 30-31%,
# набегание не больше 3 подряд); превышение = ритм наррации осел на шаблон
HEAD_TOP3_MAX = 0.34
HEAD_RUN_MAX = 3

QUOTAS = [
    ('реплики 40+ слов',        3,  None),
    ('многоточие-обрыв',        3,  RE_ELLIPSIS),
    ('среда входит в тело',     6,  RE_ENV_BODY),
    ('POV не ручается',         4,  RE_POV_DOUBT),
    ('действие не удалось',     2,  RE_FAILED_ACTION),
]


def registers(paras):
    """Сколько абзацев в каждом из четырёх регистров подачи."""
    r = Counter()
    for p in paras:
        if T.is_replica(p):
            r['прямая речь'] += 1
        elif RE_INDIRECT.search(p):
            r['косвенная речь'] += 1
        elif RE_SUMMARY.search(p):
            r['сводка-пересказ'] += 1
        elif RE_COUNT_POV.search(p):
            r['внутренний счёт'] += 1
    return r


def opening_variety(paras):
    """Чем начинаются абзацы наррации.

    Доля «я» здесь не показатель: в POV от первого лица она 18-19% и в
    принятом тексте, и в черновике. Дефект — не частота слова вообще,
    а НАБЕГАНИЕ: несколько абзацев подряд с одного и того же слова.
    """
    heads = Counter()
    seq = []
    for p in paras:
        if T.is_replica(p):
            continue
        w = T.words(p)
        if w:
            heads[w[0].lower()] += 1
            seq.append(w[0].lower())
    return heads, seq


def longest_head_run(seq):
    best = cur = 1 if seq else 0
    for i in range(1, len(seq)):
        cur = cur + 1 if seq[i] == seq[i - 1] else 1
        best = max(best, cur)
    return best


def scene_lengths(paras):
    return [len(s) for s in T.scenes(paras)]


def report(path, show=False):
    paras = T.load(path)
    n = len(paras)
    print('\n=== %s (%d абз.) ===' % (os.path.basename(path), n))

    print('\n-- регистры подачи (нужны все четыре)')
    reg = registers(paras)
    for name in ('прямая речь', 'косвенная речь', 'сводка-пересказ', 'внутренний счёт'):
        c = reg.get(name, 0)
        print('  %-18s %4d  %s' % (name, c, 'ok' if c else 'НЕТ ВОВСЕ'))

    print('\n-- квоты (минимум на главу)')
    bad = 0
    for label, need, rx in QUOTAS:
        if rx is None:
            c = sum(1 for p in paras
                    if T.is_replica(p) and T.wc(T.replica_body(p)) >= 40)
        else:
            c = sum(1 for p in paras if rx.search(p))
        ok = c >= need
        if not ok:
            bad += 1
        print('  %-24s >= %-3d %4d  %s' % (label, need, c, 'ok' if ok else 'НЕДОБОР'))

    print('\n-- начала абзацев наррации')
    heads, seq = opening_variety(paras)
    top = heads.most_common(5)
    tot = sum(heads.values()) or 1
    for w, c in top:
        print('  %-14s %3d  (%.0f%%)' % (w, c, 100 * c / tot))
    top3 = sum(c for _, c in heads.most_common(3)) / tot
    run = longest_head_run(seq)
    ok3 = top3 <= HEAD_TOP3_MAX
    okr = run <= HEAD_RUN_MAX
    print('  %-24s <= %-3.0f%% %3.0f%%  %s'
          % ('доля трёх верхних', HEAD_TOP3_MAX * 100, top3 * 100,
             'ok' if ok3 else 'ОДНООБРАЗНО'))
    print('  %-24s <= %-3d %4d  %s'
          % ('подряд с одного слова', HEAD_RUN_MAX, run,
             'ok' if okr else 'НАБЕГАНИЕ'))
    if not ok3:
        bad += 1
    if not okr:
        bad += 1

    sl = scene_lengths(paras)
    if len(sl) > 1:
        print('\n-- сцены: %d, абзацев %s' % (len(sl), ' / '.join(map(str, sl))))
        if len(set(sl)) > 1 and max(sl) <= 1.5 * min(sl):
            print('  сцены одного размера — проверить, не идут ли все по одной схеме')

    if show:
        print('\n-- реплики 40+ слов')
        for i, p in enumerate(paras, 1):
            if T.is_replica(p) and T.wc(T.replica_body(p)) >= 40:
                print('  %4d (%d) %s' % (i, T.wc(T.replica_body(p)), p[:120]))
    return bad


if __name__ == '__main__':
    rc = 0
    for p in T.argv_paths():
        rc += report(p, T.verbose())
    sys.exit(1 if rc else 0)
