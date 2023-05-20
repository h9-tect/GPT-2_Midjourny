import streamlit as st
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import replicate
import os

def generate_stories(prompt):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids, max_length=200, num_return_sequences=3, do_sample=True, top_k=50, top_p=0.95, temperature=1.1)
    stories = [tokenizer.decode(sequence, skip_special_tokens=True) for sequence in output]

    api_token = "add_your_token_here"
    os.environ["REPLICATE_API_TOKEN"] = api_token

    for i, story in enumerate(stories):
        output = replicate.run(
            "tstramer/midjourney-diffusion:436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b",
            input={"prompt": story}
        )
        st.write("Story", i+1, ":")
        st.write(story)
        st.write("\nOutput Text:")
        st.write(output)
        st.write("\n---\n")

prompt = st.text_input("Enter a prompt for the model: ")
if prompt:
    generate_stories(prompt)
