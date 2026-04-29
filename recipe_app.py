"""
=====================================
  私房菜谱管理 - 云端部署版 v2
=====================================

适配平台：Streamlit Cloud（免费）
  - 数据通过 /mount/src/recipes.json 持久化
  - 本地运行同样兼容

v2 优化：
  - 页面更紧凑，减少冗余间距
  - 图标全面升级（精致 Unicode）
  - 菜谱卡片重新设计
  - 食材标签渐变色美化
  - 手机端体验进一步优化

作者：龙虾宝宝的私房厨房
"""

import json
import os
import streamlit as st

# ============================================================================
# 配置区
# ============================================================================

if os.path.isdir("/mount/src"):
    DATA_DIR = "/mount/src"
else:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.access(_script_dir, os.W_OK):
        DATA_DIR = _script_dir
    else:
        DATA_DIR = os.path.expanduser("~")

DATA_FILE = os.path.join(DATA_DIR, "recipes.json")

st.set_page_config(
    page_title="私房菜谱",
    page_icon="♨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---- 全局样式注入：让整体更紧凑 ----
COMPACT_STYLE = """
<style>
/* 全局间距压缩 */
.stApp { padding-top: 0.6rem !important; }
.stTitle { font-size: 1.4rem !important; margin-bottom: 0.3rem !important; }
.stSubheader { font-size: 0.95rem !important; margin-bottom: 0.2rem !important; }

/* 侧边栏精简 */
[data-testid="stSidebar"] {
    min-width: 260px !important;
    max-width: 280px !important;
}

/* Metric 卡片紧凑 */
[data-testid="stMetric"] {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 0.35rem 0.7rem !important;
    border-left: 3px solid #e67e22;
}

/* 搜索框美化 */
[data-testid="stTextInput"] > div > div > input {
    border-radius: 12px !important;
    border: 2px solid #ddd !important;
    transition: all 0.2s;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #e67e22 !important;
    box-shadow: 0 0 0 2px rgba(230,126,34,0.15) !important;
}

/* 按钮圆角 */
button[kind="primary"] { border-radius: 10px !important; }
button[kind="secondary"] { border-radius: 10px !important; }

/* 分割线减淡 */
hr { margin: 0.5rem 0 !important; opacity: 0.4; }
</style>
"""
st.markdown(COMPACT_STYLE, unsafe_allow_html=True)


# ============================================================================
# 数据持久化
# ============================================================================

def load_recipes():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except (json.JSONDecodeError, IOError, PermissionError):
            pass
    sample = _get_sample_recipes()
    save_recipes(sample)
    return sample


def save_recipes(recipes):
    tmp_file = DATA_FILE + ".tmp"
    try:
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        os.rename(tmp_file, DATA_FILE)
    except Exception:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)


# ============================================================================
# 示例数据
# ============================================================================

def _get_sample_recipes():
    return [
        {
            "name": "番茄炒蛋",
            "ingredients": ["番茄", "鸡蛋", "葱花", "盐", "糖"],
            "steps": (
                "1. 番茄洗净切块，鸡蛋打散加少许盐。\n"
                "2. 热锅倒油，蛋液倒入炒至凝固盛出。\n"
                "3. 锅中再加少许油，放入番茄翻炒出汁。\n"
                "4. 倒入炒好的鸡蛋，加盐和少许糖调味。\n"
                "5. 撒上葱花，翻炒均匀即可出锅。"
            ),
        },
        {
            "name": "土豆炖鸡肉",
            "ingredients": ["鸡肉", "土豆", "胡萝卜", "姜片", "料酒", "酱油"],
            "steps": (
                "1. 鸡肉切块焯水去血沫；土豆、胡萝卜去皮切滚刀块。\n"
                "2. 热锅冷油，爆香姜片后倒入鸡块煸炒。\n"
                "3. 加入料酒、酱油翻炒均匀。\n"
                "4. 加入没过食材的热水，大火烧开后转小火炖30分钟。\n"
                "5. 放入土豆和胡萝卜块，继续炖15分钟至软烂即可。"
            ),
        },
        {
            "name": "蒜蓉西兰花",
            "ingredients": ["西兰花", "大蒜", "蚝油", "盐"],
            "steps": (
                "1. 西兰花掰成小朵，淡盐水浸泡10分钟后冲洗干净。\n"
                "2. 大蒜切成蒜末备用。\n"
                "3. 烧一锅开水，加少许盐和油，焯西兰花1分钟捞出。\n"
                "4. 热锅倒油，小火炒香蒜末。\n"
                "5. 倒入西兰花，加蚝油和少许盐，快速翻炒均匀出锅。"
            ),
        },
        {
            "name": "红烧肉",
            "ingredients": ["五花肉", "冰糖", "生抽", "老抽", "料酒", "八角", "桂皮", "葱姜"],
            "steps": (
                "1. 五花肉切3cm见方块，冷水下锅焯水后捞出沥干。\n"
                "2. 锅中放少许油，加入冰糖小火炒出糖色。\n"
                "3. 放入肉块翻炒上色，加葱段、姜片、八角、桂皮。\n"
                "4. 烹入料酒，加生抽、老抽翻炒均匀。\n"
                "5. 加热水没过肉，大火烧开转小火焖煮45分钟。\n"
                "6. 大火收汁，汤汁浓稠即可出锅。"
            ),
        },
        {
            "name": "番茄土豆牛腩",
            "ingredients": ["牛腩", "番茄", "土豆", "胡萝卜", "姜片", "料酒", "番茄酱"],
            "steps": (
                "1. 牛腩切块冷水下锅焯水，捞出洗净。\n"
                "2. 土豆、胡萝卜去皮切块；番茄顶部划十字，开水烫去皮后切块。\n"
                "3. 热锅放油，炒香姜片后倒入牛腩煸炒。\n"
                "4. 加料酒、番茄酱炒匀，加热水没过牛肉。\n"
                "5. 大火烧开转小火炖1小时至软烂。\n"
                "6. 加入土豆、胡萝卜、番茄再炖20分钟，调味即可。"
            ),
        },
    ]


