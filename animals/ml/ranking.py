from animals.models import Profile

def rank_candidates(animal):
    candidates = animal.adoptionrequest_set.filter(status="Pending").select_related('user')

    scores = []
    for request in candidates:
        profile = Profile.objects.get(user=request.user)
        score = 0

        if profile.is_profile_complete:
            score += 30
        if profile.pet_experience:
            score += 20
        if profile.has_yard and animal.species == "Dog":
            score += 20
        if profile.adoption_success_count > 0:
            score += min(profile.adoption_success_count * 5, 20)

        scores.append({
            "user_id": request.user.id,
            "username": request.user.username,
            "score": score
        })

    # Sort descending
    ranked = sorted(scores, key=lambda x: x["score"], reverse=True)
    return ranked