import streamlit as st
import ast


def memorial_card(agent):
    avatar_text = agent.get('AgentType', 'Unknown')[:2].upper()

    try:
        inv_dict = (
            ast.literal_eval(agent["Dying_Inventory"])
            if isinstance(agent["Dying_Inventory"], str)
            else agent["Dying_Inventory"]
        )

        inv_tags = "".join(
            f"""<span class="inv-tag">{k}: {v:.0f}</span>"""
            for k, v in inv_dict.items()
            if v > 0
        ) or "<span class='inv-empty'>Empty</span>"

    except Exception:
        inv_tags = "<span class='inv-empty'>Empty</span>"

    card_html = f"""
    <div class="agent-card">
        <div class="agent-step">STEP {agent['Step']}</div>
        <div class="agent-header">
            <div class="agent-avatar">{avatar_text}</div>
            <div>
                <div class="agent-title">
                    Agent {agent['AgentID']}
                </div>
                <span class="agent-badge">
                    {agent['AgentType']}
                </span>
            </div>
        </div>
        <div class="agent-stats">
            <div class="stat-box">
                <div class="stat-label">Life Span</div>
                <div class="stat-value">
                    {agent['DyingAge']} Cycles
                </div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Wealth</div>
                <div class="stat-value wealth">
                    ${agent['DyingWealth']:.2f}
                </div>
            </div>
        </div>
        <div class="agent-inventory">
            <div class="section-label">Recovered Inventory</div>
            <div class="inventory-list">
                {inv_tags}
            </div>
        </div>
        <div class="agent-action">
            Last Action: {agent['DyingAction']}
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)
