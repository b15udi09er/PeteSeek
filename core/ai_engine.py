# /opt/peteseek/core/ai_engine.py
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class PeteAI:
    def __init__(self):
        """Loads GPT-2 once (shared across all requests)."""
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
    
    def generate(self, prompt, max_length=150, temperature=0.9):
        """Generate unfiltered text with adjustable chaos."""
        clean_prompt = prompt.replace("@PeteSeek", "").strip()
        
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs,
            max_length=max_length,
            do_sample=True,
            temperature=temperature,  # 0.7-1.3: higher = crazier
            top_k=50,
            top_p=0.95,
            pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)