"""
一次性管理命令：从7个考试词表（junior/senior/CET4/CET6/graduate/TOEFL/SAT）
清洗、去重后批量导入到统一的 word 表。

自动检测源表是否存在，不存在则从 backend/db/*.sql 文件自动导入到 MySQL。

用法：
    python manage.py import_exam_words              # 自动检测 + 导入
    python manage.py import_exam_words --dry-run    # 仅统计不写入
    python manage.py import_exam_words --import-sql # 强制重新导入 SQL 文件
"""
import re
import os
from collections import OrderedDict
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from vocabulary.models import Word


# ── 7 个考试源表 → category + difficulty + SQL 文件名映射 ──
SOURCE_TABLES = OrderedDict([
    ('junior',     {'category': 'junior',       'difficulty': 1, 'sql': '1 初中-乱序_sql.sql'}),
    ('senior',     {'category': 'senior',       'difficulty': 2, 'sql': '2 高中-乱序_sql.sql'}),
    ('CET4',       {'category': 'cet4',         'difficulty': 3, 'sql': '3 四级-乱序_sql.sql'}),
    ('CET6',       {'category': 'cet6',         'difficulty': 4, 'sql': '4 六级-乱序_sql.sql'}),
    ('graduate',   {'category': 'postgraduate', 'difficulty': 4, 'sql': '5 考研-乱序_sql.sql'}),
    ('TOEFL',      {'category': 'toefl',        'difficulty': 5, 'sql': '6 托福-乱序_sql.sql'}),
    ('SAT',        {'category': 'sat',          'difficulty': 5, 'sql': '7 SAT-乱序_sql.sql'}),
])

# ── 词性缩写映射 ──
POS_PATTERN = re.compile(
    r'^(n\.|noun\.?|v\.|verb\.?|vi\.|vt\.|adj\.|a\.|adv\.|ad\.|'
    r'prep\.|conj\.|pron\.|num\.|art\.|int\.|interj\.|aux\.|modal\.?)\s*',
    re.IGNORECASE
)

POS_MAP = {
    'n': 'noun', 'noun': 'noun',
    'v': 'verb', 'verb': 'verb', 'vi': 'verb', 'vt': 'verb',
    'adj': 'adjective', 'a': 'adjective',
    'adv': 'adverb', 'ad': 'adverb',
    'prep': 'preposition',
    'conj': 'conjunction',
    'pron': 'pronoun',
    'num': 'adjective',
    'art': 'adjective',
    'int': 'conjunction',
    'interj': 'conjunction',
    'aux': 'verb',
    'modal': 'verb',
}

CLEAN_PATTERNS = [
    (re.compile(r'\[复数[^\]]*\]'), ''),
    (re.compile(r'\[过去式[^\]]*\]'), ''),
    (re.compile(r'\[过去分词[^\]]*\]'), ''),
    (re.compile(r'\[现在分词[^\]]*\]'), ''),
    (re.compile(r'\[比较级[^\]]*\]'), ''),
    (re.compile(r'\[最高级[^\]]*\]'), ''),
    (re.compile(r'\[第三人称单数[^\]]*\]'), ''),
    (re.compile(r'\[\s*(C|U|常用复数|pl\.?|sing\.?|单数|不可数)\s*\]'), ''),
    (re.compile(r'\[(亦|也|又|同|见)[^\]]*\]'), ''),
    (re.compile(r'<[^>]+>'), ''),
]

# INSERT 值解析正则：匹配 VALUES ('word','translate');
INSERT_RE = re.compile(
    r"INSERT\s+INTO\s+`?(\w+)`?\s*\(word\s*,\s*translate\)\s*VALUES\s*"
    r"\(\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*\)\s*;",
    re.IGNORECASE
)


