import re
from PyPDF2 import PdfReader

# Define the keywords for each sub-criterion
CRITERIA_KEYWORDS = {
    'Approach': {
        'Novel': ['novel', 'innovative'],
        'Modify': ['modify', 'adapt']
    },
    'Method': {
        'Experimental': ['experiment', 'testing'],
        'Development': ['development', 'build']
    },
    'Development': {
        'Assessment': ['assessment', 'evaluation'],
        'Integrated to platform technology': ['platform', 'technology integration'],
        'Comparative': ['compare', 'comparison']
    },
    'Type': {
        'Process': ['process', 'procedure'],
        'Product': ['product', 'solution']
    },
    'Client Base': {
        'Yes': ['client', 'customer'],
        'No': []  # No keywords needed for "No"
    }
}

SECTIONS = ['Title', 'Objectives', 'Scope and Limitations']

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text.lower()

def analyze_sub_criteria(text, keywords):
    if not keywords:
        return 0
    count = sum(1 for keyword in keywords if re.search(rf'\b{keyword}\b', text))
    return (count / len(keywords)) * 100 if keywords else 0

def analyze_pdf(filepath):
    text = extract_text_from_pdf(filepath)
    results = {criterion: {sub: {section: 0 for section in SECTIONS} for sub in sub_criteria}
               for criterion, sub_criteria in CRITERIA_KEYWORDS.items()}

    # Analyze the text for each sub-criterion in each section
    for criterion, sub_criteria in CRITERIA_KEYWORDS.items():
        for sub_criterion, keywords in sub_criteria.items():
            for section in SECTIONS:
                results[criterion][sub_criterion][section] = analyze_sub_criteria(text, keywords)

    # Calculate Subtotals per sub-criterion
    subtotals = {
        criterion: {
            sub_criterion: sum(results[criterion][sub_criterion].values()) / 3
            for sub_criterion in sub_criteria
        }
        for criterion, sub_criteria in CRITERIA_KEYWORDS.items()
    }

    # Overall total is the sum of all sub-criterion subtotals divided by 11
    overall_total = sum(
        sum(subtotals[criterion].values()) for criterion in subtotals
    ) / 11

    interpretation = interpret_score(overall_total)

    return {
        'section_scores': results,
        'subtotals': subtotals,
        'overall_total': overall_total,
        'interpretation': interpretation
    }

def interpret_score(score):
    if 50 <= score <= 59:
        return "Minimal Alignment"
    elif 60 <= score <= 69:
        return "Basic Alignment"
    elif 70 <= score <= 79:
        return "Moderate Alignment"
    elif 80 <= score <= 89:
        return "Strong Alignment"
    elif 90 <= score <= 99:
        return "Very Strong Alignment"
    elif score == 100:
        return "Full Alignment"
    return "No Alignment"
