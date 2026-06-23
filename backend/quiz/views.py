import random
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vocabulary.models import Word, UserWord
from .models import QuizRecord, QuizDetail
from .serializers import (
    GenerateQuizSerializer, QuizRecordListSerializer, QuizRecordSerializer
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_quiz(request):
    """生成测验题目"""
    serializer = GenerateQuizSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    quiz_type = serializer.validated_data['quiz_type']
    question_count = serializer.validated_data['question_count']
    category = serializer.validated_data.get('category', '')
    difficulty = serializer.validated_data.get('difficulty')

    # 查询单词
    words_qs = Word.objects.all()
    if category:
        words_qs = words_qs.filter(category=category)
    if difficulty:
        words_qs = words_qs.filter(difficulty=difficulty)

    words = list(words_qs)
    if len(words) < question_count:
        question_count = len(words)
    if question_count == 0:
        return Response({'error': '没有足够的单词'}, status=status.HTTP_400_BAD_REQUEST)

    selected_words = random.sample(words, question_count)

    # 生成题目
    questions = []
    for i, word in enumerate(selected_words):
        if quiz_type == 'choice':
            question = _generate_choice_question(word, words, i)
        elif quiz_type == 'spelling':
            question = _generate_spelling_question(word, i)
        else:
            question = _generate_listening_question(word, i)
        questions.append(question)

    return Response({
        'quiz_type': quiz_type,
        'questions': questions,
        'total_questions': len(questions)
    })


def _generate_choice_question(word, all_words, index):
    """生成选择题"""
    is_en_to_cn = random.choice([True, False])
    # 生成干扰选项
    other_words = [w for w in all_words if w.id != word.id]
    distractors = random.sample(other_words, min(3, len(other_words)))

    if is_en_to_cn:
        question_text = f'"{word.english}" 的中文意思是？'
        correct = word.chinese
        options = [correct] + [w.chinese for w in distractors]
    else:
        question_text = f'"{word.chinese}" 的英文是？'
        correct = word.english
        options = [correct] + [w.english for w in distractors]

    random.shuffle(options)
    return {
        'id': index + 1,
        'word_id': word.id,
        'question': question_text,
        'question_type': 'choice',
        'options': options,
        'correct_answer': correct
    }


def _generate_spelling_question(word, index):
    """生成拼写题（看中文写英文）"""
    return {
        'id': index + 1,
        'word_id': word.id,
        'question': f'请写出"{word.chinese}"对应的英文单词',
        'question_type': 'spelling',
        'hint': word.example if word.example else '',
        'correct_answer': word.english
    }


def _generate_listening_question(word, index):
    """生成英译中题"""
    return {
        'id': index + 1,
        'word_id': word.id,
        'question': f'请写出"{word.english}"的中文意思',
        'question_type': 'listening',
        'hint': word.example if word.example else '',
        'correct_answer': word.chinese
    }


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request):
    """提交测验答案"""
    quiz_type = request.data.get('quiz_type', 'choice')
    total_questions = request.data.get('total_questions', 0)
    answers_data = request.data.get('answers', [])
    questions_data = request.data.get('questions', [])

    if not answers_data:
        return Response({'error': '请提交答案'}, status=status.HTTP_400_BAD_REQUEST)

    # 创建问题字典方便查找
    question_map = {q['id']: q for q in questions_data}

    # 创建测验记录
    quiz_record = QuizRecord.objects.create(
        user=request.user,
        quiz_type=quiz_type,
        total_questions=total_questions,
        correct_answers=0,
        score=0
    )

    details = []
    correct_count = 0

    for ans in answers_data:
        q_data = question_map.get(ans.get('question_id'), {})
        is_correct = ans.get('answer', '').strip().lower() == q_data.get('correct_answer', '').strip().lower()

        if is_correct:
            correct_count += 1

        detail = QuizDetail.objects.create(
            quiz_record=quiz_record,
            word_id=q_data.get('word_id', 0),
            question=q_data.get('question', ''),
            correct_answer=q_data.get('correct_answer', ''),
            user_answer=ans.get('answer', ''),
            is_correct=is_correct
        )
        details.append(detail)

        # 更新用户单词练习记录
        word_id = q_data.get('word_id', 0)
        if word_id:
            try:
                word = Word.objects.get(id=word_id)
                user_word, _ = UserWord.objects.get_or_create(user=request.user, word=word)
                user_word.practice_count += 1
                if is_correct:
                    user_word.correct_count += 1
                user_word.save()
            except Word.DoesNotExist:
                pass

    # 更新测验记录
    score = round((correct_count / total_questions) * 100, 1) if total_questions > 0 else 0
    quiz_record.correct_answers = correct_count
    quiz_record.score = score
    quiz_record.save()

    return Response(QuizRecordSerializer(quiz_record).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_history(request):
    """获取测验历史"""
    records = QuizRecord.objects.filter(user=request.user).order_by('-completed_at')
    data = QuizRecordListSerializer(records, many=True).data
    return Response({
        'count': records.count(),
        'results': data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_detail(request, pk):
    """获取测验详情"""
    record = QuizRecord.objects.filter(id=pk, user=request.user).first()
    if not record:
        return Response({'error': '记录不存在'}, status=status.HTTP_404_NOT_FOUND)
    return Response(QuizRecordSerializer(record).data)
