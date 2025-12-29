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

    # Safe Parses
    current_row['EconomyMetrics'] = safe_parse(current_row['EconomyMetrics'])
    prev_row['EconomyMetrics'] = safe_parse(prev_row['EconomyMetrics'])

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
            delta_value = current_row['EconomyMetrics'].get('gdp', 0.0) - prev_row['EconomyMetrics'].get('gdp', 0.0)
            st.metric(
                "GDP",
                f"${current_row['EconomyMetrics'].get('gdp', 0.0):,.2f}",
                delta=f"{delta_value:,.2f}" if delta_value != 0 else None
            )
        with kpi[1]:
            delta_value = current_row['TotalAgentWealth'] - prev_row['TotalAgentWealth']
            st.metric(
                "Global Wealth",
                f"${current_row['TotalAgentWealth']:,.2f}",
                delta=f"{delta_value:,.2f}" if delta_value != 0 else None
            )
        with kpi[2]:
            delta_value = current_row['EconomyWealth'] - prev_row['EconomyWealth']
            st.metric(
                "Economy Wealth",
                f"${current_row['EconomyWealth']:,.2f}",
                delta=f"{delta_value:,.2f}" if delta_value != 0 else None
            )
        with kpi[3]:
            delta_value = current_row['Treasury'] - prev_row['Treasury']
            st.metric(
                "State Treasury",
                f"${current_row['Treasury']:,.2f}",
                delta=f"{delta_value:,.2f}" if delta_value != 0 else None
            )

        kpi = st.columns(4)

        with kpi[0]:
            delta_value = current_row['EconomyMetrics'].get('growth', 0.0) - prev_row['EconomyMetrics'].get('growth', 0.0)
            grow_pct = current_row['EconomyMetrics'].get('growth', 0.0)
            st.metric(
                "Growth",
                f"{grow_pct}" if abs(grow_pct) != 0.0 else "0.0",
                delta=f"{delta_value:,.3f}" if delta_value != 0 else None
            )
        with kpi[1]:
            delta_value = current_row['EconomyMetrics'].get('inflation', 0.0) - prev_row['EconomyMetrics'].get('inflation', 0.0)
            inf_pct = current_row['EconomyMetrics'].get('inflation', 0.0)
            st.metric(
                "Inflation",
                f"{inf_pct}" if abs(inf_pct) != 0.0 else "0.0",
                delta=f"{delta_value:,.3f}" if delta_value != 0 else None
            )
        with kpi[2]:
            delta_value = (current_row['TaxRate'] - prev_row['TaxRate']) * 100
            tax_pct = current_row['TaxRate'] * 100
            st.metric(
                "Current Tax Rate",
                f"{tax_pct:.2f}%" if tax_pct != 0 else "0%",
                delta=f"{delta_value:,.2f}%" if delta_value != 0 else None
            )

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
                color=["#10b981", "#3b82f6"]
            )

            st.markdown('<p class="section-label">Tax Rate</p>', unsafe_allow_html=True)
            chart_data = all_history[['Step', 'TaxRate']].copy()
            chart_data['TaxRate'] = chart_data['TaxRate'] * 100
            chart_data = chart_data.rename(columns={
                'TaxRate': 'Tax Rate'
            }).set_index('Step')
            st.line_chart(
                chart_data,
                color="#F27F0D"
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

            res_keys = list(resources.keys())

            for k in res_keys:
                val = resources[k]
                target = targets.get(k, 0)
                ratio = min(1.0, val / target) if target > 0 else 0

                col1, col2 = st.columns([4, 1])
                col1.write(f"**{k.capitalize()}**")
                col2.write(f"{int(ratio * 100)}%")

                st.progress(ratio)
