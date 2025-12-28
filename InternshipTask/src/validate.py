import re

def should_abstain(retrieved,min_simmilarity):
    if not retrieved:
        return True
    top_score = retrieved[0][1]
    return top_score < min_simmilarity

# extract all allowed arrticle references
def allowed_citations(retrieved):

    allowed = set()
    for c, _ in retrieved:
        article = c['article']
        allowed.add(article)

        # Also add variants
        # "მუხლი 18" must match "მუხლი 18, პ.2"
        article_num = re.search(r'მუხლი\s+(\d+)', article)
        if article_num:
            allowed.add(f"მუხლი {article_num.group(1)}")

    return allowed

# validate citations and add warnings for hallucinations (this was a big issue here)
def validate_answer(answer, allowed_articles):

    # Find all article mentions in answer
    mentioned = set(re.findall(r"მუხლი\s+\d+", answer))

    # Check which ones are not valid
    bad = []
    for m in mentioned:
        # Check if this article or any variant is in allowed
        if m not in allowed_articles:
            # check whether the base article number is in allowed
            num = re.search(r'\d+', m).group()
            if not any(f"მუხლი {num}" in a for a in allowed_articles):
                bad.append(m)

    if not bad:
        return answer

    warning = (
        f"\n\nგაფრთხილება\n"
        f"პასუხში მოხსენიებულია მუხლები, რომლებიც მოძიებულ კონტექსტში არ ფიქსირდება:\n"
        f"{', '.join(bad)}\n"
        f"ეს ნაწილი არ არის დადასტურებული და შეიძლება იყოს არასწორი!"
    )
    return answer + warning


def check_answer_quality(answer, question, context):


    # Check for abstain message
    abstain_phrases = [
        "მოცემული ამონარიდებით ზუსტი პასუხი ვერ დასტურდება",
        "კონტექსტში არ არის",
        "არ არის საკმარისი ინფორმაცია"
    ]

    for phrase in abstain_phrases:
        if phrase in answer:
            return answer




    # Check if answer has citations
    citations = re.findall(r"მუხლი\s+\d+", answer)
    if not citations and len(context) > 100:
        return answer + "\n\nპასუხი არ შეიცავს ციტირებებს კონტექსტიდან."

    return answer