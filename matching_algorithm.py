import spacy
from db_config import Profile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# spaCyを初期化
nlp = spacy.load("en_core_web_sm")


def calculate_nlp_similarity(profile1: Profile, profile2):
    # プロフィールのテキスト情報をspaCyで処理
    doc1 = nlp(
        f"{profile1.type_of_communication} {profile1.talk_contents_title} {profile1.other_topic_theme}"
    )
    doc2 = nlp(
        f"{profile2.type_of_communication} {profile2.talk_contents_title} {profile2.other_topic_theme}"
    )

    # spaCyの類似度スコアを計算
    similarity_score = doc1.similarity(doc2)

    return similarity_score


def extract_tfidf_features(text_data):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(text_data)
    return tfidf_matrix


def match_users(user_profiles, user_id, num_matches=3):
    user_profile = user_profiles[user_id]
    match_scores = []

    for other_user_id, other_user_profile in user_profiles.items():
        if other_user_id != user_id:
            # プロフィール間のNLPベースの類似度を計算
            nlp_similarity = calculate_nlp_similarity(user_profile, other_user_profile)

            # TF-IDFベースの類似度を計算
            user_profile_text = user_profile.text()
            other_user_profile_text = other_user_profile.text()
            tfidf_matrix = extract_tfidf_features([user_profile_text, other_user_profile_text])
            tfidf_similarity = cosine_similarity(tfidf_matrix)

            # NLP類似度とTF-IDF類似度を組み合わせてマッチングスコアを計算
            match_score = (nlp_similarity + tfidf_similarity[0, 1]) / 2

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

        # プロフィール間のNLPベースの類似度を計算
        nlp_similarity = calculate_nlp_similarity(profile, other_profile)

        # TF-IDFベースの類似度を計算
        profile_text = (
            f"{profile.type_of_communication} {profile.talk_contents_title} {profile.other_topic_theme}"
        )
        other_profile_text = f"{other_profile.type_of_communication} {other_profile.talk_contents_title} {other_profile.other_topic_theme}"
        tfidf_matrix = extract_tfidf_features([profile_text, other_profile_text])
        tfidf_similarity = cosine_similarity(tfidf_matrix)

        # NLP類似度とTF-IDF類似度を組み合わせてマッチングスコアを計算
        match_score = (nlp_similarity + tfidf_similarity[0, 1]) / 2

        # マッチングスコアが基準を満たす場合にのみマッチとして追加
        if match_score >= 0.7:
            matches.append(other_profile)

    return matches
