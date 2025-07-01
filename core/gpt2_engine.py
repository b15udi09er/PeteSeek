from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class GPT2Engine:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        
    def generate(self, prompt):
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=150, do_sample=True)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)