from db_config import Profile


def match_users(user_profiles, user_id, num_matches=3):
    user_profile = user_profiles[user_id]
    match_scores = []

    for other_user_id, other_user_profile in user_profiles.items():
        if other_user_id != user_id:
            match_score = calculate_match_score(user_profile, other_user_profile)
            match_scores.append((other_user_id, match_score))

    # マッチ度の高い順にソート
    match_scores.sort(key=lambda x: x[1], reverse=True)

    # 最もマッチするユーザーを選択
    top_matches = match_scores[:num_matches]
    return [user_profiles[user_id] for user_id, _ in top_matches]


def perform_matching(profile):
    matches = []
    all_profiles = Profile.select()

    for other_profile in all_profiles:
        if other_profile == profile:
            continue  # 自分自身とのマッチングはスキップ

        match_score = calculate_match_score(profile, other_profile)

        # マッチングスコアが基準を満たす場合にのみマッチとして追加
        if match_score >= 0.7:
            matches.append(other_profile)

    return matches


def calculate_match_score(profile1, profile2):
    interests1 = set(profile1.interests.split(","))
    interests2 = set(profile2.interests.split(","))

    # 共通の興味を計算
    common_interests = interests1 & interests2

    # 共通の興味の数に基づいてマッチングスコアを設定
    if len(common_interests) >= 2:
        match_score = 0.8  # 高いマッチングスコア
    elif len(common_interests) == 1:
        match_score = 0.6  # 中程度のマッチングスコア
    else:
        match_score = 0.4  # 低いマッチングスコア

    return match_score

