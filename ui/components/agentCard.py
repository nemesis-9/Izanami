import streamlit as st
import ast


def agent_card(agent):
    is_alive = agent.get('IsAlive', True)
    status_class = "alive-card" if is_alive else "dead-card"
    status_text = "ALIVE" if is_alive else "DEAD"
    status_label_class = "status-alive" if is_alive else "status-dead"

    avatar_text = agent.get('AgentType', 'Unknown')[:2].upper()

    try:
        inv_dict = (
            ast.literal_eval(agent["Inventory"])
            if isinstance(agent["Inventory"], str)
            else agent["Inventory"]
        )

        inv_tags = "".join(
            f"""<span class="inv-tag">{k}: {v:.0f}</span>"""
            for k, v in inv_dict.items()
            if v >= 0
        ) or "<span class='inv-empty'>Empty</span>"

    except Exception:
        inv_tags = "<span class='inv-empty'>Empty</span>"

    card_html = f"""
    <div class="agent-card {status_class}">
        <div class="agent-header">
            <div class="agent-step"><div class="agent-state-dot {status_label_class}"></div></div>
            <div class="agent-avatar">{avatar_text}</div>
            <div>
                <div class="agent-title">Agent {agent.get('AgentID', 'Unknown')}</div>
                <span class="agent-badge">{agent.get('AgentType', 'Unknown')}</span>
            </div>
        </div>
        <div class="agent-stats">
            <div class="stat-box">
                <div class="stat-label">Status</div>
                <div class="stat-value {status_label_class}">{status_text}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Health</div>
                <div class="stat-value">{agent.get('HealthPoints', 0.0):.1f}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Wealth</div>
                <div class="stat-value wealth">${agent.get('Wealth', 0.0):.2f}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Location</div>
                <div class="stat-value">{agent.get('AgentLocation', 'Unknown')}</div>
            </div>
        </div>
        <div class="agent-inventory">
            <div class="section-label">Current Inventory</div>
            <div class="inventory-list">
                {inv_tags}
            </div>
        </div>
        <div class="agent-action">
            Last Action: {agent.get('Action', 'None')}
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)
