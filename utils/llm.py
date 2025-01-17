import anthropic

import openai

def summarize_with_anthropic(text_chunk, instructions):
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{instructions} {text_chunk}"
                    }
                ]
            }
        ]
    )
    
    return message.content[0].text

def summarize_with_openai(text_chunk, instructions):
    client = openai.OpenAI()

    chat_completion = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
            {
                "role": "user",
                "content": f"{instructions} {text_chunk}"
            }
        ]
    )

    return chat_completion.choices[0].message.content
    
    
def summarize_with_llm(llm_name, text_chunk, instructions):
    if llm_name == 'Claude 3':
        return summarize_with_anthropic(text_chunk, instructions)
    elif llm_name == 'GPT-4':
        return summarize_with_openai(text_chunk, instructions)
    else:
        return f"model '{llm_name}' not found"
        
