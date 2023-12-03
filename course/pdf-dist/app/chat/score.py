import random
from app.chat.redis import client


def random_component_by_score(component_type: str, component_map: dict) -> str:
    """
    Retrieves the scores for the specified component type from the langfuse client.
    It then randomly selects a component name based on the scores, with higher scores being more likely to be selected.

    :param component_type: The type of component to select a name for.
    :param component_map: The dictionary of component names to scores.

    :return: The name of the component selected.

    Example Usage:

        random_component_by_score('llm', {'chatopenai-3.5-turbo': 0.75, 'chatopenai-4': 0.25})
    """

    # Ensure component_type is "llm", "retriever", or "memory"
    if component_type not in ["llm", "retriever", "memory"]:
        raise ValueError(
            f"Invalid component type: {component_type}. Must be 'llm', 'retriever', or 'memory'."
        )

    # From Redis, get the hash containing the sum total scores for the given type
    values = client.hgetall(f"{component_type}_score_values")

    # From Redis, get the hash containing the number of times each component has been scored for the given type
    counts = client.hgetall(f"{component_type}_score_counts")

    # Get all the valid component names from the component map
    names = component_map.keys()

    # Loop over the component names and calculate the average score for each
    # Add average score to a dictionary
    average_scores = {}
    for name in names:
        score = int(values.get(name, 1))
        count = int(counts.get(name, 1))
        average = score / count
        average_scores[name] = max(average, 0.1)

    # Do a weighted random selection of the component names based on their average scores
    sum_scores = sum(average_scores.values())
    value = random.uniform(0, sum_scores)
    cumulative = 0
    for name, score in average_scores.items():
        cumulative += score
        if value <= cumulative:
            return name


def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    """
    This function interfaces with langfuse to assign a score to a conversation, specified by its ID.
    It creates a new langfuse score utilizing the provided llm, retriever, and memory components.
    The details are encapsulated in JSON format and submitted along with the conversation_id and the score.

    :param conversation_id: The unique identifier for the conversation to be scored.
    :param score: The score assigned to the conversation.
    :param llm: The Language Model component information.
    :param retriever: The Retriever component information.
    :param memory: The Memory component information.

    Example Usage:

    score_conversation('abc123', 0.75, 'llm_info', 'retriever_info', 'memory_info')
    """

    score = min(max(score, 0), 1)
    client.hincrby("llm_score_values", llm, score)
    client.hincrby("llm_score_counts", llm, 1)
    client.hincrby("retriever_score_values", retriever, score)
    client.hincrby("retriever_score_counts", retriever, 1)
    client.hincrby("memory_score_values", memory, score)
    client.hincrby("memory_score_counts", memory, 1)


def get_scores():
    """
    Retrieves and organizes scores from the langfuse client for different component types and names.
    The scores are categorized and aggregated in a nested dictionary format where the outer key represents
    the component type and the inner key represents the component name, with each score listed in an array.

    The function accesses the langfuse client's score endpoint to obtain scores.
    If the score name cannot be parsed into JSON, it is skipped.

    :return: A dictionary organized by component type and name, containing arrays of scores.

    Example:

        {
            'llm': {
                'gpt-3.5-turbo': [average_score],
                'gpt-4': [average_score]
            },
            'retriever': { 'pinecone_store': [average_score] },
            'memory': { 'sql_buffer_memory': [average_score] }
        }
    """

    aggregate = {"llm": {}, "retriever": {}, "memory": {}}

    for component_type in aggregate.keys():
        values = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_counts")
        names = values.keys()

        for name in names:
            score = int(values.get(name, 1))
            count = int(counts.get(name, 1))
            average = score / count
            aggregate[component_type][name] = [average]

    return aggregate
