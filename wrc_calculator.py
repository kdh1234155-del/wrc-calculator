import streamlit as st

# wOBA와 wRC+, 등급 계산 함수는 이전과 동일
def calculate_woba(bb, hbp, h, dbl, tpl, hr, ab, sf):
    singles = h - dbl - tpl - hr
    numerator = (0.69 * bb) + (0.72 * hbp) + (0.88 * singles) + (1.24 * dbl) + (1.56 * tpl) + (1.98 * hr)
    denominator = ab + bb + sf + hbp
    if denominator == 0:
        return 0
    return numerator / denominator

def calculate_wrc_plus(woba, league_woba, woba_scale, league_r_pa, park_factor):
    pf_adjusted = park_factor / 100.0
    wraa_per_pa = (woba - league_woba) / woba_scale
    park_adjustment = (league_r_pa - (pf_adjusted * league_r_pa))
    if league_r_pa == 0:
        return 0
    wrc_plus = (((wraa_per_pa + league_r_pa) + park_adjustment) / league_r_pa) * 100
    return wrc_plus

# 네가 수정한 등급 설명이 있는 함수 (그대로 두면 돼!)
def get_wrc_plus_grade(wrc_plus):
    if wrc_plus >= 160:
        return "🏆 우리 팀의 희망 (MVP 급)"
    elif wrc_plus >= 140:
        return "⭐ 훌륭함 (올스타급)"
    elif wrc_plus >= 115:
        return "👍 좋음 (주전급 이상)"
    elif wrc_plus >= 100:
        return "🙂 1인분은 하는 선수"
    elif wrc_plus >= 80:
        return "👇 평균 이하 (수비라도 잘해야...)"
    elif wrc_plus >= 60:
        return "🥶 나쁨"
    else:
        return "😱 끔찍함"

# --- 웹페이지 UI 부분 ---
st.title('⚾ MLB The Show wRC+ 추정 계산기')
st.write("더 쇼 게임에서 확인한 선수의 시즌 스탯을 입력하세요.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    h = st.number_input("안타(H)", min_value=0, step=1)
    dbl = st.number_input("2루타(2B)", min_value=0, step=1)
with col2:
    tpl = st.number_input("3루타(3B)", min_value=0, step=1)
    hr = st.number_input("홈런(HR)", min_value=0, step=1)
with col3:
    bb = st.number_input("볼넷(BB)", min_value=0, step=1)
    hbp = st.number_input("몸 맞는 공(HBP)", min_value=0, step=1)
with col4:
    ab = st.number_input("타수(AB)", min_value=0, step=1)
    sf = st.number_input("희생플라이(SF)", min_value=0, step=1)

memo = st.text_input("✍️ 선수 평가 메모 (선택 사항)", placeholder="예: 우리 팀의 미래! or 수비는 좋지만 타격은 아쉽다.")

if st.button('wRC+ 계산하기'):
    if ab > 0:
        player_woba = calculate_woba(bb, hbp, h, dbl, tpl, hr, ab, sf)
        league_woba, woba_scale, league_r_pa, park_factor = 0.310, 1.27, 0.115, 100
        result_wrc_plus = calculate_wrc_plus(player_woba, league_woba, woba_scale, league_r_pa, park_factor)
        grade = get_wrc_plus_grade(result_wrc_plus)
        
        st.divider()
        st.subheader("📊 계산 결과")
        
        # --- [수정된 부분] 결과를 2개의 컬럼으로 바꾸고, 긴 설명은 아래에 따로 표시 ---
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="계산된 선수 wOBA", value=f"{player_woba:.3f}")
        with res_col2:
            st.metric(label="추정 wRC+", value=f"{result_wrc_plus:.1f}")
        
        # 등급 설명은 st.markdown을 사용해 아래에 따로 길게 표시
        st.markdown(f"**등급:** {grade}")
        
        if memo:
            st.success(f"나의 평가: {memo}")
            
    else:
        st.error("타수(AB)는 0보다 커야 합니다.")