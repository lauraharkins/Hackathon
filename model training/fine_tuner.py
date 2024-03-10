from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("distilgpt2",padding_side="right")
tokenizer.pad_token = tokenizer.eos_token

from transformers import AutoModelForCausalLM, TrainingArguments, Trainer
model = AutoModelForCausalLM.from_pretrained("distilgpt2")
model.cuda()
level_dataset = []
with open(input("Level file"),"r") as file:
    level_data = "LevelSchematic:" + file.readline()
    i = 1
    while level_data != "LevelSchematic:":
        if (i<16):
            level_data += file.readline()
            i+=1
        else:
            level_dataset.append({"schem":level_data.rstrip("\n")})
            level_data = "LevelSchematic:" + file.readline()
            i=1
import datasets

level_Dataset = datasets.Dataset.from_list(level_dataset)

def preprocess_function(examples):
    result = tokenizer(examples["schem"],padding="max_length",max_length=256)
    result['labels'] = result['input_ids'].copy()
    return result

tokenized_dataset = level_Dataset.map(
    preprocess_function,
    remove_columns=["schem"]
)

training_args = TrainingArguments(
    num_train_epochs=100,
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset
)

trainer.train()
prompt = "LevelSchematic:"

from transformers import pipeline, set_seed
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
results = generator(prompt, max_length=256, num_return_sequences=5)
for result in results:
    print(result['generated_text'].lstrip("LevelSchematic:"))
    print("\n\n")
