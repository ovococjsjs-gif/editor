#!/usr/bin/env python3
"""Общая загрузка текста для детекторов.

Принимает .docx или .txt. Отдаёт список абзацев (пустые отброшены).
Умеет отличать реплику от наррации и вынимать тело реплики без атрибуции.
"""
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
DASH = '—'
NBSP = '\u00a0'


def load(path):
    """Список непустых абзацев."""
    if path.lower().endswith('.docx'):
        raw = _from_docx(path)
    else:
        with open(path, encoding='utf-8') as fh:
            raw = fh.read().split('\n')
    out = []
    for line in raw:
        line = line.replace(NBSP, ' ').strip()
        if line:
            out.append(line)
    return out


def _from_docx(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    paras = []
    for p in root.iter(W + 'p'):
        parts = []
        for node in p.iter():
            if node.tag == W + 't':
                parts.append(node.text or '')
            elif node.tag in (W + 'tab', W + 'br'):
                parts.append(' ')
        paras.append(''.join(parts))
    return paras


def is_replica(par):
    """Абзац начинается с прямой речи."""
    return par.lstrip().startswith(DASH)


def replica_body(par):
    """Тело реплики: все речевые сегменты без авторских вставок.

    «— Морок тоже проснулся, — сказал Кайр. — Пятьдесят секунд.»
        -> «Морок тоже проснулся, Пятьдесят секунд.»
    «— Какие тиски. — Он не поднял головы от миски.» -> «Какие тиски.»

    В русской типографике сегменты, разделённые тире в пробелах,
    чередуются: речь, вставка, речь, вставка...
    """
    s = par.lstrip()
    if s.startswith(DASH):
        s = s[1:].strip()
    segs = re.split(r'\s+' + DASH + r'\s+', s)
    speech = []
    for k, seg in enumerate(segs):
        if k % 2 == 0:
            speech.append(seg.strip())
        elif wc(seg) > 20 and not _looks_like_attribution(seg):
            # длинный сегмент без глагола речи — скорее всего речь продолжается
            speech.append(seg.strip())
    return ' '.join(x for x in speech if x).strip()


_ATTR = re.compile(
    r'\b(сказал|сказала|ответил|ответила|спросил|спросила|произнёс|произнесла|'
    r'проговорил|проговорила|бросил|бросила|добавил|добавила|заметил|заметила|'
    r'согласил|согласилась|повторил|повторила|перебил|перебила|отозвал|'
    r'усмехн|кивн|пожал|посмотрел|поднял|опустил|встал|сел|отвернул)', re.I)


def _looks_like_attribution(seg):
    return bool(_ATTR.search(seg))


def words(s):
    return re.findall(r'[\w-]+', s, re.UNICODE)


def wc(s):
    return len(words(s))


def sentences(s):
    return [x for x in re.split(r'(?<=[.!?…])\s+', s) if x.strip()]


def scenes(paras, marker=re.compile(r'^[\s*•·—-]{3,}$')):
    """Разбить на сцены по разделителю вида '* * *'."""
    cur, out = [], []
    for p in paras:
        if marker.match(p.replace(' ', ' ')) or p.strip() in ('* * *', '***'):
            if cur:
                out.append(cur)
                cur = []
        else:
            cur.append(p)
    if cur:
        out.append(cur)
    return out


def argv_paths():
    paths = [a for a in sys.argv[1:] if not a.startswith('-')]
    if not paths:
        print('использование: %s <файл.docx|txt> [...] [--list] [--strict]'
              % sys.argv[0])
        sys.exit(2)
    return paths


def verbose():
    return '--list' in sys.argv or '-l' in sys.argv


def strict():
    """В строгом режиме диагностические превышения дают ненулевой код.

    По умолчанию инструменты только печатают отчёт: эвристика не должна
    блокировать литературный текст без редакторского чтения.
    """
    return '--strict' in sys.argv
