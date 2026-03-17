from groq_utility import generate_response
import streamlit as st

def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip()) == 0:
        return True
    t = text.strip()

    if t.endswith(('.', '!', '?', '"', "'", ')', ']', '}')):
        return False
    return True

def complete_answer(question: str, max_rounds: int = 2) -> str:
    base_prompt = (
        "You are a helpful assistant that provides detailed answers to questions. "
        "If your answer is incomplete, you will continue to generate more text until the answer is complete. "
        "An answer is considered complete if it ends with a full sentence or a closing punctuation mark "
        "(e.g., '.', '!', '?', '\"', \"'\", ')', ']', '}').\n\n"
        f"Question: {question}\n"
        "Answer:"
    )
    ans = generate_response(base_prompt, temperature=0.7)
    rounds = 0
    while rounds < max_rounds and looks_incomplete(ans):
        cont_prompt = (
            "The previous answer seems incomplete. Please continue the answer without repeating what has already been said. "
            "Do not add any introductory text, just continue from where it left off.\n\n"
            f"Question: {question}\n"
            f"Answer so far:\n{ans}\n\nContinue the answer:"
        )
        more = generate_response(cont_prompt, temperature=0.7)
        if not more or more.strip() in ans:
            break
        ans = (ans.rstrip() + "\n" + more.lstrip()).strip()
        rounds += 1
    return ans

def main():
    st.title("AI Teaching Assistant")
    st.write("Welcome to the AI Teaching Assistant! Ask any question, and I'll do my best to provide a detailed answer. If the answer seems incomplete, I'll continue to generate more information until it's complete.")
    user_input = st.text_input("Enter your question here:")

    if user_input:
        st.write(f"**Question:** {user_input}")
        answer = complete_answer(user_input)
        st.write(f"**Answer:** {answer}")
    else:
        st.info("Please enter a question to get started.")

if __name__ == "__main__":
    main()
