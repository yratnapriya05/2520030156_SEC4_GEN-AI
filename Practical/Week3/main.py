
import time

from llm_client import LLMClient
from cost_calculator import calculate_cost
from mongo_logger import log_call, close_connection


def main():
    print("\n===== WEEK 3: LLM MONITORING =====")
    print("1. Gemini")
    print("2. Ollama")

    choice = input("\nSelect provider (1/2): ")

    if choice == "1":
        provider = "gemini"
    elif choice == "2":
        provider = "ollama"
    else:
        print("Invalid choice!")
        return

    prompt = input("\nEnter your prompt: ")

    try:
        client = LLMClient(provider)

        start_time = time.time()
        result = client.generate(prompt)
        latency = round(time.time() - start_time, 3)

        response = result["response"]
        model = result["model"]
        input_tokens = result["input_tokens"]
        output_tokens = result["output_tokens"]

        cost = calculate_cost(
            result["provider"],
            model,
            input_tokens,
            output_tokens
        )

        print("\n===== LLM RESPONSE =====")
        print(response)
        print("\n===== USAGE DETAILS =====")
        print("Provider:", result["provider"])
        print("Model:", model)
        print("Input Tokens:", input_tokens)
        print("Output Tokens:", output_tokens)
        print("Latency:", latency, "seconds")
        print("Estimated Cost:", cost)

        log_call(
            result["provider"],
            model,
            prompt,
            response,
            input_tokens,
            output_tokens,
            cost if cost is not None else 0.0
        )

        print("\nSuccessfully saved to MongoDB!")

    except Exception as e:
        print("\nError:", e)

    finally:
        close_connection()


if __name__ == "__main__":
    main()
