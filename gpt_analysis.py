import openai

def analyze_github_comments(credentials, comments):
    openai.api_key = credentials['openai_secret_key']
    print('analyzing comments')
    output = []
    for comment_chunk in comments:
        conversation = [
            {
                "role": "system",
                "content": "You are a helpful assistant that analyzes GitHub comments, and provides feedback. you respond with a sentence followed by bullet points"
            },
            {
                "role": "user",
                "content": f"Please read the following GitHub comments and analyze what types of mistakes the programmer tends to make: '{comment_chunk}'. Pay special attention to programming errors/mistakes. if you don't see patterns return an empty response. Take your time to think, then list the feedback."
            },
        ]
        try: 
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
            output.append(response['choices'][0]['message']['content'])
        except Exception as e:
            print(f"Error processing comments: {e}")
    return "\n".join(output)

def summarize_feedback(credentials, feedback):
    openai.api_key = credentials['openai_secret_key']
    feedback_array = chunk_text_by_words(feedback)
    print('summarizing feedback')
    conversation = [
    {
        "role": "system",
        "content": "You are a programming instructor that summarizes feedback comments."
    },
    {
        "role": "user",
        "content": f"Please summarize the following feedback using upto 10 key points: '{feedback_array[0]}'"
    },
]
    try: 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
    except Exception as e:
        print(f"Error summarizing feedback: {e}")
        exit(1)
    summary = response['choices'][0]['message']['content']
    return summary

def chunk_text_by_words(text, max_words=500):
    words = text.split(' ')
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]



# tokenizer approach for long files
# def chunk_text(text, max_length=4000):
#     tokens = openai.tokenizer.encode(text)
#     chunks = []
#     current_chunk = []
#     for token in tokens:
#         if len(current_chunk) + 1 > max_length:
#             chunks.append(openai.tokenizer.decode(current_chunk))
#             current_chunk = [token]
#         else:
#             current_chunk.append(token)

#     if current_chunk:
#         chunks.append(openai.tokenizer.decode(current_chunk))
#     return chunks
