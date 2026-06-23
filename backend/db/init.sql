-- ============================================
-- EnglishGo 英文学习平台 - 数据库初始化脚本
-- 适用于 SQLite / MySQL / PostgreSQL
-- ============================================

-- 创建用户扩展信息表
CREATE TABLE IF NOT EXISTS user_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    avatar VARCHAR(255) NOT NULL DEFAULT '',
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- 创建单词表
CREATE TABLE IF NOT EXISTS word (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    english VARCHAR(200) NOT NULL,
    chinese VARCHAR(200) NOT NULL,
    phonetic VARCHAR(200) NOT NULL DEFAULT '',
    part_of_speech VARCHAR(20) NOT NULL DEFAULT 'noun',
    example TEXT NOT NULL DEFAULT '',
    category VARCHAR(20) NOT NULL DEFAULT 'basic',
    difficulty INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_word_category ON word(category);
CREATE INDEX IF NOT EXISTS idx_word_difficulty ON word(difficulty);

-- 创建用户-单词关系表
CREATE TABLE IF NOT EXISTS user_word (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    is_favorite INTEGER NOT NULL DEFAULT 0,
    mastered INTEGER NOT NULL DEFAULT 0,
    practice_count INTEGER NOT NULL DEFAULT 0,
    correct_count INTEGER NOT NULL DEFAULT 0,
    last_practiced DATETIME,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (word_id) REFERENCES word(id) ON DELETE CASCADE,
    UNIQUE(user_id, word_id)
);

-- 创建测验记录表
CREATE TABLE IF NOT EXISTS quiz_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    quiz_type VARCHAR(20) NOT NULL,
    total_questions INTEGER NOT NULL DEFAULT 0,
    correct_answers INTEGER NOT NULL DEFAULT 0,
    score REAL NOT NULL DEFAULT 0,
    completed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- 创建测验详情表
CREATE TABLE IF NOT EXISTS quiz_detail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_record_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    question VARCHAR(500) NOT NULL,
    correct_answer VARCHAR(500) NOT NULL,
    user_answer VARCHAR(500) NOT NULL DEFAULT '',
    is_correct INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (quiz_record_id) REFERENCES quiz_record(id) ON DELETE CASCADE
);

-- 创建每日学习进度表
CREATE TABLE IF NOT EXISTS daily_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    words_learned INTEGER NOT NULL DEFAULT 0,
    words_reviewed INTEGER NOT NULL DEFAULT 0,
    quiz_count INTEGER NOT NULL DEFAULT 0,
    study_minutes INTEGER NOT NULL DEFAULT 0,
    checked_in INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    UNIQUE(user_id, date)
);

-- ============================================
-- 初始词汇数据 (60个英文单词)
-- ============================================

