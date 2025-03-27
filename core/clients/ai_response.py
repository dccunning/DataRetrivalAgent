from core.utils.ai_model import AIModel


class AIResponseClient:
    """Get a response from an AI model"""

    def __init__(self, model: AIModel, system_message: str = ""):
        self.model = model
        self.system_message = system_message

    def one_shot(self, content: str) -> str:
        """One shot AI response with system message"""
        response = self.model.client().chat.completions.create(
            model=self.model.name,
            messages=[
                {'role': 'system', 'content': self.system_message},
                {'role': 'user', 'content': content}
            ],
        )
        return response.choices[0].message.content
