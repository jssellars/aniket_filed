def remove_actor_prefix(actor_id):
    index_of_ = actor_id.find("_")
    return actor_id[index_of_ + 1:]

def remove_actors_prefix(actor_ids):

    resulting_actors = []

    for actor_id in actor_ids:
        index_of_ = actor_id.find("_")
        resulting_actors.append(actor_id[index_of_ + 1:])

    return resulting_actors