-- 基础词汇 (basic)
INSERT INTO word (english, chinese, phonetic, part_of_speech, example, category, difficulty) VALUES
('abandon', '放弃；抛弃', '/əˈbændən/', 'verb', 'He had to abandon his plan.', 'basic', 2),
('ability', '能力；才能', '/əˈbɪləti/', 'noun', 'She has the ability to learn quickly.', 'basic', 1),
('abroad', '在国外；到国外', '/əˈbrɔːd/', 'adverb', 'He is studying abroad.', 'basic', 1),
('absent', '缺席的；不在的', '/ˈæbsənt/', 'adjective', 'She was absent from school yesterday.', 'basic', 1),
('absorb', '吸收；吸引', '/əbˈzɔːb/', 'verb', 'Plants absorb water from the soil.', 'basic', 2),
('accept', '接受；同意', '/əkˈsept/', 'verb', 'I accept your invitation.', 'basic', 1),
('accident', '事故；意外', '/ˈæksɪdənt/', 'noun', 'There was a car accident.', 'basic', 1),
('achieve', '实现；达到', '/əˈtʃiːv/', 'verb', 'She achieved her goal.', 'basic', 2),
('active', '活跃的；积极的', '/ˈæktɪv/', 'adjective', 'He is an active member.', 'basic', 1),
('actually', '实际上；事实上', '/ˈæktʃuəli/', 'adverb', 'Actually, I don''t agree.', 'basic', 1),
('balance', '平衡；均衡', '/ˈbæləns/', 'noun', 'You need to keep a balance.', 'basic', 2),
('behavior', '行为；举止', '/bɪˈheɪvjər/', 'noun', 'His behavior was excellent.', 'basic', 2),
('believe', '相信；认为', '/bɪˈliːv/', 'verb', 'I believe in you.', 'basic', 1),
('benefit', '利益；好处', '/ˈbenɪfɪt/', 'noun', 'Exercise has many benefits.', 'basic', 2),
('breathe', '呼吸', '/briːð/', 'verb', 'Breathe deeply.', 'basic', 2),
('brilliant', '杰出的；明亮的', '/ˈbrɪliənt/', 'adjective', 'That''s a brilliant idea!', 'basic', 2),
('challenge', '挑战；质疑', '/ˈtʃælɪndʒ/', 'noun', 'This is a real challenge.', 'basic', 2),
('character', '性格；角色；字符', '/ˈkærəktər/', 'noun', 'He has a strong character.', 'basic', 2),
('comfortable', '舒适的；舒服的', '/ˈkʌmftəbl/', 'adjective', 'This chair is comfortable.', 'basic', 2),
('communicate', '沟通；交流', '/kəˈmjuːnɪkeɪt/', 'verb', 'We communicate by email.', 'basic', 2);

-- 中级词汇 (intermediate)
INSERT INTO word (english, chinese, phonetic, part_of_speech, example, category, difficulty) VALUES
('abundant', '丰富的；充裕的', '/əˈbʌndənt/', 'adjective', 'The region has abundant natural resources.', 'intermediate', 3),
('accommodate', '容纳；提供住宿', '/əˈkɑːmədeɪt/', 'verb', 'The hotel can accommodate 200 guests.', 'intermediate', 3),
('accumulate', '积累；积聚', '/əˈkjuːmjəleɪt/', 'verb', 'He accumulated a large fortune.', 'intermediate', 3),
('acknowledge', '承认；确认', '/əkˈnɑːlɪdʒ/', 'verb', 'She acknowledged her mistake.', 'intermediate', 3),
('advocate', '提倡；拥护', '/ˈædvəkeɪt/', 'verb', 'He advocates for human rights.', 'intermediate', 3),
('ambiguous', '模糊的；有歧义的', '/æmˈbɪɡjuəs/', 'adjective', 'The statement was ambiguous.', 'intermediate', 4),
('anticipate', '预期；期望', '/ænˈtɪsɪpeɪt/', 'verb', 'We anticipate a large crowd.', 'intermediate', 3),
('appreciate', '欣赏；感激；升值', '/əˈpriːʃieɪt/', 'verb', 'I really appreciate your help.', 'intermediate', 3),
('bureaucracy', '官僚机构；官僚主义', '/bjʊˈrɑːkrəsi/', 'noun', 'The bureaucracy slows things down.', 'intermediate', 4),
('comprehensive', '全面的；综合的', '/ˌkɑːmprɪˈhensɪv/', 'adjective', 'We need a comprehensive plan.', 'intermediate', 3),
('controversial', '有争议的', '/ˌkɑːntrəˈvɜːrʃl/', 'adjective', 'It''s a controversial topic.', 'intermediate', 4),
('demonstrate', '证明；演示；示威', '/ˈdemənstreɪt/', 'verb', 'Let me demonstrate how it works.', 'intermediate', 3);

