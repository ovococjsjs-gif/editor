#!/usr/bin/env python3
"""Лесенка: диалог, рассыпавшийся в лестницу коротких обменов.

Серия — 4+ подряд идущих реплик, где средняя длина тела <= 9 слов
и не меньше 60% реплик короче 12 слов.

    python3 ladder.py <файл.docx|txt> [--list]
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import text as T

MIN_RUN = 4
AVG_MAX = 9
SHORT_W = 12
SHORT_FRAC = 0.6

SERIES_MAX = 6        # норма длины серии
SERIES_BLOCK = 8      # блокер
FRAC_MAX = 0.40       # доля реплик внутри лесенок
FRAC_BLOCK = 0.50
LONG_REPLICA = 40     # реплик такой длины нужно >= 3 на главу
LONG_MIN = 3


def runs(paras):
    """Непрерывные серии реплик (индексы 1-based).

    Любой абзац наррации серию рвёт: абзац между репликами и есть то,
    чем автор ломает лесенку. Нормы SERIES_MAX/FRAC_MAX посчитаны
    по принятому тексту именно при таком строгом счёте.
    """
    out, cur = [], []
    for p_i, p in enumerate(paras, 1):
        if T.is_replica(p):
            cur.append((p_i, T.replica_body(p)))
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def ladders(paras):
    res = []
    for run in runs(paras):
        if len(run) < MIN_RUN:
            continue
        lens = [T.wc(b) for _, b in run]
        avg = sum(lens) / len(lens)
        frac = sum(1 for x in lens if x < SHORT_W) / len(lens)
        if avg <= AVG_MAX and frac >= SHORT_FRAC:
            res.append(run)
    return res


def report(path, show=False):
    paras = T.load(path)
    total = sum(1 for p in paras if T.is_replica(p))
    lads = ladders(paras)
    inside = sum(len(x) for x in lads)
    frac = inside / total if total else 0
    longest = max((len(x) for x in lads), default=0)
    long_replicas = [
        (i, p) for i, p in enumerate(paras, 1)
        if T.is_replica(p) and T.wc(T.replica_body(p)) >= LONG_REPLICA]

    print('\n=== %s ===' % os.path.basename(path))
    print('реплик всего            %d' % total)
    print('лесенок                 %d' % len(lads))
    print('реплик внутри лесенок   %d (%.0f%%)  норма <=40%%  %s'
          % (inside, frac * 100,
             'ok' if frac <= FRAC_MAX else
             ('превышение' if frac <= FRAC_BLOCK else 'БЛОКЕР')))
    print('самая длинная серия     %d  норма <=%d  %s'
          % (longest, SERIES_MAX,
             'ok' if longest <= SERIES_MAX else
             ('превышение' if longest <= SERIES_BLOCK else 'БЛОКЕР')))
    print('реплик по %d+ слов       %d  норма >=%d  %s'
          % (LONG_REPLICA, len(long_replicas), LONG_MIN,
             'ok' if len(long_replicas) >= LONG_MIN else 'НЕДОБОР'))

    if show:
        for run in lads:
            print('\n-- серия %d реплик, абз. %d-%d'
                  % (len(run), run[0][0], run[-1][0]))
            for i, b in run:
                print('  %4d  (%2d) %s' % (i, T.wc(b), b[:110]))
    bad = frac > FRAC_MAX or longest > SERIES_MAX or len(long_replicas) < LONG_MIN
    return 1 if bad else 0


if __name__ == '__main__':
    rc = 0
    for p in T.argv_paths():
        rc += report(p, T.verbose())
    sys.exit(1 if rc else 0)
