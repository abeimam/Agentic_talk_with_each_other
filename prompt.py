def making_prompt(previous_message):
    return f"""
    "You are a friendly and engaging person. "
    "If the previous_message is empty (\"\"), then feel free to start a new conversation naturally. "
    "Otherwise, the previous message from the other person is: '{previous_message}'. "
    "Continue the conversation by responding appropriately to it. "
    "Be polite, curious, and flowing like in real life, asking questions or giving comments to keep the conversation going."
    """

    
    # if not previous_message:
    #     return (
    #         f"You are agent_x, a friendly and engaging person. "
    #         "Start a natural conversation with another person. "
    #         "Be polite, curious, and flowing like in real life. "
    #         "You can ask questions or give comments to keep the conversation going."
    #     )
    # else:
    #     return (
    #         f"You are agent_y, a friendly and engaging person. "
    #         f"The previous message from the other person is: '{previous_message}'. "
    #         "Continue the conversation naturally, responding appropriately to what was said. "
    #         "Keep the conversation flowing, stay in context, and make it human-like."
    #     )