-- 高级词汇 (advanced)
INSERT INTO word (english, chinese, phonetic, part_of_speech, example, category, difficulty) VALUES
('aberration', '异常；偏差', '/ˌæbəˈreɪʃn/', 'noun', 'This was an aberration from the norm.', 'advanced', 5),
('acquiesce', '默许；勉强同意', '/ˌækwiˈes/', 'verb', 'He acquiesced to their demands.', 'advanced', 5),
('ameliorate', '改善；改良', '/əˈmiːliəreɪt/', 'verb', 'Steps were taken to ameliorate the situation.', 'advanced', 5),
('anachronism', '时代错误；不合时宜', '/əˈnækrənɪzəm/', 'noun', 'The monarchy is seen as an anachronism.', 'advanced', 5),
('circumspect', '谨慎的；小心的', '/ˈsɜːrkəmspekt/', 'adjective', 'She was circumspect in her remarks.', 'advanced', 5),
('conundrum', '难题；谜题', '/kəˈnʌndrəm/', 'noun', 'It''s a real conundrum.', 'advanced', 5),
('dichotomy', '二分法；对立', '/daɪˈkɑːtəmi/', 'noun', 'There is a dichotomy between theory and practice.', 'advanced', 5),
('ephemeral', '短暂的；转瞬即逝的', '/ɪˈfemərəl/', 'adjective', 'Fame is ephemeral.', 'advanced', 5);

-- 商务词汇 (business)
INSERT INTO word (english, chinese, phonetic, part_of_speech, example, category, difficulty) VALUES
('agenda', '议程；议事日程', '/əˈdʒendə/', 'noun', 'What''s on the agenda today?', 'business', 2),
('budget', '预算', '/ˈbʌdʒɪt/', 'noun', 'We need to stay within budget.', 'business', 2),
('collaborate', '合作；协作', '/kəˈlæbəreɪt/', 'verb', 'We collaborate with many partners.', 'business', 3),
('deadline', '截止日期', '/ˈdedlaɪn/', 'noun', 'The deadline is next Friday.', 'business', 1),
('entrepreneur', '企业家', '/ˌɑːntrəprəˈnɜːr/', 'noun', 'She is a successful entrepreneur.', 'business', 3),
('feasibility', '可行性', '/ˌfiːzəˈbɪləti/', 'noun', 'We need to study the feasibility.', 'business', 3),
('implement', '实施；执行', '/ˈɪmplɪment/', 'verb', 'We will implement the new policy.', 'business', 3),
('negotiate', '谈判；协商', '/nɪˈɡoʊʃieɪt/', 'verb', 'We need to negotiate the terms.', 'business', 3),
('proposal', '提案；建议书', '/prəˈpoʊzl/', 'noun', 'I''ve submitted my proposal.', 'business', 2),
('strategy', '策略；战略', '/ˈstrætədʒi/', 'noun', 'We need a new strategy.', 'business', 2);

-- 旅游词汇 (travel)
INSERT INTO word (english, chinese, phonetic, part_of_speech, example, category, difficulty) VALUES
('accommodation', '住宿；膳宿', '/əˌkɑːməˈdeɪʃn/', 'noun', 'We need to find accommodation.', 'travel', 2),
('boarding pass', '登机牌', '', 'phrase', 'Please show your boarding pass.', 'travel', 1),
('currency', '货币', '/ˈkɜːrənsi/', 'noun', 'What currency do they use?', 'travel', 2),
('departure', '出发；离开', '/dɪˈpɑːrtʃər/', 'noun', 'The departure time is 3 PM.', 'travel', 1),
('destination', '目的地', '/ˌdestɪˈneɪʃn/', 'noun', 'We reached our destination.', 'travel', 2),
('itinerary', '行程表；旅行计划', '/aɪˈtɪnəreri/', 'noun', 'Here is our itinerary.', 'travel', 3),
('luggage', '行李', '/ˈlʌɡɪdʒ/', 'noun', 'I have two pieces of luggage.', 'travel', 1),
('passport', '护照', '/ˈpæspɔːrt/', 'noun', 'Don''t forget your passport.', 'travel', 1),
('reservation', '预订；预约', '/ˌrezərˈveɪʃn/', 'noun', 'I have a reservation.', 'travel', 2),
('sightseeing', '观光；游览', '/ˈsaɪtsiːɪŋ/', 'noun', 'We went sightseeing all day.', 'travel', 2);

-- ============================================
-- 统计确认
-- ============================================
-- 总词汇: 60个
--   basic:        20个 (难度 1-2)
--   intermediate: 12个 (难度 3-4)
--   advanced:      8个 (难度 5)
--   business:     10个 (难度 1-3)
--   travel:       10个 (难度 1-3)
-- ============================================
