import openai
from setup import load_credentials


credentials = load_credentials()
openai.api_key = credentials['openai_secret_key']


def analyze_github_comments():
    try:
        with open('text/pull_comments.txt', 'r') as file:
            allComments = file.read().replace('\n', ' ')
        comments = chunk_text_by_words(allComments)    
    except Exception as e:
        print(f"Error reading comments: {e}")
        exit(1)
    try:
        with open('text/feedback.txt', 'w') as file:
            file.write('')
    except Exception as e:
        print(f"Error cleaning cleanup document: {e}")
        exit(1)
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
            output.append(response['choices'][0]['message']['content'] + '\n')
        except Exception as e:
            print(f"Error processing comments: {e}")
    try:
        for outputChunk in output:
            if outputChunk is not None:
                with open('text/feedback.txt', 'a') as file:
                    file.write(outputChunk+ '\n')
    except Exception as e:
        print(f"Error writing feedback.txt: {e}")
        exit(1)
    return



def summarize_feedback():
    try:
        with open('text/feedback.txt', 'r') as file:
                feedback_content = file.read().replace('\n', ' ')
                feedback_array = chunk_text_by_words(feedback_content)
    except Exception as e:
        print(f"Error reading comments: {e}")
        exit(1)
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

    try:
        with open('text/summary.txt', 'w') as file:
            file.write(response['choices'][0]['message']['content'] + '\n')
    except Exception as e:
        print(f"Error writing summary.txt: {e}")
        exit(1)
    print('complete')
    return



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
