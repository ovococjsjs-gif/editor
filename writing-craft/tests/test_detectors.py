import contextlib
import io
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))

import ladder  # noqa: E402
import range as range_detector  # noqa: E402
import text  # noqa: E402
import tics  # noqa: E402


class TextParsingTests(unittest.TestCase):
    def test_replica_body_keeps_speech_after_attribution(self):
        par = '— Морок тоже проснулся, — сказал Кайр. — Пятьдесят секунд.'
        self.assertEqual(
            text.replica_body(par),
            'Морок тоже проснулся, Пятьдесят секунд.',
        )

    def test_narration_breaks_dialogue_run(self):
        paras = ['— Раз.', '— Два.', 'Он отвернулся.', '— Три.', '— Четыре.']
        self.assertEqual([len(run) for run in ladder.runs(paras)], [2, 2])

    def test_four_short_replicas_form_ladder(self):
        paras = ['— Раз.', '— Два.', '— Три.', '— Четыре.']
        self.assertEqual(len(ladder.ladders(paras)), 1)


class HeuristicTests(unittest.TestCase):
    def test_missing_register_is_not_a_mandatory_failure(self):
        regs = range_detector.registers(['Я вошла в комнату.'])
        self.assertEqual(regs['прямая речь'], 0)

    def test_three_equal_scene_lengths_are_reportable(self):
        paras = ['Первый.', '***', 'Второй.', '***', 'Третий.']
        self.assertEqual(range_detector.scene_lengths(paras), [1, 1, 1])

    def test_triad_is_only_formal_heuristic(self):
        self.assertTrue(
            tics._triad('Первое предложение немного длиннее. Второе предложение тоже длиннее. Итог.')
        )
        self.assertFalse(tics._triad('Первое. Второе. Очень длинный итог здесь.'))

    def test_range_report_does_not_fail_for_absent_old_quotas(self):
        path = Path(__file__).with_name('_short_fixture.txt')
        path.write_text(
            '\n'.join([
                'Утро началось.', 'Дверь закрылась.', 'Книга лежала.',
                'Окно светилось.', 'Снаружи шумели.', 'Позже стемнело.',
                'Рядом ждали.', 'Наверху ходили.', 'К вечеру стихло.',
                'После вернулись.', 'Тогда позвали.', 'Внизу ответили.',
            ]),
            encoding='utf-8',
        )
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                alerts = range_detector.report(str(path))
            # Only repetitive paragraph openings may alert. Missing ellipses,
            # long replicas, bodily markers and failed actions do not.
            self.assertEqual(alerts, 0)
        finally:
            path.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
