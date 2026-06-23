from django.core.management.base import BaseCommand
from vocabulary.models import Word


INITIAL_WORDS = [
    # 基础词汇
    {"english": "abandon", "chinese": "放弃；抛弃", "phonetic": "/əˈbændən/", "part_of_speech": "verb", "example": "He had to abandon his plan.", "category": "basic", "difficulty": 2},
    {"english": "ability", "chinese": "能力；才能", "phonetic": "/əˈbɪləti/", "part_of_speech": "noun", "example": "She has the ability to learn quickly.", "category": "basic", "difficulty": 1},
    {"english": "abroad", "chinese": "在国外；到国外", "phonetic": "/əˈbrɔːd/", "part_of_speech": "adverb", "example": "He is studying abroad.", "category": "basic", "difficulty": 1},
    {"english": "absent", "chinese": "缺席的；不在的", "phonetic": "/ˈæbsənt/", "part_of_speech": "adjective", "example": "She was absent from school yesterday.", "category": "basic", "difficulty": 1},
    {"english": "absorb", "chinese": "吸收；吸引", "phonetic": "/əbˈzɔːb/", "part_of_speech": "verb", "example": "Plants absorb water from the soil.", "category": "basic", "difficulty": 2},
    {"english": "accept", "chinese": "接受；同意", "phonetic": "/əkˈsept/", "part_of_speech": "verb", "example": "I accept your invitation.", "category": "basic", "difficulty": 1},
    {"english": "accident", "chinese": "事故；意外", "phonetic": "/ˈæksɪdənt/", "part_of_speech": "noun", "example": "There was a car accident.", "category": "basic", "difficulty": 1},
    {"english": "achieve", "chinese": "实现；达到", "phonetic": "/əˈtʃiːv/", "part_of_speech": "verb", "example": "She achieved her goal.", "category": "basic", "difficulty": 2},
    {"english": "active", "chinese": "活跃的；积极的", "phonetic": "/ˈæktɪv/", "part_of_speech": "adjective", "example": "He is an active member.", "category": "basic", "difficulty": 1},
    {"english": "actually", "chinese": "实际上；事实上", "phonetic": "/ˈæktʃuəli/", "part_of_speech": "adverb", "example": "Actually, I don't agree.", "category": "basic", "difficulty": 1},

    {"english": "balance", "chinese": "平衡；均衡", "phonetic": "/ˈbæləns/", "part_of_speech": "noun", "example": "You need to keep a balance.", "category": "basic", "difficulty": 2},
    {"english": "behavior", "chinese": "行为；举止", "phonetic": "/bɪˈheɪvjər/", "part_of_speech": "noun", "example": "His behavior was excellent.", "category": "basic", "difficulty": 2},
    {"english": "believe", "chinese": "相信；认为", "phonetic": "/bɪˈliːv/", "part_of_speech": "verb", "example": "I believe in you.", "category": "basic", "difficulty": 1},
    {"english": "benefit", "chinese": "利益；好处", "phonetic": "/ˈbenɪfɪt/", "part_of_speech": "noun", "example": "Exercise has many benefits.", "category": "basic", "difficulty": 2},
    {"english": "breathe", "chinese": "呼吸", "phonetic": "/briːð/", "part_of_speech": "verb", "example": "Breathe deeply.", "category": "basic", "difficulty": 2},
    {"english": "brilliant", "chinese": "杰出的；明亮的", "phonetic": "/ˈbrɪliənt/", "part_of_speech": "adjective", "example": "That's a brilliant idea!", "category": "basic", "difficulty": 2},

    {"english": "challenge", "chinese": "挑战；质疑", "phonetic": "/ˈtʃælɪndʒ/", "part_of_speech": "noun", "example": "This is a real challenge.", "category": "basic", "difficulty": 2},
    {"english": "character", "chinese": "性格；角色；字符", "phonetic": "/ˈkærəktər/", "part_of_speech": "noun", "example": "He has a strong character.", "category": "basic", "difficulty": 2},
    {"english": "comfortable", "chinese": "舒适的；舒服的", "phonetic": "/ˈkʌmftəbl/", "part_of_speech": "adjective", "example": "This chair is comfortable.", "category": "basic", "difficulty": 2},
    {"english": "communicate", "chinese": "沟通；交流", "phonetic": "/kəˈmjuːnɪkeɪt/", "part_of_speech": "verb", "example": "We communicate by email.", "category": "basic", "difficulty": 2},

    # 中级词汇
    {"english": "abundant", "chinese": "丰富的；充裕的", "phonetic": "/əˈbʌndənt/", "part_of_speech": "adjective", "example": "The region has abundant natural resources.", "category": "intermediate", "difficulty": 3},
    {"english": "accommodate", "chinese": "容纳；提供住宿", "phonetic": "/əˈkɑːmədeɪt/", "part_of_speech": "verb", "example": "The hotel can accommodate 200 guests.", "category": "intermediate", "difficulty": 3},
    {"english": "accumulate", "chinese": "积累；积聚", "phonetic": "/əˈkjuːmjəleɪt/", "part_of_speech": "verb", "example": "He accumulated a large fortune.", "category": "intermediate", "difficulty": 3},
    {"english": "acknowledge", "chinese": "承认；确认", "phonetic": "/əkˈnɑːlɪdʒ/", "part_of_speech": "verb", "example": "She acknowledged her mistake.", "category": "intermediate", "difficulty": 3},
    {"english": "advocate", "chinese": "提倡；拥护", "phonetic": "/ˈædvəkeɪt/", "part_of_speech": "verb", "example": "He advocates for human rights.", "category": "intermediate", "difficulty": 3},
    {"english": "ambiguous", "chinese": "模糊的；有歧义的", "phonetic": "/æmˈbɪɡjuəs/", "part_of_speech": "adjective", "example": "The statement was ambiguous.", "category": "intermediate", "difficulty": 4},
    {"english": "anticipate", "chinese": "预期；期望", "phonetic": "/ænˈtɪsɪpeɪt/", "part_of_speech": "verb", "example": "We anticipate a large crowd.", "category": "intermediate", "difficulty": 3},
    {"english": "appreciate", "chinese": "欣赏；感激；升值", "phonetic": "/əˈpriːʃieɪt/", "part_of_speech": "verb", "example": "I really appreciate your help.", "category": "intermediate", "difficulty": 3},

    {"english": "bureaucracy", "chinese": "官僚机构；官僚主义", "phonetic": "/bjʊˈrɑːkrəsi/", "part_of_speech": "noun", "example": "The bureaucracy slows things down.", "category": "intermediate", "difficulty": 4},
    {"english": "comprehensive", "chinese": "全面的；综合的", "phonetic": "/ˌkɑːmprɪˈhensɪv/", "part_of_speech": "adjective", "example": "We need a comprehensive plan.", "category": "intermediate", "difficulty": 3},
    {"english": "controversial", "chinese": "有争议的", "phonetic": "/ˌkɑːntrəˈvɜːrʃl/", "part_of_speech": "adjective", "example": "It's a controversial topic.", "category": "intermediate", "difficulty": 4},
    {"english": "demonstrate", "chinese": "证明；演示；示威", "phonetic": "/ˈdemənstreɪt/", "part_of_speech": "verb", "example": "Let me demonstrate how it works.", "category": "intermediate", "difficulty": 3},

    # 高级词汇
    {"english": "aberration", "chinese": "异常；偏差", "phonetic": "/ˌæbəˈreɪʃn/", "part_of_speech": "noun", "example": "This was an aberration from the norm.", "category": "advanced", "difficulty": 5},
    {"english": "acquiesce", "chinese": "默许；勉强同意", "phonetic": "/ˌækwiˈes/", "part_of_speech": "verb", "example": "He acquiesced to their demands.", "category": "advanced", "difficulty": 5},
    {"english": "ameliorate", "chinese": "改善；改良", "phonetic": "/əˈmiːliəreɪt/", "part_of_speech": "verb", "example": "Steps were taken to ameliorate the situation.", "category": "advanced", "difficulty": 5},
    {"english": "anachronism", "chinese": "时代错误；不合时宜", "phonetic": "/əˈnækrənɪzəm/", "part_of_speech": "noun", "example": "The monarchy is seen as an anachronism.", "category": "advanced", "difficulty": 5},
    {"english": "circumspect", "chinese": "谨慎的；小心的", "phonetic": "/ˈsɜːrkəmspekt/", "part_of_speech": "adjective", "example": "She was circumspect in her remarks.", "category": "advanced", "difficulty": 5},
    {"english": "conundrum", "chinese": "难题；谜题", "phonetic": "/kəˈnʌndrəm/", "part_of_speech": "noun", "example": "It's a real conundrum.", "category": "advanced", "difficulty": 5},
    {"english": "dichotomy", "chinese": "二分法；对立", "phonetic": "/daɪˈkɑːtəmi/", "part_of_speech": "noun", "example": "There is a dichotomy between theory and practice.", "category": "advanced", "difficulty": 5},
    {"english": "ephemeral", "chinese": "短暂的；转瞬即逝的", "phonetic": "/ɪˈfemərəl/", "part_of_speech": "adjective", "example": "Fame is ephemeral.", "category": "advanced", "difficulty": 5},

    # 商务词汇
    {"english": "agenda", "chinese": "议程；议事日程", "phonetic": "/əˈdʒendə/", "part_of_speech": "noun", "example": "What's on the agenda today?", "category": "business", "difficulty": 2},
    {"english": "budget", "chinese": "预算", "phonetic": "/ˈbʌdʒɪt/", "part_of_speech": "noun", "example": "We need to stay within budget.", "category": "business", "difficulty": 2},
    {"english": "collaborate", "chinese": "合作；协作", "phonetic": "/kəˈlæbəreɪt/", "part_of_speech": "verb", "example": "We collaborate with many partners.", "category": "business", "difficulty": 3},
    {"english": "deadline", "chinese": "截止日期", "phonetic": "/ˈdedlaɪn/", "part_of_speech": "noun", "example": "The deadline is next Friday.", "category": "business", "difficulty": 1},
    {"english": "entrepreneur", "chinese": "企业家", "phonetic": "/ˌɑːntrəprəˈnɜːr/", "part_of_speech": "noun", "example": "She is a successful entrepreneur.", "category": "business", "difficulty": 3},
    {"english": "feasibility", "chinese": "可行性", "phonetic": "/ˌfiːzəˈbɪləti/", "part_of_speech": "noun", "example": "We need to study the feasibility.", "category": "business", "difficulty": 3},
    {"english": "implement", "chinese": "实施；执行", "phonetic": "/ˈɪmplɪment/", "part_of_speech": "verb", "example": "We will implement the new policy.", "category": "business", "difficulty": 3},
    {"english": "negotiate", "chinese": "谈判；协商", "phonetic": "/nɪˈɡoʊʃieɪt/", "part_of_speech": "verb", "example": "We need to negotiate the terms.", "category": "business", "difficulty": 3},
    {"english": "proposal", "chinese": "提案；建议书", "phonetic": "/prəˈpoʊzl/", "part_of_speech": "noun", "example": "I've submitted my proposal.", "category": "business", "difficulty": 2},
    {"english": "strategy", "chinese": "策略；战略", "phonetic": "/ˈstrætədʒi/", "part_of_speech": "noun", "example": "We need a new strategy.", "category": "business", "difficulty": 2},

    # 旅游词汇
    {"english": "accommodation", "chinese": "住宿；膳宿", "phonetic": "/əˌkɑːməˈdeɪʃn/", "part_of_speech": "noun", "example": "We need to find accommodation.", "category": "travel", "difficulty": 2},
    {"english": "boarding pass", "chinese": "登机牌", "phonetic": "", "part_of_speech": "phrase", "example": "Please show your boarding pass.", "category": "travel", "difficulty": 1},
    {"english": "currency", "chinese": "货币", "phonetic": "/ˈkɜːrənsi/", "part_of_speech": "noun", "example": "What currency do they use?", "category": "travel", "difficulty": 2},
    {"english": "departure", "chinese": "出发；离开", "phonetic": "/dɪˈpɑːrtʃər/", "part_of_speech": "noun", "example": "The departure time is 3 PM.", "category": "travel", "difficulty": 1},
    {"english": "destination", "chinese": "目的地", "phonetic": "/ˌdestɪˈneɪʃn/", "part_of_speech": "noun", "example": "We reached our destination.", "category": "travel", "difficulty": 2},
    {"english": "itinerary", "chinese": "行程表；旅行计划", "phonetic": "/aɪˈtɪnəreri/", "part_of_speech": "noun", "example": "Here is our itinerary.", "category": "travel", "difficulty": 3},
    {"english": "luggage", "chinese": "行李", "phonetic": "/ˈlʌɡɪdʒ/", "part_of_speech": "noun", "example": "I have two pieces of luggage.", "category": "travel", "difficulty": 1},
    {"english": "passport", "chinese": "护照", "phonetic": "/ˈpæspɔːrt/", "part_of_speech": "noun", "example": "Don't forget your passport.", "category": "travel", "difficulty": 1},
    {"english": "reservation", "chinese": "预订；预约", "phonetic": "/ˌrezərˈveɪʃn/", "part_of_speech": "noun", "example": "I have a reservation.", "category": "travel", "difficulty": 2},
    {"english": "sightseeing", "chinese": "观光；游览", "phonetic": "/ˈsaɪtsiːɪŋ/", "part_of_speech": "noun", "example": "We went sightseeing all day.", "category": "travel", "difficulty": 2},
]


class Command(BaseCommand):
    help = '初始化英文单词数据'

    def handle(self, *args, **options):
        created_count = 0
        for word_data in INITIAL_WORDS:
            _, created = Word.objects.get_or_create(
                english=word_data['english'],
                defaults=word_data
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'成功初始化 {created_count} 个新单词（共 {len(INITIAL_WORDS)} 个）'))
