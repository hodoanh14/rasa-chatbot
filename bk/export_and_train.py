import os
import yaml
import mysql.connector
import subprocess
from collections import defaultdict

# Intent mặc định và nội dung tương ứng nếu thiếu
default_intents = {
    "greet": {
        "examples": ["xin chào", "chào bạn", "hello", "hi"],
        "responses": ["Chào bạn! Tôi có thể giúp gì?"]
    },
    "goodbye": {
        "examples": ["tạm biệt", "bye", "hẹn gặp lại"],
        "responses": ["Tạm biệt! Hẹn gặp lại sau nhé."]
    },
    "bot_challenge": {
        "examples": ["bạn là ai", "bạn có phải là bot không", "bạn được tạo bởi ai"],
        "responses": ["Tôi là một trợ lý ảo được tạo bởi AI."]
    }
}

# Kết nối MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="rasa_chatbot"
)
cursor = db.cursor(dictionary=True)

# Truy vấn dữ liệu
cursor.execute("SELECT * FROM intents ORDER BY created_at DESC")
rows = cursor.fetchall()

# Gom dữ liệu
intents_examples = defaultdict(list)
intent_responses = defaultdict(list)

for row in rows:
    intent = row['intent']
    example = row['example']
    response = row['response']
    if example:
        intents_examples[intent].append(example.strip())
    if response:
        intent_responses[intent].append(response.strip())

# Thêm intent mặc định nếu chưa có trong MySQL
for intent, content in default_intents.items():
    if intent not in intents_examples:
        print(f"⚠️ Thêm intent mặc định: {intent}")
        intents_examples[intent] = content['examples']
        intent_responses[intent] = content['responses']

# Xoá các file YAML cũ
for file in ['data/nlu.yml', 'domain.yml', 'data/stories.yml', 'data/rules.yml']:
    try:
        os.remove(file)
        print(f"🧹 Đã xoá: {file}")
    except FileNotFoundError:
        pass

# Ghi file NLU
nlu_data = {'version': '3.1', 'nlu': []}
for intent, examples in intents_examples.items():
    examples_text = "\n".join([f"- {e}" for e in examples])
    nlu_data['nlu'].append({'intent': intent, 'examples': examples_text})
with open('data/nlu.yml', 'w', encoding='utf-8') as f:
    yaml.dump(nlu_data, f, allow_unicode=True)
print("✅ Đã ghi file: data/nlu.yml")

# Ghi file domain
domain = {
    'version': '3.1',
    'intents': list(intents_examples.keys()),
    'responses': {},
    'actions': []
}
for intent, responses in intent_responses.items():
    domain['responses'][f"utter_{intent}"] = [{"text": r} for r in responses]
with open('domain.yml', 'w', encoding='utf-8') as f:
    yaml.dump(domain, f, allow_unicode=True)
print("✅ Đã ghi file: domain.yml")

# Ghi file stories
stories = {
    'version': '3.1',
    'stories': []
}
for intent in intents_examples:
    story = {
        'story': f"story_{intent}",
        'steps': [
            {'intent': intent},
            {'action': f"utter_{intent}"}
        ]
    }
    stories['stories'].append(story)
with open('data/stories.yml', 'w', encoding='utf-8') as f:
    yaml.dump(stories, f, allow_unicode=True)
print("✅ Đã ghi file: data/stories.yml")

# Ghi file rules.yml
rules = {
    'version': '3.1',
    'rules': []
}
for intent in intents_examples:
    rule = {
        'rule': f"rule_{intent}",
        'steps': [
            {'intent': intent},
            {'action': f"utter_{intent}"}
        ]
    }
    rules['rules'].append(rule)
with open('data/rules.yml', 'w', encoding='utf-8') as f:
    yaml.dump(rules, f, allow_unicode=True)
print("✅ Đã ghi file: data/rules.yml")

# Train Rasa
print("📦 Export hoàn tất. Đang chạy 'rasa train'...")
try:
    subprocess.run(['rasa', 'train'], check=True)
except subprocess.CalledProcessError as e:
    print(f"❌ Lỗi khi train Rasa: {e}")
