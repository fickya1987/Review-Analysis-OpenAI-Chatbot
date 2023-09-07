import streamlit as st
import openai
import json

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"


def analyze_review(review_text):
    try:
        prompt = f"""
                You are an expert customer review analyst. \
                Analyze the following customer review delimited by triple backticks \
                extract the following details from the review in a JSON Object response \
                1 - Item / Product \
                2 - Company / Manufacturer \
                3 - Review (One Word) \
                4 - Rating (1 to 10) \
                5 - Satisfactory Score (1 to 10) \
                6 - User Mood \

                JSON object structure \
                {{
                  "item": "",
                  "company": "",
                  "user_mood": "",
                  "review": "",
                  "rating": "",
                  "satisfactory_score": "",
                }}

                Review:
                ```
                {review_text}
                ```
        """

        messages = [{"role": "system", "content": "You are an expert customer support analyst that analyzes the "
                                                  "reviews and feedback of the customer"},
                    {"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )

        # Extracting relevant information from the GPT-3 response
        analyzed_data = json.loads(response.choices[0].text)

        return analyzed_data
    except Exception as e:
        st.error(f"Error analyzing the review: {str(e)}")
        return None


def main():
    st.title("Review Analyzing App")

    # User input for review
    user_review = st.text_area("Enter your review here:")

    if st.button("Analyze Review"):
        if user_review:
            analyzed_data = analyze_review(user_review)
            if analyzed_data:
                st.subheader("Analysis Results:")
                st.write(f"Item: {analyzed_data['item']}")
                st.write(f"Company: {analyzed_data['company']}")
                st.write(f"Review: {analyzed_data['review']}")
                st.write(f"Rating (1-10): {analyzed_data['rating']}")
                st.write(f"Satisfactory Score (1-10): {analyzed_data['satisfactory_score']}")
                st.write(f"User Mood: {analyzed_data['user_mood']}")
        else:
            st.warning("Please enter a review for analysis.")


if __name__ == "__main__":
    main()
