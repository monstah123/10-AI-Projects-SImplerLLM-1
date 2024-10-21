from SimplerLLM.language.llm import LLM, LLMProvider

llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-4o")

generated_text = llm_instance.generate_response(prompt="generate a sentence of 6 words about rain")

print(generated_text)

