# EnglishGo 英文学习平台 - API 接口文档

## 基础信息
- **Base URL**: `http://localhost:8000/api/v1/`
- **认证方式**: JWT Bearer Token
- **Content-Type**: `application/json`
- **数据库**: MySQL 8 (`englishgo`)，Word 表约 15,000+ 条

---

## 一、用户认证接口

### 1.1 注册
```
POST /api/v1/auth/register/
```
**请求体:**
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "password2": "password123"
}
```
**响应:**
```json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "token": { "access": "...", "refresh": "..." }
}
```

### 1.2 登录
```
POST /api/v1/auth/login/
```
**请求体:**
```json
{ "username": "testuser", "password": "password123" }
```
**响应:** 同注册

### 1.3 刷新令牌
```
POST /api/v1/auth/refresh/
```
**请求体:**
```json
{ "refresh": "refresh_token_string" }
```

### 1.4 当前用户信息
```
GET /api/v1/auth/me/
```
**Header:** `Authorization: Bearer {access_token}`

---

## 二、词汇接口

### 2.1 获取词汇列表
```
GET /api/v1/vocabulary/words/
```
**Query 参数:**

| 参数 | 类型 | 可选值 / 说明 |
|------|------|--------------|
| category | string | ★ 考试：`junior`(初中) `senior`(高中) `cet4`(四级) `cet6`(六级) `postgraduate`(考研) `toefl`(托福) `sat`(SAT) <br> 难度：`basic` `intermediate` `advanced` `business` `travel` |
| difficulty | int | 1-5 |
| search | string | 英文/中文搜索 |
| page | int | 页码 |
| page_size | int | 每页数量（默认 20） |

**响应:**
```json
{
    "count": 15420,
    "next": "http://...?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "english": "abandon",
            "chinese": "放弃；抛弃",
            "phonetic": "",
            "part_of_speech": "verb",
            "example": "",
            "category": "cet4",
            "difficulty": 3,
            "created_at": "2024-01-01T00:00:00Z",
            "is_favorite": false,
            "mastered": false,
            "practice_count": 0,
            "correct_count": 0
        }
    ]
}
```

### 2.2 获取单词详情

```
GET /api/v1/vocabulary/words/{id}/
```
**响应:** 单个单词对象（同上 results 格式）

### 2.3 创建单词
```
POST /api/v1/vocabulary/words/
```
**请求体:**
```json
{
    "english": "abandon",
    "chinese": "放弃",
    "part_of_speech": "verb",
    "category": "cet4",
    "difficulty": 3
}
```

### 2.4 更新单词
```
PUT /api/v1/vocabulary/words/{id}/
```

### 2.5 删除单词
```
DELETE /api/v1/vocabulary/words/{id}/
```

### 2.6 切换收藏
```
POST /api/v1/vocabulary/words/{id}/toggle_favorite/
```
**响应:**
```json
{ "is_favorite": true }
```

### 2.7 标记掌握
```
POST /api/v1/vocabulary/words/{id}/mark_mastered/
```
**响应:**
```json
{ "mastered": true }
```

### 2.8 获取分类列表
```
GET /api/v1/vocabulary/categories/
```
**响应:**
```json
["junior","senior","cet4","cet6","postgraduate","toefl","sat","basic","intermediate","advanced","business","travel"]
```

### 2.9 获取收藏单词
```
GET /api/v1/vocabulary/favorites/
```

### 2.10 获取未掌握单词
```
GET /api/v1/vocabulary/unmastered/
```

---

## 三、测验接口

### 3.1 生成测验题目
```
POST /api/v1/quiz/generate/
```
**请求体:**
```json
{
    "quiz_type": "choice",
    "question_count": 10,
    "category": "cet4",
    "difficulty": null
}
```
**quiz_type:** `choice`(选择题) / `spelling`(拼写) / `listening`(英译中)

**category:** 可选值同词汇接口（junior/senior/cet4/cet6/postgraduate/toefl/sat/basic/...）

**响应:**
```json
{
    "quiz_id": 1,
    "quiz_type": "choice",
    "questions": [
        {
            "id": 1,
            "word_id": 5,
            "question": "abandon",
            "question_type": "en_to_cn",
            "options": ["放弃", "接受", "保持", "开始"],
            "correct_answer": "放弃"
        }
    ]
}
```

### 3.2 提交答案
```
POST /api/v1/quiz/{quiz_id}/submit/
```
**请求体:**
```json
{
    "answers": [
        {"question_id": 1, "answer": "放弃"},
        {"question_id": 2, "answer": "reject"}
    ]
}
```
**响应:**
```json
{
    "quiz_id": 1,
    "total_questions": 10,
    "correct_answers": 8,
    "score": 80.0,
    "details": [
        {
            "question_id": 1,
            "word": "abandon",
            "your_answer": "放弃",
            "correct_answer": "放弃",
            "is_correct": true
        }
    ]
}
```

### 3.3 测验历史
```
GET /api/v1/quiz/history/
```

### 3.4 测验详情
```
GET /api/v1/quiz/history/{id}/
```

---

## 四、学习进度接口

### 4.1 学习统计
```
GET /api/v1/progress/stats/
```
**响应:**
```json
{
    "total_words": 15420,
    "learned_words": 120,
    "mastered_words": 80,
    "total_quizzes": 15,
    "average_score": 78.5,
    "total_study_minutes": 320,
    "streak_days": 7
}
```

### 4.2 每日进度
```
GET /api/v1/progress/daily/?days=30
```

### 4.3 今日打卡
```
POST /api/v1/progress/checkin/
```

### 4.4 记录学习活动
```
POST /api/v1/progress/record_activity/
```
**请求体:**
```json
{ "words_learned": 5, "words_reviewed": 10, "study_minutes": 15 }
```

---

## 五、文章阅读接口

### 5.1 文章列表
```
GET /api/v1/articles/
```
**Query 参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码 |
| page_size | int | 每页数量 |
| level | string | beginner / intermediate / advanced |
| search | string | 标题/摘要搜索 |

### 5.2 文章详情
```
GET /api/v1/articles/{id}/
```
（阅读计数自动 +1）

### 5.3 难度列表
```
GET /api/v1/articles/levels/
```

---

## 六、错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 参数错误 |
| 401 | 未认证/令牌过期 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务端错误 |

错误格式：
```json
{ "error": "错误描述" }
```

---

## 七、管理命令

| 命令 | 说明 |
|------|------|
| `python manage.py seed_words` | 初始化 60 个基础词 |
| `python manage.py import_exam_words` | ★ 自动导入 7 个考试 SQL + 清洗 + 去重 + 写入 word 表 |
| `python manage.py import_exam_words --dry-run` | 仅统计预览，不写入 |
| `python manage.py import_exam_words --import-sql` | 强制重新导入 SQL 源表 |
