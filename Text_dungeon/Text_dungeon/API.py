import shutil
import replicate
import requests
import openai
import os


def threading_api_calls(queue, previous_text):
    try:
        prompt = queue.get()
        print(f"thread got prompt {prompt}")
        queue.task_done()
        output = generate_text(prompt, previous_text)
        generate_image(output)
    # call the open ai with text input
    # get the text from open ai
    # feed it to generate_image(prompt)
        queue.put(True)
        queue.put(output)
    except Exception as e:
        # put exception in queue
        queue.put(e.__str__())

def generate_image(prompt):
        img_file = os.getcwd() + '\\image'
        client = replicate.Client(api_token="60a8e5a0df9ec55d351a5a0d33f8e2b37f42e810")
        model = client.models.get("stability-ai/stable-diffusion")

        crash_count = 0
        working_image = False
        while crash_count < 5 and not working_image:
            try:
                output = model.predict(prompt=prompt)
                working_image = True
            except Exception as e:
                print(f"AI api crashed: {e}")
                crash_count += 1
        if not working_image:
            raise Exception("API is crashing consistently, prompt too nsfw or token exhausted")
        res  = requests.get(output[0], stream = True)
        if res.status_code == 200:
            with open(f'{img_file}\\main.png', 'wb') as f:
                #change where image gets saved to.
                shutil.copyfileobj(res.raw, f)
                print(f'{prompt} image generated')
        else:
            print('Image could not be downloaded')

def generate_text(prompt, previous_text):
    openai.organization = "org-8ARA7uqgkWLwELOKOsMBZLHD"
    openai.api_key = "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"
    text = prompt
    if previous_text == "":
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Human : {text} ",
            temperature=0.9,
            max_tokens=300,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"],
        )
        return response["choices"][0]["text"]
    else:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"""AI: {previous_text}
                    Human: {prompt}""",
            temperature=0.9,
            max_tokens=300,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"],
        )
        return response["choices"][0]["text"]