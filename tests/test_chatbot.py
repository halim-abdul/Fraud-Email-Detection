from fraud_email.chatbot import answer
from fraud_email.schemas import EmailInput

def test_chat_never_executes_reply():
    e=EmailInput(subject="Lottery winner",body="You won money; send funds immediately")
    result=answer(e,"Please reply")
    assert result["review_required"] and not result["action_executed"]
    assert "Do not automatically reply" in result["answer"]