def parse_translate(raw: str) -> dict:
    """将原始 translate 解析为 {chinese, part_of_speech}"""
    if not raw or not raw.strip():
        return {'chinese': '', 'part_of_speech': 'noun'}

    text = raw.strip()
    pos = 'noun'
    pos_match = POS_PATTERN.match(text)
    if pos_match:
        pos_abbr = pos_match.group(1).rstrip('. ').lower()
        pos = POS_MAP.get(pos_abbr, 'noun')
        text = text[pos_match.end():]

    if not text.strip():
        text = raw.strip()

    for pattern, replacement in CLEAN_PATTERNS:
        text = pattern.sub(replacement, text)

    second_pos = POS_PATTERN.search(text)
    if second_pos:
        text = text[:second_pos.start()]

    text = re.sub(r';\s*$', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    if len(text) > 200:
        text = text[:197] + '...'

    return {'chinese': text, 'part_of_speech': pos}


class Command(BaseCommand):
    help = '从7个考试词表批量导入到统一word表（自动导入SQL+清洗去重）'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help='仅统计不实际写入')
        parser.add_argument('--import-sql', action='store_true',
                            help='强制重新导入 SQL 文件到源表')

    # ────────────── 第一步：导入 SQL 文件到 MySQL ──────────────
    def _import_sql_files(self, force=False):
        """把 7 个 SQL 文件导入 MySQL，创建源表并插入原始数据"""
        db_dir = Path(settings.BASE_DIR) / 'db'

        for table_name, config in SOURCE_TABLES.items():
            sql_file = db_dir / config['sql']

            if not sql_file.exists():
                self.stderr.write(self.style.ERROR(f'  ✗ 找不到 {sql_file}'))
                continue

            # 检查表是否已存在且有数据
            if not force:
                try:
                    with connection.cursor() as c:
                        c.execute(f'SELECT COUNT(*) FROM `{table_name}`')
                        cnt = c.fetchone()[0]
                        if cnt > 0:
                            self.stdout.write(f'  ✓ {table_name}: 已有 {cnt} 条，跳过')
                            continue
                except Exception:
                    pass  # 表不存在，继续导入

            self.stdout.write(f'  ⏳ 导入 {config["sql"]} → {table_name} ...', ending='')

            try:
                with open(sql_file, 'r', encoding='utf-8') as f:
                    sql_text = f.read()

                with connection.cursor() as cursor:
                    # 先执行建表语句（SET / DROP / CREATE）
                    for stmt in re.split(r';\s*\n', sql_text):
                        stmt = stmt.strip()
                        if not stmt:
                            continue
                        # INSERT 语句单独处理，用正则批量解析
                        if stmt.upper().startswith('INSERT'):
                            continue
                        try:
                            cursor.execute(stmt)
                        except Exception:
                            pass  # 忽略单个非关键语句错误

                    # 用正则批量提取所有 INSERT 的值
                    matches = INSERT_RE.findall(sql_text)
                    if matches:
                        all_values = [(tbl, w, tr) for tbl, w, tr in matches]
                        # 分批插入，每批 2000 条
                        batch_size = 2000
                        for i in range(0, len(all_values), batch_size):
                            batch = all_values[i:i + batch_size]
                            values = [(w, tr) for _, w, tr in batch]
                            cursor.executemany(
                                f'INSERT INTO `{table_name}` (word, translate) VALUES (%s, %s)',
                                values
                            )
                    else:
                        # 如果正则解析失败（极少情况），逐行执行 INSERT
                        for line in sql_text.split('\n'):
                            line = line.strip()
                            if line.upper().startswith('INSERT'):
                                try:
                                    cursor.execute(line)
                                except Exception:
                                    pass

                self.stdout.write(self.style.SUCCESS(f' ✓ 完成'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f' ✗ 失败: {e}'))

    # ────────────── 第二步：从源表读取原始数据 ──────────────
    def _read_source_tables(self):
        all_raw = []
        per_table_count = {}

        for table_name, config in SOURCE_TABLES.items():
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f'SELECT word, translate FROM `{table_name}`')
                    rows = cursor.fetchall()
            except Exception as e:
                self.stderr.write(self.style.WARNING(f'  跳过 {table_name}: {e}'))
                continue

            per_table_count[table_name] = len(rows)
            for word, translate in rows:
                if word and word.strip():
                    all_raw.append((word.strip(), translate or '', table_name))

        return all_raw, per_table_count

    # ────────────── 主流程 ──────────────
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        import_sql = options['import_sql']

        # ── 步骤 0：导入 SQL 文件 ──
        self.stdout.write(f'\n{"=" * 60}')
        self.stdout.write('  [0/5] 检查并导入考试词表 SQL 文件到 MySQL')
        self.stdout.write(f'{"=" * 60}')
        self._import_sql_files(force=import_sql)

        # ── 步骤 1：读取原始数据 ──
        all_raw, per_table_count = self._read_source_tables()

        self.stdout.write(f'\n{"=" * 60}')
        self.stdout.write('  [1/5] 原始数据统计（7 个考试词表）')
        self.stdout.write(f'{"=" * 60}')
        for t, c in per_table_count.items():
            self.stdout.write(f'  {t:12s} → {c:>6} 条')
        self.stdout.write(f'  {"合计":12s} → {len(all_raw):>6} 条\n')

        if not all_raw:
            self.stderr.write(self.style.ERROR('❌ 所有源表都为空，无法导入。请检查 SQL 文件。'))
            return

        # ── 步骤 2：清洗 + 去重 ──
        best = {}
        for english, raw_translate, table_name in all_raw:
            key = english.lower()
            parsed = parse_translate(raw_translate)
            cfg = SOURCE_TABLES[table_name]
            difficulty = cfg['difficulty']

            if key not in best or difficulty >= best[key]['difficulty']:
                best[key] = {
                    'english': english,
                    'chinese': parsed['chinese'],
                    'part_of_speech': parsed['part_of_speech'],
                    'category': cfg['category'],
                    'difficulty': difficulty,
                }

        self.stdout.write(f'  [2/5] 去重后 → {len(best):>6} 个唯一单词\n')

        # ── 步骤 3：统计 ──
        empty_chinese = sum(1 for v in best.values() if not v['chinese'])
        if empty_chinese:
            self.stdout.write(self.style.WARNING(
                f'  ⚠ 有 {empty_chinese} 个单词解析后中文为空（将保留英文）'
            ))
            for v in best.values():
                if not v['chinese']:
                    v['chinese'] = v['english']

        category_stats = {}
        for v in best.values():
            c = v['category']
            category_stats[c] = category_stats.get(c, 0) + 1

        self.stdout.write(f'  [3/5] 按分类统计：')
        for cat, cnt in category_stats.items():
            self.stdout.write(f'    {cat:15s} → {cnt:>6} 个')

        # ── 步骤 4：检查已存在的词 ──
        existing_lower = {
            e.lower() for e in Word.objects.values_list('english', flat=True)
        }

        new_words = []
        skipped = 0
        for key, data in best.items():
            if key in existing_lower:
                skipped += 1
                continue
            new_words.append(Word(
                english=data['english'],
                chinese=data['chinese'],
                part_of_speech=data['part_of_speech'],
                category=data['category'],
                difficulty=data['difficulty'],
                phonetic='',
                example='',
            ))

        self.stdout.write(f'\n  [4/5] 已在 word 表中: {skipped} 个（跳过）')
        self.stdout.write(f'        待导入新词:     {len(new_words)} 个\n')

        if dry_run:
            self.stdout.write(self.style.SUCCESS('[DRY RUN] 以上为模拟结果，未实际写入。'))
            return

        if not new_words:
            self.stdout.write(self.style.SUCCESS('✅ 没有新词需要导入。'))
            return

        # ── 步骤 5：批量写入 ──
        self.stdout.write('  [5/5] 写入中...')
        BATCH_SIZE = 2000
        created = 0
        total = len(new_words)

        for i in range(0, total, BATCH_SIZE):
            batch = new_words[i:i + BATCH_SIZE]
            Word.objects.bulk_create(batch, batch_size=BATCH_SIZE)
            created += len(batch)
            self.stdout.write(
                f'        进度 {min(i + BATCH_SIZE, total):>6}/{total}'
            )

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ 导入完成！\n'
            f'   原始数据:  {len(all_raw)} 条\n'
            f'   去重跳过:  {len(all_raw) - len(best)} 个\n'
            f'   已存在:    {skipped} 个\n'
            f'   成功新增:  {created} 个\n'
            f'   word 表总计: {Word.objects.count()} 个'
        ))
