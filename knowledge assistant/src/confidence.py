# 计算信任度的函数
def confidance(respond):
    if not respond:
        return 0.0

    scores = [score for _, score in respond]
    # 平均分
    avg_score = sum(scores)/len(scores)
    # 最高分
    max_score = max(scores)
    # 一致性
    score_range = max(scores) - min(scores)
    consistency = 1.0 - min(score_range / 0.3, 1.0)

    # 得到信任度
    confidance = avg_score * 0.4 + max_score * 0.3 + consistency * 0.3

    confidance = min(confidance,1.0)

    return confidance