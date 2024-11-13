# src/llm.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List, Dict

class LLMHandler:
    def __init__(self):
        """Initialize the LLM."""
        # Load model and tokenizer
        self.model_name = "./TinyLlama-1.1B-Chat-v1.0"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            low_cpu_mem_usage=True
        )
        
        if torch.cuda.is_available():
            self.model = self.model.cuda()

    def generate_response(self, query: str, context: List[Dict]) -> str:
        """Generate a response based on the query and context."""
        try:
            # Prepare context from retrieved documents
            context_text = "\n\n".join([
                f"Document {i+1} ({doc['metadata']['source']}):\n{doc['content']}"
                for i, doc in enumerate(context)
            ])

            # Create prompt
            prompt = f"""<|system|>You are a helpful AI assistant that answers questions based on the provided context.
            
<|user|>Context information is below:
---------------------
{context_text}
---------------------

Based on the context information above, please answer this question: {query}

<|assistant|>"""

            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            if torch.cuda.is_available():
                inputs = inputs.to("cuda")

            # Generate response
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the assistant's response
            response = response.split("<|assistant|>")[-1].strip()
            
            return response

        except Exception as e:
            print(f"Error generating LLM response: {str(e)}")
            return "I apologize, but I encountered an error while generating the response."