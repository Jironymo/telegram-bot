def sample_responses(input_text):
    user_message = str(input_text).lower().strip()

    if user_message in ('привет', 'hello', 'hi', 'hey'):
        return "Heeey! How ya doin?"

    if user_message in ("что ты умеешь?", "what can you do?"):
        return "Limitless possibilities I have within the reach of my power... Only left to take it!"

    return "I don't understand you. = ("
