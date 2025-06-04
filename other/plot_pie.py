import matplotlib.pyplot as plt
import numpy as np


def plt_pie(sizes, labels, save_path):
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    colors = plt.cm.tab20.colors[: len(labels)]
    explode = [0.05 if s == max(sizes) else 0 for s in sizes]

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, _,_ = ax.pie(
        sizes,
        labels=None,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        explode=explode,
        pctdistance=0.75,
    )

    # Step 1: 计算每个 wedge 的角度和理想 label 位置
    label_positions = []

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2.0 + p.theta1
        x = np.cos(np.deg2rad(ang))
        y = np.sin(np.deg2rad(ang))
        label_positions.append(
            {"i": i, "x": x, "y": y, "angle": ang, "label": labels[i]}
        )

    # Step 2: 按 y 排序并调整重叠
    label_positions.sort(key=lambda k: k["y"])
    min_gap = 0.08  # 最小 y 间距
    for idx in range(1, len(label_positions)):
        dy = label_positions[idx]["y"] - label_positions[idx - 1]["y"]
        if dy < min_gap:
            label_positions[idx]["y"] = label_positions[idx - 1]["y"] + min_gap

    # Step 3: 绘制标签（使用调整后的位置）
    kw = dict(
        arrowprops=dict(arrowstyle="-", connectionstyle="angle,angleA=0,angleB=90"),
        zorder=0,
        va="center",
        fontsize=15,
    )

    for item in label_positions:
        i = item["i"]
        x0, y0 = item["x"] * 0.9, item["y"] * 0.9
        x1, y1 = 1.1 * np.sign(item["x"]), item["y"]
        alignment = "left" if x1 > 0 else "right"

        ax.annotate(
            item["label"],
            xy=(x0, y0),
            xytext=(x1, y1),
            horizontalalignment=alignment,
            **kw
        )

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    # 数据
    sizes = [2, 19, 140, 148, 14, 4, 2, 14]
    labels = [
        "工作人员",
        "施工人员",
        "田地人员作业",
        "道路行人通行",
        "道路车辆通行",
        "误检物体",
        "有用告警",
        "其他",
    ]
    plt_pie(sizes, labels, save_path="徘徊告警.png")
