def load_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
    import torch
    import os
    from google.colab import files

  torch.set_default_tensor_type(torch.cuda.FloatTensor)
  the_model_repo_address = str(input("Enter the address for Model Repo from Huggingface: "))
  print("\n")

model = AutoModelForCausalLM.from_pretrained(the_model_repo_address, use_cache=True)
tokenizer = AutoTokenizer.from_pretrained(the_model_repo_address)
