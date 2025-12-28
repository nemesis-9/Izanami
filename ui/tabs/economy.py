import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ast


def economy_tab(model_data):
    def safe_parse(val):
        try:
            return ast.literal_eval(val) if isinstance(val, str) else val
        except:
            return {}

    # Current Step Context
    current_step = st.session_state.step
    all_history = model_data[model_data['Step'] <= current_step]
    current_row = model_data[model_data['Step'] == current_step].iloc[0]
    prev_row = model_data[model_data['Step'] == current_step - 1].iloc[0] if current_step > 1 else current_row

    header_cols = st.columns([9, 2])

    with header_cols[0]:
        st.markdown("""
            <div class="flex flex-col border-l-4 border-purple-600 pl-6 py-2">
                <h1 class="text-6xl font-black text-white tracking-tighter flex items-center gap-4">
                    <span class="shining-title" style="font-size: 4rem; font-weight: 900; letter-spacing: -2px; font-style: italic;">
                        IZANAMI
                    </span>
                    <span class="bg-purple-600 text-xs font-mono tracking-normal px-2 py-1 rounded italic text-purple-100">
                        ECONOMY
                    </span>
                </h1>
                <p class="text-purple-400/60 font-mono text-sm mt-1 uppercase tracking-widest">
                    Macro-Stability & Resource Circulation Protocol
                </p>
            </div>
            """, unsafe_allow_html=True)

    with header_cols[1]:
        spc = st.columns(3)
        with spc[1]:
            st.metric("Step", st.session_state.step)

    left_col, right_col = st.columns([4, 1])

    with left_col:
        st.divider()

        kpi = st.columns(4)
        with kpi[0]:
            st.metric(
                "Global Wealth",
                f"${current_row['TotalAgentWealth']:,.0f}",
                delta=f"{current_row['TotalAgentWealth'] - prev_row['TotalAgentWealth']:,.0f}"
            )
        with kpi[1]:
            st.metric("State Treasury", f"${current_row['Treasury']:,.0f}",
                      delta=f"{current_row['Treasury'] - prev_row['Treasury']:,.0f}")
        with kpi[2]:
            tax_pct = current_row['TaxRate'] * 100
            st.metric("Current Tax Rate", f"{tax_pct:.1f}%", delta=None)

        st.write("")

        chart_spc = st.columns([5, 1])

        with chart_spc[0]:

            st.markdown('<p class="section-label">Wealth Accumulation & State Liquidity</p>', unsafe_allow_html=True)
            chart_data = all_history[['Step', 'TotalAgentWealth', 'Treasury']].copy()
            chart_data = chart_data.rename(columns={
                'TotalAgentWealth': 'Agent Wealth',
                'Treasury': 'State Treasury'
            }).set_index('Step')
            st.line_chart(
                chart_data,
                color=["#10b981", "#3b82f6"],
                use_container_width=True
            )

            st.markdown('<p class="section-label">Tax Rate</p>', unsafe_allow_html=True)
            chart_data = all_history[['Step', 'TaxRate']].copy()
            chart_data['TaxRate'] = chart_data['TaxRate'] * 100
            chart_data = chart_data.rename(columns={
                'TaxRate': 'Tax Rate'
            }).set_index('Step')
            st.line_chart(
                chart_data,
                color="#F27F0D",
                use_container_width=True
            )

        st.write("")

        st.markdown('<p class="section-label">Market Price Index & Supply Ratio</p>', unsafe_allow_html=True)

        resources = safe_parse(current_row['ResourcePool'])
        prices = safe_parse(current_row['PricePool'])
        targets = safe_parse(current_row['TargetSupply'])

        price_data = []
        for key in prices.keys():
            price_data.append({
                "Commodity": key.capitalize(),
                "Market Price": f"${prices[key]:.2f}",
                "Stock": f"{resources.get(key, 0):.2f}",
                "Target Supply": f"{targets.get(key, 0):.0f}"
            })

        st.write(pd.DataFrame(price_data))

    with right_col:
        space_cols = st.columns([1, 8, 1])

        with space_cols[1]:
            st.subheader("Governance")

            st.metric(
                "Total Tax Collected",
                f"${current_row['TotalTaxCollected']:,.2f}"
            )
            st.metric(
                "Net Public Spending",
                f"${current_row['TotalPublicSpending']:,.0f}"
            )

            # Aid Fund Breakdown
            st.subheader("Aid Fund")
            aid_fund = safe_parse(current_row['AidFund'])
            if aid_fund:
                for item, amount in aid_fund.items():
                    st.markdown(f"""
                    <div class="flex justify-between items-center bg-white/5 p-2 rounded mb-1">
                        <span class="text-xs font-mono">{item.capitalize()}</span>
                        <span class="text-xs font-bold text-emerald-400">{amount:.2f} units</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No active aid disbursements.")

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<p class="section-label" style="margin-top:20px;">Supply vs Demand</p>',
                        unsafe_allow_html=True)

            # Calculate ratio
            res_keys = list(resources.keys())
            ratios = [min(100, (resources[k] / targets[k] * 100)) if targets.get(k, 0) > 0 else 0 for k in res_keys]

            health_fig = px.bar(
                x=ratios, y=[k.capitalize() for k in res_keys],
                orientation='h', color=ratios,
                color_continuous_scale='RdYlGn', range_color=[0, 100]
            )
            health_fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0), height=200,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title="% of Target Met", range=[0, 100]),
                yaxis=dict(title=None),
                coloraxis_showscale=False
            )
            st.plotly_chart(health_fig, use_container_width=True)
