#!/usr/bin/env python3
"""Тики второго класса: однообразие хорошего приёма.

Ловит не ошибку, а превышение потолка. Каждая находка по отдельности
законна; блокирует их количество.

    python3 tics.py <файл.docx|txt> [--list]
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import text as T

# ось: (норма, описание)
NORMS = {
    'said_this': (4, '«сказал это» + оценка'),
    'like_general': (4, 'сравнение «как + делают вообще»'),
    'without_noun': (6, '«без + отвлечённое сущ.»'),
    'earlier_than': (3, '«раньше / прежде, чем»'),
    'and_it_was': (2, '«и это было / означало»'),
    'pointe': (14, 'афоризм-пуант'),
    'triad': (10, 'триада «факт. факт. вывод.»'),
}
SHORT_REPLICA_MAX = 0.45   # доля реплик <= 3 слов

# Равномерность считается ТОЛЬКО по дефектным осям и ТОЛЬКО как перегрев
# густой трети. Прежняя версия делила густую треть на пустую и потому
# ругалась на вычищенную треть: у Глава_02_wip первая треть дала 0 находок
# и отношение ушло в бесконечность. Дефект — сгущение, а не чистота.
# Плотность нормируется на абзацы наррации: в диалоговой сцене абзацев
# наррации меньше, и абсолютный счёт занижен не по делу.
THIRDS_KEYS = ('said_this', 'like_general', 'without_noun',
               'earlier_than', 'and_it_was')
THIRDS_HOT = 2.2           # во сколько раз густая треть гуще средней по главе
THIRDS_MIN_N = 12          # ниже этого числа находок треть не считаем

RE_SAID_THIS = re.compile(
    r'\b(сказал|сказала|произнёс|произнесла|проговорил|проговорила|'
    r'ответил|ответила|бросил|бросила)\s+(это|её|его|этот)\b', re.I)
RE_SAID_THIS2 = re.compile(
    r'\b(сказано|сказал|сказала)\b[^.!?]{0,40}\b(без|тем же|таким|как\s+говорят)\b', re.I)

RE_LIKE_GENERAL = re.compile(
    r'\bкак\s+(?:это\s+)?'
    r'(?:делают|говорят|смотрят|стоят|ходят|читают|пишут|берут|кладут|'
    r'отвечают|спрашивают|прощаются|здороваются|считают|носят|'
    r'бывает|принято|положено|разговаривают|улыбаются|молчат|'
    r'подравнивают|отсчитывают|записывают|провожают)\b', re.I)

# «без + отвлечённое существительное» как способ описать манеру.
# Предметное «без цепи», «без перца», «без рекомендации» — не тик.
_ABSTRACT = (
    r'(?:выражени\w+|удовольстви\w+|весель\w+|смущени\w+|нажим\w*|интерес\w*|'
    r'злоб\w+|злост\w+|усили\w+|спешк\w+|труд\w*|сомнени\w+|страх\w*|жалост\w+|'
    r'тепл\w+|охот\w+|вызов\w*|упрёк\w*|пауз\w+|предислови\w+|запинк\w+|'
    r'заминк\w+|нежност\w+|раздражени\w+|насмешк\w+|ирони\w+|надежд\w+|'
    r'намерени\w+|толк\w*|тишин\w+|звук\w*|шум\w*|слов)')
RE_WITHOUT_NOUN = re.compile(
    r'\bбез\s+(?:всяк\w+\s+\w+|особ\w+\s+\w+|' + _ABSTRACT + r')', re.I)

RE_EARLIER = re.compile(r'\bраньше,\s*чем\b|\bпрежде,\s*чем\b', re.I)
RE_AND_IT_WAS = re.compile(
    r'(^|[.!?…»]\s+|,\s+)и\s+это\s+(было|значило|означало|оказалось)\b', re.I)

# глагол в прош. вр.: любое слово на -л/-ла/-ло/-ли, кроме связок и омонимов
RE_PAST = re.compile(r'\b([а-яё]{3,}?(?:л|ла|ло|ли))(?:сь|ся)?\b', re.I)
_LINK = {'был', 'была', 'было', 'были', 'стал', 'стала', 'стало', 'стали',
         'значил', 'значила', 'значило', 'значили'}
_NOUN_L = {'стол', 'угол', 'пол', 'узел', 'котёл', 'мел', 'орёл', 'факел',
           'вол', 'ствол', 'козёл', 'осёл', 'сокол', 'пепел', 'уголь'}


def _has_action(par):
    for m in RE_PAST.finditer(par):
        w = m.group(1).lower()
        if w in _LINK or w in _NOUN_L:
            continue
        return True
    return False


def _pointe(paras, i):
    """Абзац-приговор: короткая сентенция, вынесенная отдельной строкой.

    1-2 предложения, <=12 слов, не реплика, без глагола действия.
    Исключения: строка с тире (это графа перечня, а не пуант) и абзац
    сразу после такого же короткого (это серия, а не отдельный удар).
    """
    par = paras[i]
    if T.is_replica(par):
        return False
    n = T.wc(par)
    if not (3 <= n <= 12):
        return False
    if len(T.sentences(par)) > 2:
        return False
    if _has_action(par):
        return False
    if re.search(r'\s' + T.DASH + r'\s', par):
        return False
    if i > 0 and T.wc(paras[i - 1]) <= 12:
        return False
    return True


def _triad(par):
    """Три предложения, последнее короче и обобщает."""
    if T.is_replica(par):
        return False
    ss = T.sentences(par)
    if len(ss) != 3:
        return False
    a, b, c = (T.wc(x) for x in ss)
    return c <= a and c <= b and c <= 9 and a >= 4 and b >= 4


def scan(paras):
    hits = {k: [] for k in NORMS}
    for i, p in enumerate(paras, 1):
        if RE_SAID_THIS.search(p) or RE_SAID_THIS2.search(p):
            hits['said_this'].append((i, p))
        if RE_LIKE_GENERAL.search(p):
            hits['like_general'].append((i, p))
        if RE_WITHOUT_NOUN.search(p):
            hits['without_noun'].append((i, p))
        if RE_EARLIER.search(p):
            hits['earlier_than'].append((i, p))
        if RE_AND_IT_WAS.search(p):
            hits['and_it_was'].append((i, p))
        if _pointe(paras, i - 1):
            hits['pointe'].append((i, p))
        if _triad(p):
            hits['triad'].append((i, p))
    return hits


def short_replicas(paras):
    bodies = [T.replica_body(p) for p in paras if T.is_replica(p)]
    if not bodies:
        return 0, 0.0
    short = sum(1 for b in bodies if T.wc(b) <= 3)
    return len(bodies), short / len(bodies)


def thirds(hits, total, keys=None):
    """Распределение находок по третям главы.

    keys=None — все оси (для отчёта); THIRDS_KEYS — только дефектные.
    """
    if not total:
        return (0, 0, 0)
    b = [0, 0, 0]
    for k in (keys if keys is not None else hits):
        for i, _ in hits[k]:
            b[min(2, (i - 1) * 3 // total)] += 1
    return tuple(b)


def narration_thirds(paras):
    """Абзацы наррации по третям — знаменатель для плотности."""
    n = len(paras)
    b = [0, 0, 0]
    for i, p in enumerate(paras, start=1):
        if not T.is_replica(p):
            b[min(2, (i - 1) * 3 // n)] += 1
    return b


def hot_third(paras, hits):
    """(находки, во сколько раз густая треть гуще средней по главе).

    Односторонняя проверка: ловит сгущение дефектов, не чистоту.
    """
    n = len(paras)
    b = thirds(hits, n, THIRDS_KEYS)
    nar = narration_thirds(paras)
    avg = sum(b) / max(sum(nar), 1)
    if not avg:
        return b, 0.0
    dens = [b[k] / max(nar[k], 1) for k in range(3)]
    return b, max(dens) / avg


def report(path, show=False):
    paras = T.load(path)
    hits = scan(paras)
    print('\n=== %s (%d абз.) ===' % (os.path.basename(path), len(paras)))
    print('%-34s %-8s %s' % ('ось', 'норма', 'факт'))
    bad = 0
    for k, (limit, label) in NORMS.items():
        n = len(hits[k])
        flag = 'ok' if n <= limit else 'БЛОКЕР'
        if n > limit:
            bad += 1
        print('%-34s <= %-5d %d %s' % (label, limit, n, flag))
    tot, frac = short_replicas(paras)
    flag = 'ok' if frac <= SHORT_REPLICA_MAX else 'БЛОКЕР'
    if frac > SHORT_REPLICA_MAX:
        bad += 1
    print('%-34s <= %-5s %.0f%% (%d реплик) %s'
          % ('реплик <= 3 слов', '%.0f%%' % (SHORT_REPLICA_MAX * 100),
             frac * 100, tot, flag))
    t, hot = hot_third(paras, hits)
    if sum(t) < THIRDS_MIN_N:
        flag = 'ok (мало находок)'
    elif hot > THIRDS_HOT:
        flag = 'сгущение'
        bad += 1
    else:
        flag = 'ok'
    print('%-34s <= %-5.1f %d / %d / %d  x%.1f %s'
          % ('дефекты в одной трети', THIRDS_HOT, t[0], t[1], t[2], hot, flag))

    if show:
        for k, (limit, label) in NORMS.items():
            if hits[k]:
                print('\n-- %s (%d)' % (label, len(hits[k])))
                for i, p in hits[k]:
                    print('  %4d  %s' % (i, p[:150]))
    return bad


if __name__ == '__main__':
    rc = 0
    for p in T.argv_paths():
        rc += report(p, T.verbose())
    sys.exit(1 if rc else 0)