# ============================================================================
# 核心搜索逻辑
# ============================================================================

def search_recipes(recipes, query):
    if not query or not query.strip():
        return recipes
    raw_parts = query.replace("，", ",").split(",")
    keywords = [p.strip() for p in raw_parts if p.strip()]
    if not keywords:
        return recipes
    matched = []
    for recipe in recipes:
        all_ings = "".join(recipe.get("ingredients", []))
        if all(kw in all_ings for kw in keywords):
            matched.append(recipe)
    return matched


# ============================================================================
# 颜色工具：为每个菜名生成稳定的渐变色
# ============================================================================

def _recipe_color(name):
    """根据菜名哈希返回一组稳定颜色。"""
    colors = [
        ("#ff6b6b", "#ee5a24"),   /* 红-橙 */
        ("#f9ca24", "#f0932b"),   /* 黄-橙 */
        ("#6c5ce7", "#a29bfe"),   /* 紫-浅紫 */
        ("#00b894", "#55efc4"),   /* 绿-薄荷 */
        ("#0984e3", "#74b9ff"),   /* 蓝-天蓝 */
        ("#d63031", "#ff7675"),   /* 红-粉红 */
        ("#e17055", "#fab1a0"),   /* 橙-桃色 */
        ("#00cec9", "#81ecec"),   /* 青-淡青 */
    ]
    idx = hash(name) % len(colors)
    return colors[idx]


# ============================================================================
# UI 组件：添加 / 编辑表单
# ============================================================================

def show_recipe_form(edit_index=None):
    recipes = st.session_state.get("recipes", [])

    if edit_index is not None and 0 <= edit_index < len(recipes):
        existing = recipes[edit_index]
        default_name = existing["name"]
        default_ings = ", ".join(existing["ingredients"])
        default_steps = existing["steps"]
        form_title = f"编辑：{existing['name']}"
        submit_label = "[保存修改]"
    else:
        default_name = ""
        default_ings = ""
        default_steps = ""
        form_title = "+ 添加新菜谱"
        submit_label = "+ 添加菜谱"

    with st.form(key="recipe_form", clear_on_submit=True):
        st.markdown(f"##### {form_title}")

        name = st.text_input(
            label="菜名 *",
            value=default_name,
            placeholder="例：番茄炒蛋",
            label_visibility="collapsed",
        )

        ingredients = st.text_area(
            label="食材列表（逗号分隔）*",
            value=default_ings,
            height=80,
            placeholder="番茄, 鸡蛋, 葱花, 盐, 糖",
            label_visibility="collapsed",
        )

        steps = st.text_area(
            label="制作步骤 *",
            value=default_steps,
            height=140,
            placeholder="1. 第一步...\n2. 第二步...",
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button(submit_label, use_container_width=True, type="primary")

        if submitted:
            if not name.strip():
                st.error("请填写菜名")
                return
            if not ingredients.strip():
                st.error("请填写至少一种食材")
                return
            if not steps.strip():
                st.error("请填写制作步骤")
                return

            ing_list = [
                item.strip()
                for item in ingredients.replace("，", ",").split(",")
                if item.strip()
            ]

            new_recipe = {
                "name": name.strip(),
                "ingredients": ing_list,
                "steps": steps.strip(),
            }

            if edit_index is not None:
                st.session_state.recipes[edit_index] = new_recipe
                save_recipes(st.session_state.recipes)
                st.success(f'已更新「{new_recipe["name"]}」')
                st.session_state.pop("editing_index", None)
            else:
                st.session_state.recipes.append(new_recipe)
                save_recipes(st.session_state.recipes)
                st.success(f'已添加「{new_recipe["name"]}」')

            st.rerun()


# ============================================================================
# UI 组件：菜谱卡片（重新设计）
# ============================================================================

def recipe_card(recipe, index):
    c1, c2 = _recipe_color(recipe["name"])

    # 卡片头部：菜名 + 操作按钮
    col_left, col_right = st.columns([5, 1])
    with col_left:
        st.markdown(
            f"<span style='font-size:1.08rem;font-weight:600;"
            f"color:#222;border-left:4px solid {c1};padding-left:8px;'>"
            f"{recipe['name']}</span>",
            unsafe_allow_html=True,
        )
    with col_right:
        btn_e, btn_d = st.columns(2)
        with btn_e:
            if st.button("✎", key=f"edit_{index}",
                         help="编辑", use_container_width=True):
                st.session_state["editing_index"] = index
                st.rerun()
        with btn_d:
            if st.button("×", key=f"del_{index}",
                         help="删除", type="secondary", use_container_width=True):
                st.session_state[f"confirm_del_{index}"] = True

    # 食材标签行 —— 渐变胶囊式标签
    tags_html = " ".join([
        f'<span style="background:linear-gradient(135deg,{c1},{c2});'
        f'color:white;padding:2px 11px;border-radius:12px;'
        f'font-size:12px;display:inline-block;margin:2px;'
        f'font-weight:500;">{ing}</span>'
        for ing in recipe["ingredients"]
    ])
    st.markdown(f"<div style='margin:2px 0 4px 14px;'>{tags_html}</div>", unsafe_allow_html=True)

    # 制作步骤（可折叠）
    with st.expander("查看步骤", expanded=False, icon="📋"):
        st.markdown(
            f"<div style='line-height:1.7;font-size:0.88rem;color:#444;padding-left:8px;'>"
            f"{recipe['steps'].replace(chr(10), '<br>')}"
            f"</div>",
            unsafe_allow_html=True,
        )

    # 删除确认弹窗
    if st.session_state.get(f"confirm_del_{index}"):
        st.markdown("---")
        cw, cy, cn = st.columns([5, 1.5, 1.5])
        with cw:
            st.warning(f'确定删除「{recipe["name"]}」？')
        with cy:
            if st.button("确认", key=f"yes_{index}", type="primary", use_container_width=True):
                del st.session_state.recipes[index]
                save_recipes(st.session_state.recipes)
                st.success('已删除')
                st.session_state.pop(f"confirm_del_{index}", None)
                st.rerun()
        with cn:
            if st.button("取消", key=f"no_{index}", use_container_width=True):
                st.session_state.pop(f"confirm_del_{index}", None)
                st.rerun()

    st.markdown("<hr style='opacity:0.25;margin:8px 0;'>", unsafe_allow_html=True)


# ============================================================================
# 主程序入口
# ============================================================================

def main():
    if "recipes" not in st.session_state:
        st.session_state.recipes = load_recipes()

    # ================================================================
    # 侧边栏
    # ================================================================
    with st.sidebar:
        # Logo 区域
        st.markdown("""
        <div style='text-align:center;padding:0.5rem 0;'>
            <span style='font-size:2rem;'>♨</span>
            <div style='font-size:1.05rem;font-weight:700;color:#e67e22;'>私房菜谱</div>
        </div>
        """, unsafe_allow_html=True)

        total = len(st.session_state.recipes)
        total_ings = len(set(
            ing for r in st.session_state.recipes for ing in r["ingredients"]
        ))
        m1, m2 = st.columns(2)
        with m1:
            st.metric("菜谱", str(total))
        with m2:
            st.metric("食材", str(total_ings))

        st.markdown("<hr>", unsafe_allow_html=True)

        editing_idx = st.session_state.get("editing_index")
        if editing_idx is not None:
            if st.button("← 取消编辑", use_container_width=True):
                st.session_state.pop("editing_index", None)
                st.rerun()

        show_recipe_form(edit_index=editing_idx)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.caption("数据自动保存云端")

    # ================================================================
    # 主区域
    # ================================================================
    # 顶栏标题 + 搜索框一行搞定
    tcol, scol = st.columns([1, 2])
    with tcol:
        st.markdown("### 我的私房菜谱")
    with scol:
        search_query = st.text_input(
            label="search",
            placeholder="搜索食材… (如: 鸡肉 土豆)",
            label_visibility="collapsed",
        )

    filtered = search_recipes(st.session_state.recipes, search_query)

    # 结果统计（精简为一行小字）
    if search_query.strip():
        st.caption(f'「{search_query.strip()}」→ 找到 **{len(filtered)}** 道匹配菜谱')
    else:
        st.caption(f'共 **{total}} 道菜谱')

    st.markdown("<hr style='opacity:0.25;'>", unsafe_allow_html=True)

    # 菜谱列表
    if filtered:
        for idx, recipe in enumerate(filtered):
            real_index = st.session_state.recipes.index(recipe)
            recipe_card(recipe, real_index)
    else:
        st.markdown("""
        <div style='text-align:center; padding:30px 0; color:#bbb;'>
            <span style='font-size:2.5rem;'>&#128270;</span><br>
            <span style='font-size:1rem;'>没有找到匹配的菜谱</span><br>
            <span style='font-size:0.85rem;'>试试换个关键词或添加新菜谱吧</span>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
