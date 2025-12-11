from pathlib import Path
import pandas as pd
import plotly.express as px
from step_1_1 import OUT_DIR
from step_3_1 import OUT_3_1

df_raw = pd.read_csv(OUT_3_1)

fig = px.treemap(
    df_raw,
    path=["종목명"],
    values="조단위",
    color="조단위",
    color_continuous_scale="Plasma",
)

# ★ 핵심: 삼성전자만 글자색 검정색으로 지정
text_colors = ["black" if label == "삼성전자" else "white" for label in df_raw["종목명"]]

fig.update_traces(
    marker=dict(
        cornerradius=5,
        line=dict(width=2, color="white"),
        pad=dict(t=10, r=10, b=10, l=10)
    ),
    texttemplate="<b>%{label}</b><br>%{value:,.0f}조원",
    textfont=dict(
        size=30,
        color=text_colors          # ← 여기서 개별 색상 적용!
    ),
    hovertemplate="<b>%{label}</b><br>시가총액: %{value:,.1f}조원<extra></extra>"
)

fig.update_layout(
    margin=dict(t=0, r=0, b=0, l=0),
    coloraxis_colorbar=dict(
        title="시가총액 (조원)",
        tickformat=",",
        x=1.02
    )
)

img_path = OUT_DIR / f"{Path(__file__).stem}.png"
fig.write_image(img_path, width=1600, height=900, scale=2)

print(f"트리맵 저장 완료 (삼성전자 글자 검정색 적용): {img_path}")