-- ============================================
-- EnglishGo 英文学习平台 - MySQL 数据库初始化
-- 使用方式: mysql -u root -p < init_mysql.sql
-- ============================================

CREATE DATABASE IF NOT EXISTS englishgo DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE englishgo;

-- ============================================
-- 注意: auth_user 表由 Django migrate 自动创建
-- 以下 6 张表为业务表
-- ============================================

-- 用户扩展信息表
CREATE TABLE IF NOT EXISTS user_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    avatar VARCHAR(255) NOT NULL DEFAULT '',
    CONSTRAINT fk_user_profile_user FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 单词表
CREATE TABLE IF NOT EXISTS word (
    id INT AUTO_INCREMENT PRIMARY KEY,
    english VARCHAR(200) NOT NULL,
    chinese VARCHAR(200) NOT NULL,
    phonetic VARCHAR(200) NOT NULL DEFAULT '',
    part_of_speech VARCHAR(20) NOT NULL DEFAULT 'noun',
    example TEXT NOT NULL,
    category VARCHAR(20) NOT NULL DEFAULT 'basic',
    difficulty INT NOT NULL DEFAULT 1,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    INDEX idx_word_category (category),
    INDEX idx_word_difficulty (difficulty)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户-单词关系表
CREATE TABLE IF NOT EXISTS user_word (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    word_id INT NOT NULL,
    is_favorite TINYINT(1) NOT NULL DEFAULT 0,
    mastered TINYINT(1) NOT NULL DEFAULT 0,
    practice_count INT NOT NULL DEFAULT 0,
    correct_count INT NOT NULL DEFAULT 0,
    last_practiced DATETIME(6) NULL,
    CONSTRAINT fk_user_word_user FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_word_word FOREIGN KEY (word_id) REFERENCES word(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_word (user_id, word_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 测验记录表
CREATE TABLE IF NOT EXISTS quiz_record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    quiz_type VARCHAR(20) NOT NULL,
    total_questions INT NOT NULL DEFAULT 0,
    correct_answers INT NOT NULL DEFAULT 0,
    score DOUBLE NOT NULL DEFAULT 0,
    completed_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    CONSTRAINT fk_quiz_record_user FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 测验详情表
CREATE TABLE IF NOT EXISTS quiz_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_record_id INT NOT NULL,
    word_id INT NOT NULL,
    question VARCHAR(500) NOT NULL,
    correct_answer VARCHAR(500) NOT NULL,
    user_answer VARCHAR(500) NOT NULL DEFAULT '',
    is_correct TINYINT(1) NOT NULL DEFAULT 0,
    CONSTRAINT fk_quiz_detail_record FOREIGN KEY (quiz_record_id) REFERENCES quiz_record(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 每日学习进度表
CREATE TABLE IF NOT EXISTS daily_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    words_learned INT NOT NULL DEFAULT 0,
    words_reviewed INT NOT NULL DEFAULT 0,
    quiz_count INT NOT NULL DEFAULT 0,
    study_minutes INT NOT NULL DEFAULT 0,
    checked_in TINYINT(1) NOT NULL DEFAULT 0,
    CONSTRAINT fk_daily_progress_user FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    UNIQUE KEY uk_daily_progress (user_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 文章表
CREATE TABLE IF NOT EXISTS article (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    title_cn VARCHAR(300) NOT NULL DEFAULT '',
    author VARCHAR(100) NOT NULL DEFAULT 'EnglishGo',
    content LONGTEXT NOT NULL,
    content_cn LONGTEXT NOT NULL,
    summary LONGTEXT NOT NULL,
    level VARCHAR(20) NOT NULL DEFAULT 'intermediate',
    tags VARCHAR(300) NOT NULL DEFAULT '',
    word_count INT NOT NULL DEFAULT 0,
    read_count INT NOT NULL DEFAULT 0,
    source_url VARCHAR(200) NOT NULL DEFAULT '',
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    INDEX idx_article_level (level),
    INDEX idx_article_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
-- 统计: 基础20 + 中级12 + 高级8 + 商务10 + 旅游10 = 共60个
-- ============================================

-- ============================================
-- 初始文章数据 (6篇英文文章)
-- ============================================

INSERT INTO article (title, title_cn, author, content, content_cn, summary, level, tags) VALUES
(
    'The Benefits of Reading Every Day',
    '每天阅读的好处',
    'EnglishGo',
    'Reading is one of the most valuable habits a person can develop. It opens doors to new knowledge, improves vocabulary, and sharpens the mind. Studies show that people who read regularly have better memory and stronger analytical skills.\n\nWhen you read in a foreign language like English, the benefits multiply. You naturally absorb grammar patterns, learn new words in context, and develop a sense of how native speakers express ideas. Unlike memorizing vocabulary lists, reading shows you how words are actually used.\n\nStart with short articles on topics you enjoy. Don''t worry about understanding every single word — focus on grasping the main ideas. Over time, your reading speed and comprehension will improve dramatically.\n\nMake reading a daily habit. Even fifteen minutes a day can make a significant difference. Choose materials that are slightly challenging but not frustrating. This is called the ''comprehensible input'' approach, and it''s one of the most effective ways to learn a language.',
    '阅读是一个人能养成的最有价值的习惯之一。它为新的知识打开大门，改善词汇量，并锻炼思维。研究表明，经常阅读的人记忆力更好，分析能力更强。\n\n当你用英语这样的外语阅读时，好处会成倍增加。你自然吸收语法模式，在语境中学习新词汇，并培养对母语者表达方式的感觉。与背诵词汇表不同，阅读向你展示单词实际如何被使用。\n\n从你感兴趣主题的短文章开始。不要担心理解每一个单词——专注于掌握主旨。随着时间的推移，你的阅读速度和理解能力将显著提高。\n\n让阅读成为日常习惯。即使每天十五分钟也能产生显著差异。选择略具挑战性但不会令人沮丧的材料。这被称为''可理解输入''方法，是学习语言最有效的方式之一。',
    'Discover why daily reading is one of the most powerful habits for English learners.',
    'beginner',
    'reading,habits,learning tips'
),
(
    'A Day in New York City',
    '纽约市的一天',
    'EnglishGo',
    'New York City wakes up early. By 6 AM, the streets are already busy with delivery trucks, early commuters, and people walking their dogs. The smell of fresh coffee and bagels fills the air from corner delis and coffee shops.\n\nThe subway is the lifeline of the city. Millions of New Yorkers ride it every day. During rush hour, platforms are packed with people checking their phones, reading newspapers, or simply staring ahead, lost in thought before the workday begins.\n\nCentral Park offers a peaceful escape from the concrete jungle. Joggers circle the reservoir, families spread picnic blankets on the Great Lawn, and street musicians fill the air with jazz and folk music. In spring, the cherry blossoms create a stunning pink canopy over the paths.\n\nAs evening falls, the city transforms. Broadway theaters light up, restaurants fill with diners, and the skyline glitters with millions of lights. From the top of the Empire State Building, the view is breathtaking — a sea of lights stretching as far as the eye can see.\n\nNew York truly is the city that never sleeps.',
    '纽约市醒得很早。到早上6点，街道上已经满是送货车、早班通勤者和遛狗的人。新鲜咖啡和贝果的香味从街角熟食店和咖啡店飘散到空气中。\n\n地铁是这座城市的生命线。数百万人每天乘坐地铁。在高峰期，站台上挤满了看手机、读报纸，或只是凝视前方、在工作日开始前陷入沉思的人。\n\n中央公园提供了远离水泥丛林的宁静逃逸。慢跑者环绕水库，家庭在大草坪上铺开野餐毯，街头音乐家让空气中充满爵士和民谣音乐。春天，樱花在步道上形成令人惊叹的粉色华盖。\n\n随着夜幕降临，城市变了模样。百老汇剧院亮起灯光，餐馆里坐满了食客，天际线闪烁着数百万盏灯。从帝国大厦顶端眺望，景色令人屏息——一片灯海延伸到目之所及之处。\n\n纽约确实是一座不眠之城。',
    'Experience a typical day in America''s most famous city, from morning coffee to Broadway lights.',
    'beginner',
    'travel,culture,new york'
),
(
    'The Science of Happiness',
    '幸福的科学',
    'EnglishGo',
    'What makes people happy? For centuries, philosophers have debated this question. Today, psychologists and neuroscientists are finding answers through rigorous research.\n\nOne of the most important discoveries is that happiness is not primarily determined by external circumstances. While factors like income, health, and relationships do matter, research suggests that approximately 40% of our happiness is within our conscious control.\n\nGratitude practice is one of the most evidence-backed happiness strategies. People who regularly write down things they are grateful for report higher levels of well-being. This simple exercise rewires the brain to notice positive experiences more readily.\n\nSocial connections are another crucial factor. The famous Harvard Study of Adult Development, which tracked participants for over 80 years, found that close relationships are the strongest predictor of a happy, healthy life.\n\nExercise, adequate sleep, and time in nature also contribute significantly to happiness. Physical activity releases endorphins, while nature exposure reduces stress and improves mood. Combined, these habits create a strong foundation for mental well-being.\n\nThe key insight from happiness research is that small, consistent actions often matter more than dramatic life changes. A daily walk, a kind word, a moment of gratitude — these simple practices, repeated over time, can transform how we experience life.',
    '什么让人幸福？几个世纪以来，哲学家们一直在争论这个问题。如今，心理学家和神经科学家正在通过严谨的研究找到答案。\n\n最重要的发现之一是，幸福并不主要由外部环境决定。虽然收入、健康和人际关系等因素确实重要，但研究表明，大约40%的幸福在我们的意识控制范围内。\n\n感恩练习是最有证据支持的幸福策略之一。定期写下感恩事项的人报告了更高的幸福感水平。这个简单的练习能重新连接大脑，使其更容易注意到积极体验。\n\n社交联系是另一个关键因素。著名的哈佛成人发展研究追踪参与者超过80年，发现亲密关系是幸福健康生活最有力的预测因素。\n\n运动、充足睡眠和亲近大自然也对幸福有显著贡献。身体活动释放内啡肽，而接触自然减轻压力并改善心情。综合起来，这些习惯为心理健康奠定了坚实基础。\n\n幸福研究的关键洞见是，小而持续的行动往往比戏剧性的生活变化更重要。每天散步、一句友善的话、一个感恩的时刻——这些简单的练习，随着时间反复进行，可以改变我们体验生活的方式。',
    'Explore what modern science reveals about the keys to lasting happiness and well-being.',
    'intermediate',
    'science,psychology,happiness'
),
(
    'Why We Procrastinate and How to Stop',
    '我们为什么拖延以及如何停止',
    'EnglishGo',
    'Procrastination is not about laziness. According to psychologists, it is an emotional regulation problem, not a time management problem. When we procrastinate, we are trying to avoid negative feelings — boredom, anxiety, insecurity, or frustration — rather than avoiding the task itself.\n\nThe brain''s limbic system, which processes emotions, often overrides the prefrontal cortex, the part responsible for planning and decision-making. This is why we sometimes find ourselves scrolling social media instead of working on an important project.\n\nSo how can we overcome procrastination? Research points to several effective strategies:\n\nFirst, break tasks into tiny steps. The smaller the first step, the less resistance you will feel. Instead of ''write the report,'' start with ''open the document and write the title.'' This lowers the emotional barrier to getting started.\n\nSecond, use the ''two-minute rule.'' If a task takes less than two minutes, do it immediately. This prevents small tasks from piling up and creating a sense of overwhelm.\n\nThird, practice self-compassion. Studies show that people who forgive themselves for procrastinating are less likely to procrastinate in the future. Guilt and self-criticism actually make the problem worse by increasing negative emotions.\n\nFinally, make the task more appealing. Pair it with something you enjoy — listen to music while cleaning, work at a favorite café, or reward yourself after completing each milestone.\n\nRemember: action comes before motivation, not the other way around. Start small, be kind to yourself, and build momentum one step at a time.',
    '拖延与懒惰无关。据心理学家称，这是一个情绪调节问题，而非时间管理问题。当我们拖延时，我们在试图避免负面情绪——无聊、焦虑、不安或挫败——而不是在逃避任务本身。\n\n大脑中处理情绪的边缘系统，经常超越前额叶皮层——负责规划和决策的部分。这就是为什么我们有时会发现自己刷社交媒体，而不是在完成重要项目。\n\n那么我们如何克服拖延？研究指出了几种有效策略：\n\n首先，将任务分解为微小步骤。第一步越小，阻力就越小。不要想''写报告''，从''打开文档并写标题''开始。这降低了开始行动的情感障碍。\n\n第二，使用''两分钟规则''。如果任务只需不到两分钟，立即去做。这防止小任务堆积并产生压迫感。\n\n第三，练习自我同情。研究表明，原谅自己拖延的人未来更不可能拖延。内疚和自我批评实际上通过增加负面情绪使问题更糟。\n\n最后，让任务更有吸引力。将它与你喜欢的事情结合——打扫时听音乐，在最爱的咖啡馆工作，或在完成每个里程碑后奖励自己。\n\n记住：行动先于动力，而不是反过来。从小处开始，善待自己，一步一步建立惯性。',
    'Understand the psychology behind procrastination and learn research-backed techniques to overcome it.',
    'intermediate',
    'psychology,productivity,self-improvement'
),
(
    'The Rise of Artificial Intelligence in Everyday Life',
    '人工智能在日常生活中的崛起',
    'EnglishGo',
    'Artificial Intelligence has quietly become an integral part of our daily lives. From the moment we unlock our phones with facial recognition to the personalized recommendations on streaming platforms, AI algorithms are working behind the scenes.\n\nIn healthcare, AI systems can now detect certain cancers in medical images with accuracy that matches or exceeds human radiologists. Machine learning models analyze vast amounts of patient data to predict disease risks and suggest preventive measures.\n\nThe transportation industry is undergoing a revolution. Self-driving cars, once a science fiction fantasy, are now being tested on public roads. AI-powered traffic management systems optimize traffic flow in major cities, reducing congestion and emissions.\n\nHowever, the rapid advancement of AI raises important ethical questions. Concerns about job displacement, algorithmic bias, and data privacy are at the forefront of public discourse. How do we ensure that AI benefits everyone, not just a privileged few?\n\nEducation is another field being transformed. Adaptive learning platforms personalize curriculum for each student, identifying strengths and weaknesses in real time. Language learning apps use speech recognition to provide instant feedback on pronunciation.\n\nThe key to thriving in an AI-powered world is not to resist change but to adapt. Critical thinking, creativity, and emotional intelligence — skills that AI cannot easily replicate — will become increasingly valuable. The future belongs to those who can work alongside intelligent machines, leveraging their capabilities while bringing uniquely human qualities to the table.',
    '人工智能已经悄然成为我们日常生活中不可或缺的一部分。从我们用人脸识别解锁手机的那一刻，到流媒体平台上的个性化推荐，AI算法在幕后工作。\n\n在医疗领域，AI系统现在可以检测医学图像中的某些癌症，准确度达到或超过人类放射科医生。机器学习模型分析大量患者数据以预测疾病风险并建议预防措施。\n\n交通行业正在经历一场革命。自动驾驶汽车曾经是科幻小说的幻想，现在正在公共道路上测试。AI驱动的交通管理系统优化主要城市的交通流量，减少拥堵和排放。\n\n然而，人工智能的快速发展引发了重要的伦理问题。关于工作岗位流失、算法偏见和数据隐私的担忧处于公众讨论的前沿。我们如何确保AI惠及所有人，而不仅仅是少数特权阶层？\n\n教育是另一个正在被改变的领域。自适应学习平台为每个学生个性化课程，实时识别优势和弱点。语言学习应用使用语音识别提供即时的发音反馈。\n\n在AI驱动的世界中蓬勃发展的关键不是抵制变化，而是去适应。批判性思维、创造力和情商——AI难以轻易复制的技能——将变得越来越有价值。未来属于那些能与智能机器协同工作的人，他们利用机器的能力，同时发挥独特的人类品质。',
    'Explore how artificial intelligence is reshaping healthcare, transportation, education, and our daily routines.',
    'advanced',
    'technology,AI,future,society'
),
(
    'The Power of Small Habits',
    '微习惯的力量',
    'EnglishGo',
    'We often believe that big changes require big actions. But the truth is, small habits, repeated consistently, are what create lasting transformation. This principle is at the heart of James Clear''s bestselling book ''Atomic Habits.''\n\nThe math is compelling. If you improve by just 1% each day, you will be 37 times better after one year. Conversely, getting 1% worse each day leads to a decline of nearly 97% over the same period. Small changes compound.\n\nThe key is to focus on systems rather than goals. Goals tell you where you want to go; systems show you how to get there. Winners and losers often have the same goals — the difference lies in their daily systems and habits.\n\nTo build a new habit, make it obvious, attractive, easy, and satisfying. For example, if you want to read more, place a book on your pillow each morning so you see it at night. If you want to exercise, lay out your workout clothes the night before.\n\nTo break a bad habit, do the opposite: make it invisible, unattractive, difficult, and unsatisfying. Remove junk food from your home, delete social media apps from your phone, or add friction to behaviors you want to stop.\n\nRemember: you do not rise to the level of your goals; you fall to the level of your systems. Focus on building better systems, and the results will follow naturally.',
    '我们常常相信大变化需要大行动。但真相是，持续重复的小习惯，才是创造持久改变的原因。这一原则是詹姆斯·克利尔畅销书《原子习惯》的核心。\n\n数学计算令人信服。如果你每天进步1%，一年后你将进步37倍。相反，每天退步1%会导致同期近97%的下降。微小的改变会复利增长。\n\n关键是关注系统而非目标。目标告诉你想去哪里；系统告诉你如何到达。赢家和输家通常有相同的目标——区别在于他们日常的系统和习惯。\n\n要建立新习惯，让它显而易见、有吸引力、简单易行、令人满足。例如，如果你想多读书，每天早上把一本书放在枕头上，这样晚上就能看到。如果你想锻炼，前一晚把运动服放好。\n\n要打破坏习惯，反其道而行：让它不可见、没有吸引力、困难、不满足。把垃圾食品从家里清除，从手机上删除社交媒体应用，或给想停止的行为增加阻力。\n\n记住：你无法达到目标的高度，只能跌落到系统的水平。专注于构建更好的系统，结果自然会随之而来。',
    'Learn how tiny changes can lead to remarkable results, based on the principles of habit formation.',
    'beginner',
    'habits,self-improvement,productivity'
);

-- ============================================
-- 文章统计: beginner 3 + intermediate 2 + advanced 1 = 共6篇
-- 词汇统计: 基础20 + 中级12 + 高级8 + 商务10 + 旅游10 = 共60个
-- ============================================
