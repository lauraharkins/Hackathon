from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, pipeline
import random

def clean_level(level):
    lines = level.split("\n")
    output = []
    for line in lines:
        temp = line
        if len(line) > 16:
            temp = temp.replace(" ","",len(temp)-16)
        if len(line) < 16:
            temp = temp.replace(" ","  ",16-len(temp))
        chars = list(temp)
        chars[0] = "#"
        chars[-1] = "#"
        output.append(chars)
    return output

def generate_text(prompt="LevelSchematic:"):
    model = AutoModelForCausalLM.from_pretrained("./results/checkpoint-2500")
    model.cuda()
    
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2",padding_side="right")
    tokenizer.pad_token = tokenizer.eos_token
    
    generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
    level = generator("LevelSchematic:", max_length=256, num_return_sequences=1)
    return level[0]['generated_text']
    
def generate_level():
    text = generate_text()
    return clean_level(text.lstrip("LevelSchematic:"))

if __name__ == "__main__":
    prompt = input("Model Prompt: ")
    text = generate_text(prompt)
    print("Generated Text")
    print(text+"\n")
    if prompt == "LevelSchematic:":
        level = clean_level(text.lstrip("LevelSchematic:"))
        text_output = ""
        for line in level:
            text_output += "".join(line) + "\n"
        print("Cleaned Level")
        print(text_output)