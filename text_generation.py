import os
import json
from openai import OpenAI
from config import SYSTEM_PROMPT_PATH

class Bot:
    def __init__(self, client: OpenAI, memory_file='bot_memory.json'):
        self.client = client
        self.memory_file = memory_file
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {'history': []}
        else:
            return {'history': []}

    def save_memory(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=4)

    def update_memory(self, user_message: str, bot_response: str):
        if 'history' not in self.memory:
            self.memory['history'] = []
        self.memory['history'].append({
            'user': user_message,
            'bot': bot_response
        })
        self.save_memory()

    def build_prompt(self, user_message: str, max_history=5):
        prompt = ''
        try:
            with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
                prompt += f.read().strip() + '\n'
        except FileNotFoundError:
            prompt += 'Default prompt header\n'

        if self.memory.get('history'):
            prompt += 'Last conversations:\n'
            for conv in self.memory['history'][-max_history:]:
                prompt += f'user: {conv['user']}\n'
                prompt += f'bot: {conv['bot']}\n'
            prompt += '\n'

        prompt += 'Main request:\n'
        prompt += f'user: {user_message}\n'
        prompt += 'bot: '
        return prompt

    def query(self, prompt):
        completion = self.client.chat.completions.create(
            extra_body={},
            model='google/gemini-2.0-flash-lite-preview-02-05:free',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        if completion.choices:
            return completion.choices[0].message.content
        else:
            return 'No response from API'

    def chat(self, user_message: str):
        prompt = self.build_prompt(user_message)
        bot_response = self.query(prompt)
        self.update_memory(user_message, bot_response)
        return bot_response