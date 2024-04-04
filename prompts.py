'''
A set of supporting functions for making the interim prompts we use to 
generate a final engineered image prompt.
'''

# These constants are written this way for formatting purposes.
# We don't want a bunch of tab characters going to GPT.
SUBJECT_PROMPT = '''Create a detailed physical description of the following subject and setting in 150 words.

Subject: {}

Setting: {}
'''

STYLE_PROMPT = 'Create a 50 word summary of the visual aspects of the following artistic style: {}'

IMG_PROMPT_REQUEST = '''Write a prompt for an image generator using the following content and style in 200 words.

Image content: {}

Image Style: {}
'''


def fetch_scene_details(client, model, subject, setting):
    '''
    Use the supplied args and OpenAI client to fetch a more
    detailed description from OpenAI.

    client (OpenAI client) -- client makes the request
    model (str) -- a valid OpenAI API model string, e.g. 'gpt-4'
    subject (str) -- a string describing a subject in plain english, for LLM use.
    setting (str) -- a string describing a setting in plain english, for LLM use.
    '''
    prompt_content = SUBJECT_PROMPT.format(subject, setting)
    
    subject_response = client.chat.completions.create(
        model=model,
        messages=[
        {
            "role": "user",
            "content": prompt_content
        }],
        temperature=1,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    subject_details = subject_response.choices[0].message.content
    
    return subject_details



def fetch_style_detail(client, model, style):
    '''
    Use the supplied args and OpenAI client to fetch a more
    detailed description of the art style from OpenAI.

    client (OpenAI client) -- client makes the request
    model (str) -- a valid OpenAI API model string, e.g. 'gpt-4'
    style (str) -- a string describing a subject in plain english, for LLM use.
    '''
    prompt_content = STYLE_PROMPT.format(style)
    
    style_response = client.chat.completions.create(
        model=model,
        messages=[
        {
            "role": "user",
            "content": prompt_content
        }],
        temperature=1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    style_details = style_response.choices[0].message.content

    return style_details


def fetch_dalle_prompt(client, model, image_content_description, image_style_details):
    '''
    Use the supplied args and OpenAI client to fetch a more
    detailed description of the art style from OpenAI.

    client (OpenAI client) -- client makes the request
    model (str) -- a valid OpenAI API model string, e.g. 'gpt-4'
    image_content_description (str) -- a string describing a subject in plain english, for LLM use.
    image_style_details (str) -- a string describing an art style in plain english, for LLM use.
    '''
    prompt_content = IMG_PROMPT_REQUEST.format(image_content_description, image_style_details)

    image_prompt_response = client.chat.completions.create(
        model=model,
        messages=[
        {
            "role": "user",
            "content": prompt_content
        }],
        temperature=1,
        max_tokens=700,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    generated_image_prompt = image_prompt_response.choices[0].message.content
    
    return generated_image_prompt