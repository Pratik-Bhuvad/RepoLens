from .constants import STACK_TOKENS

def classify_query_stack(query):
    query = query.lower().split()
    
    stack_qualifiers = []
    concept_tokens = []
    
    for token in query:
        if token in STACK_TOKENS:
            stack_qualifiers.append(STACK_TOKENS[token])
        else:
            concept_tokens.append(token)
            
    return stack_qualifiers, concept_tokens