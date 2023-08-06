def setup_model():

    set_seed(424242)

    title = input("Enter the title of your article: ")
    print("\n")
    prompt = input("Enter the promt you wish for the article: ")
    formatted_prompt = prompt.format()

    MAX_LENGTH = int(input("Enter the maximum number of words you'd like in your content: "))
    print("\n")

    input_ids = tokenizer(formatted_prompt, return_tensors="pt").to(0)


def generate_text():
    print("\n")
    sample = model.generate(**input_ids, max_length=length,  num_beams = 2, num_beam_groups = 2, top_k=1, temperature=1.5, repetition_penalty = 3.0, diversity_penalty = 1.2)
    str(tokenizer.decode(sample[0]))
    # print(tokenizer.decode(sample[0], truncate_before_pattern=[r"\n\n^#", "^'''", "\n\n\n"]))

def run():
    setup_model()
  
    generate_text()


    filename = title + ".txt"



    with open(filename, "w") as f:
      f.close()

    location = '/content/'+title+'.txt'

    with open(filename, "a") as f:

      if os.stat(location).st_size == 0:
        print('File is empty')
        f.write('\n'+str(tokenizer.decode(sample[0])).replace('</s>', ''))
      else:
        print('File is not empty')
        print("\n")
        f.write('\n'+str(tokenizer.decode(sample[0])).replace('</s>', ''))
      f.close()

    print("\n\n")
    print(str(tokenizer.decode(sample[0])).replace('</s>', ''))


    files.download(location)

