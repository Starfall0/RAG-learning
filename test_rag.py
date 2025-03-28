from query_data import query_rag
from langchain_openai import ChatOpenAI

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""
###
# use pytest to run the tests
# $ pytest test_rag.py -s
###

def test_monopoly_rules():
    assert query_and_validate(
        question="How much total money does a player start with in classic Monopoly? (Answer with the number only)",
        expected_response="$1500",
    )

def test_monopoly_rules_negative():
    assert not query_and_validate(
        question="How much total money does a player start with in classic Monopoly? (Answer with the number only)",
        expected_response="$9999",
    )

def test_ticket_to_ride_rules():
    assert query_and_validate(
        question="How many points does the longest continuous train get in Ticket to Ride? (Answer with the number only)",
        expected_response="10 points",
    )


def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="your-api-key",
        model="mistral-7b-instruct-v0.3",
        temperature=0
    )
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.content.strip().lower()

    # print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )
