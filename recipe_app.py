"""
=====================================
  私房菜谱管理 - 云端部署版
=====================================

适配平台：Streamlit Cloud（免费）
  - 数据通过 /mount/src/recipes.json 持久化
  - 本地运行同样兼容

手机访问：
  部署成功后，用手机浏览器打开你的 Streamlit Cloud 地址即可

功能说明：
  1. 菜谱的增、删、改、查（CRUD）
  2. 按食材实时搜索 / 多食材组合搜索
  3. 手机端完美适配，响应式布局

作者：龙虾宝宝的私房厨房 🍳
"""

import json
import os
import streamlit as st

# ============================================================================
# 配置区
# ============================================================================

# ---- 数据持久化路径 ----
# Streamlit Cloud 提供了 /mount/src/ 目录，重启后数据不会丢失
# 本地运行时自动回退到脚本所在目录
if os.path.isdir("/mount/src"):
    DATA_DIR = "/mount/src"
else:
    # 本地运行：使用脚本同目录或用户主目录
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.access(_script_dir, os.W_OK):
        DATA_DIR = _script_dir
    else:
        DATA_DIR = os.path.expanduser("~")

DATA_FILE = os.path.join(DATA_DIR, "recipes.json")

# 页面基础配置
st.set_page_config(
    page_title="私房菜谱管理",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="auto",
)


# ============================================================================
# 数据持久化：JSON 文件读写
# ============================================================================

def load_recipes():
    """
    从 JSON 文件加载全部菜谱。
    首次使用返回内置示例数据。
    返回值：list[dict]，每个字典代表一道菜谱。
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except (json.JSONDecodeError, IOError, PermissionError):
            pass
    # 写入示例数据并返回
    sample = _get_sample_recipes()
    save_recipes(sample)
    return sample


def save_recipes(recipes):
    """原子写入：先写临时文件，再重命名，防止数据损坏。"""
    tmp_file = DATA_FILE + ".tmp"
    try:
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
        # Windows 不支持原子 rename，分步处理
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        os.rename(tmp_file, DATA_FILE)
    except Exception:
        # 回退：直接写入
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)


# ============================================================================
# 示例数据（首次使用时的默认菜谱）
# ============================================================================

def _get_sample_recipes():
    """返回一组内置示例菜谱，方便首次体验。"""
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
    """
    根据用户输入的食材关键词筛选菜谱。

    高阶匹配规则：
      - 用户输入 "番茄鸡蛋" → 自动拆分为 ["番茄", "鸡蛋"]
      - 菜谱必须**同时包含所有输入的食材**才被命中
      - 支持逗号分隔的多食材："鸡肉, 土豆" → ["鸡肉", "土豆"]
    """
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
# UI 组件：添加 / 编辑菜谱表单
# ============================================================================

def show_recipe_form(edit_index=None):
    """渲染「新增菜谱」或「编辑菜谱」的表单。"""
    recipes = st.session_state.get("recipes", [])

    if edit_index is not None and 0 <= edit_index < len(recipes):
        existing = recipes[edit_index]
        default_name = existing["name"]
        default_ings = ", ".join(existing["ingredients"])
        default_steps = existing["steps"]
        form_title = f"✏️ 编辑菜谱：{existing['name']}"
        submit_label = "💾 保存修改"
    else:
        default_name = ""
        default_ings = ""
        default_steps = ""
        form_title = "📝 添加新菜谱"
        submit_label = "➕ 添加菜谱"

    with st.form(key="recipe_form", clear_on_submit=True):
        st.subheader(form_title)

        name = st.text_input(
            label="菜名 *",
            value=default_name,
            placeholder="例如：番茄炒蛋",
        )

        ingredients = st.text_area(
            label="食材列表（用逗号分隔）*",
            value=default_ings,
            height=100,
            placeholder="例如：番茄, 鸡蛋, 葱花, 盐, 糖",
            help="每样食材之间用英文或中文逗号隔开",
        )

        steps = st.text_area(
            label="制作步骤 *",
            value=default_steps,
            height=200,
            placeholder=(
                "请详细描述制作步骤...\n"
                "例如：\n"
                "1. 番茄洗净切块\n"
                "2. 鸡蛋打散..."
            ),
        )

        submitted = st.form_submit_button(submit_label, use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("⚠️ 请填写菜名！")
                return
            if not ingredients.strip():
                st.error("⚠️ 请填写至少一种食材！")
                return
            if not steps.strip():
                st.error("⚠️ 请填写制作步骤！")
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
                st.success(f'✅ 菜谱「{new_recipe["name"]}」已更新！')
                st.session_state.pop("editing_index", None)
            else:
                st.session_state.recipes.append(new_recipe)
                save_recipes(st.session_state.recipes)
                st.success(f'✅ 菜谱「{new_recipe["name"]}」已添加！')

            st.rerun()


# ============================================================================
# UI 组件：展示单张菜谱卡片
# ============================================================================

def recipe_card(recipe, index):
    """以美观的卡片形式展示一道菜谱。"""
    st.markdown(f"### {recipe['name']}")

    # 食材标签 —— 自动换行，避免手机端溢出
    for ing in recipe["ingredients"]:
        st.markdown(
            f'<span style="'
            f'background:#e8f5e9;'
            f'color:#2e7d32;'
            f'padding:3px 10px;'
            f'border-radius:14px;'
            f'font-size:13px;'
            f'display:inline-block;'
            f'margin:2px;'
            f'white-space:nowrap;">'
            f'{ing}</span>',
            unsafe_allow_html=True,
        )
    st.write("")  # 空行间隔

    # 制作步骤（可折叠）
    with st.expander("📖 查看制作步骤", expanded=False):
        st.markdown(
            recipe["steps"].replace("\n", "<br>"),
            unsafe_allow_html=True,
        )

    # 操作按钮行
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button("✏️ 编辑", key=f"edit_{index}", use_container_width=True):
            st.session_state["editing_index"] = index
            st.rerun()

    with btn_col2:
        if st.button("🗑️ 删除", key=f"del_{index}",
                     type="secondary", use_container_width=True):
            st.session_state[f"confirm_del_{index}"] = True

    # 删除确认弹窗
    if st.session_state.get(f"confirm_del_{index}"):
        c_warn, c_yes, c_no = st.columns([6, 2, 2])
        with c_warn:
            st.warning(f'确定删除「{recipe["name"]}」吗？此操作不可恢复！')
        with c_yes:
            if st.button("⚠️ 确认删除", key=f"yes_{index}",
                         type="primary"):
                del st.session_state.recipes[index]
                save_recipes(st.session_state.recipes)
                st.success(f'已删除「{recipe["name"]}」')
                st.session_state.pop(f"confirm_del_{index}", None)
                st.rerun()
        with c_no:
            if st.button("取消", key=f"no_{index}"):
                st.session_state.pop(f"confirm_del_{index}", None)
                st.rerun()

    st.divider()


# ============================================================================
# 主程序入口
# ============================================================================

def main():
    """应用的主体 UI 流程。"""

    # ---- 初始化 session_state ----
    if "recipes" not in st.session_state:
        st.session_state.recipes = load_recipes()

    # ================================================================
    #  侧边栏：添加 / 编辑菜谱 + 统计信息
    # ================================================================
    with st.sidebar:
        st.title("私房菜谱")

        total = len(st.session_state.recipes)
        total_ings = len(set(
            ing for r in st.session_state.recipes for ing in r["ingredients"]
        ))
        st.metric("菜谱总数", total)
        st.metric("食材种类", total_ings)

        st.markdown("---")

        editing_idx = st.session_state.get("editing_index")

        if editing_idx is not None:
            st.info(f'正在编辑第 {editing_idx + 1} 道菜')
            if st.button("取消编辑", use_container_width=True):
                st.session_state.pop("editing_index", None)
                st.rerun()
            st.markdown("---")

        show_recipe_form(edit_index=editing_idx)

        st.markdown("---")
        st.caption("数据自动保存云端")

    # ================================================================
    #  主区域：搜索栏 + 菜谱列表
    # ================================================================
    st.title("我的私房菜谱")
    st.caption("输入食材，快速找到你想做的菜")

    st.markdown("---")

    # 实时搜索框
    search_query = st.text_input(
        label="按食材搜索菜谱",
        placeholder="尝试输入：鸡肉, 土豆 或 番茄鸡蛋",
        label_visibility="collapsed",
    )

    # 执行搜索
    filtered = search_recipes(st.session_state.recipes, search_query)

    # 搜索结果统计
    if search_query.strip():
        st.info(
            f'输入「**{search_query.strip()}**」，'
            f'找到 **{len(filtered)}** 道相关菜谱'
        )
    else:
        st.success(f'共有 **{total}** 道菜谱')

    st.markdown("---")

    # 菜谱卡片列表
    if filtered:
        for idx, recipe in enumerate(filtered):
            real_index = st.session_state.recipes.index(recipe)
            recipe_card(recipe, real_index)
    else:
        st.markdown("""
        <div style='text-align:center; padding:40px 0; color:#999;'>
            <h2>没有找到匹配的菜谱</h2>
            <p>试试换个食材关键词，或者添加一道新菜谱吧！</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
