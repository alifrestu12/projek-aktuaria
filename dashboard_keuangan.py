import streamlit as st
import plotly.graph_objects as go
import math

# ══════════════════════════════════════════════════════════
#  DASHBOARD KEUANGAN — Proyeksi Pensiun + Kalkulator Kredit
# ══════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Dashboard Keuangan Cerdas",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* Root variables */
:root {
    --blue: #4361ee;
    --cyan: #0ea5e9;
    --emerald: #10b981;
    --amber: #f59e0b;
    --rose: #ef4444;
    --purple: #8b5cf6;
    --pink: #ec4899;
    --orange: #f97316;
}

/* Hide streamlit default stuff */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main background */
.stApp { background: #f8f9fe; }

/* Masthead */
.masthead {
    background: white;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    border: 1px solid #e6eaf4;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
}
.masthead-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: .7rem;
    letter-spacing: .15em;
    color: #8b5cf6;
    text-transform: uppercase;
    margin-bottom: .3rem;
}
.masthead h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(1.4rem, 3vw, 2rem);
    font-weight: 800;
    line-height: 1.15;
    color: #1a1a2e;
    margin: 0;
}
.masthead h1 span {
    background: linear-gradient(135deg, #8b5cf6, #4361ee, #0ea5e9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.masthead-sub {
    margin-top: .4rem;
    font-size: .85rem;
    color: #6b7a8f;
    line-height: 1.6;
}
.badges { display: flex; gap: .6rem; flex-wrap: wrap; margin-top: .3rem; }
.badge {
    font-size: .72rem; font-weight: 600;
    padding: .4rem .9rem; border-radius: 20px;
}
.badge-purple { background: #f5f3ff; color: #8b5cf6; }
.badge-pink   { background: #fdf2f8; color: #ec4899; }

/* Stat cards */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: .9rem;
    margin-bottom: 1.5rem;
}
.stat-card {
    background: #f0f2f9;
    border: 1px solid #e6eaf4;
    border-radius: 12px;
    padding: 1.2rem;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.stat-lbl {
    font-size: .7rem; font-weight: 500;
    text-transform: uppercase; letter-spacing: .06em;
    color: #6b7a8f; margin-bottom: .4rem;
}
.stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem; font-weight: 700;
    line-height: 1.3; word-break: break-word;
}
.s-blue::before { background: #4361ee; }
.s-blue .stat-val { color: #4361ee; }
.s-cyan::before { background: #0ea5e9; }
.s-cyan .stat-val { color: #0ea5e9; }
.s-emerald::before { background: #10b981; }
.s-emerald .stat-val { color: #10b981; }
.s-rose::before { background: #ef4444; }
.s-rose .stat-val { color: #ef4444; }
.s-amber::before { background: #f59e0b; }
.s-amber .stat-val { color: #f59e0b; }
.s-purple::before { background: #8b5cf6; }
.s-purple .stat-val { color: #8b5cf6; }
.s-pink::before { background: #ec4899; }
.s-pink .stat-val { color: #ec4899; }

.stat-full { grid-column: 1/-1; }

/* Result heading */
.result-hd {
    font-family: 'Syne', sans-serif;
    font-weight: 700; font-size: 1.2rem;
    margin-bottom: 1.2rem;
    padding-bottom: .8rem;
    border-bottom: 2px solid #e6eaf4;
    color: #1a1a2e;
}
.result-hd small {
    font-family: 'Inter', sans-serif;
    font-size: .7rem; font-weight: 400;
    color: #6b7a8f; text-transform: uppercase;
    letter-spacing: .06em; margin-left: .8rem;
}

/* Card wrapper */
.section-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    border: 1px solid #e6eaf4;
}

/* Streamlit element customization */
div[data-testid="stTabs"] [role="tab"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: .9rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: Format Rupiah ──────────────────────────────────
def fmt(n: float) -> str:
    if n >= 1e12:
        return f"Rp {n/1e12:.2f} T"
    if n >= 1e9:
        return f"Rp {n/1e9:.2f} M"
    if n >= 1e6:
        return f"Rp {n/1e6:.2f} Jt"
    return f"Rp {n:,.0f}".replace(",", ".")


# ── Helper: Proyeksi Pensiun ───────────────────────────────
def proyeksi_pensiun(modal, tambahan, rate, tahun, rutin):
    rows = []
    aset = modal
    setor = modal
    for t in range(tahun + 1):
        rows.append({"t": t, "aset": round(aset), "modal": round(setor), "untung": round(aset - setor)})
        if t < tahun:
            aset = aset * (1 + rate)
            if rutin:
                aset += tambahan
                setor += tambahan
    return rows


# ── Helper: Kalkulator Kredit ──────────────────────────────
def kalkulator_kredit(pokok, rate_thn, bulan, jenis):
    rate = rate_thn / 12 / 100
    rows = []
    sisa = pokok
    total_bunga = 0

    if jenis == "anuitas":
        if rate > 0:
            angsuran = pokok * rate * (1 + rate)**bulan / ((1 + rate)**bulan - 1)
        else:
            angsuran = pokok / bulan
        for b in range(1, bulan + 1):
            bunga_b = sisa * rate
            pokok_b = angsuran - bunga_b
            sisa -= pokok_b
            total_bunga += bunga_b
            rows.append({
                "b": b,
                "angsuran": round(angsuran),
                "pokok": round(pokok_b),
                "bunga": round(bunga_b),
                "sisa": round(max(sisa, 0))
            })
    else:  # pokok_tetap
        pokok_b = pokok / bulan
        for b in range(1, bulan + 1):
            bunga_b = sisa * rate
            angsuran = pokok_b + bunga_b
            sisa -= pokok_b
            total_bunga += bunga_b
            rows.append({
                "b": b,
                "angsuran": round(angsuran),
                "pokok": round(pokok_b),
                "bunga": round(bunga_b),
                "sisa": round(max(sisa, 0))
            })

    return {"rows": rows, "total_bunga": round(total_bunga)}


# ── Masthead ───────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div>
    <p class="masthead-tag">✦ financial dashboard</p>
    <h1>Manajemen<br><span>Keuangan Cerdas</span></h1>
    <p class="masthead-sub">Proyeksi pensiun &amp; kalkulator kredit dalam satu platform modern.</p>
  </div>
  <div>
    <div class="badges">
      <span class="badge badge-purple">📈 Proyeksi Pensiun</span>
      <span class="badge badge-pink">🏦 Kalkulator Kredit</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────
tab_pensiun, tab_kredit = st.tabs(["📈  Proyeksi Pensiun", "🏦  Kalkulator Kredit"])


# ════════════════════════════════════════════════════════════
#  TAB 1 — PROYEKSI PENSIUN
# ════════════════════════════════════════════════════════════
with tab_pensiun:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Data Proyeksi Pensiun")

    col1, col2 = st.columns(2)

    with col1:
        nama = st.text_input("Nama Lengkap *", placeholder="cth. Budi Santoso", key="p_nama")
        usia_skrg = st.number_input("Usia Sekarang *", min_value=18, max_value=80, value=30, step=1, key="p_usia_skrg")
        rate_pct = st.number_input("Return Tahunan (%) *", min_value=0.0, max_value=100.0, value=8.0, step=0.1, key="p_rate")

    with col2:
        usia_pensiun = st.number_input("Target Usia Pensiun *", min_value=20, max_value=100, value=55, step=1, key="p_usia_pensiun")
        nominal = st.number_input("Modal Investasi Awal (Rp) *", min_value=0.0, value=50_000_000.0, step=1_000_000.0, format="%.0f", key="p_nominal")

    rutin = st.radio("Rutin Investasi Setiap Tahun?", ["✅ Ya, rutin", "❌ Tidak"], index=1, horizontal=True, key="p_rutin")
    tambahan = 0.0
    if rutin.startswith("✅"):
        tambahan = st.number_input("Tambahan Investasi per Tahun (Rp) *", min_value=0.0, value=12_000_000.0, step=1_000_000.0, format="%.0f", key="p_tambahan")

    hitung_pensiun = st.button("Hitung Proyeksi Pensiun →", type="primary", use_container_width=True, key="btn_pensiun")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Validasi & Kalkulasi ──────────────────────────────
    if hitung_pensiun:
        errors = []
        if not nama.strip():
            errors.append("Nama tidak boleh kosong.")
        if usia_pensiun <= usia_skrg:
            errors.append("Usia pensiun harus lebih besar dari usia sekarang.")
        if nominal <= 0:
            errors.append("Modal awal harus lebih dari 0.")
        if rutin.startswith("✅") and tambahan <= 0:
            errors.append("Tambahan investasi harus lebih dari 0.")

        if errors:
            for e in errors:
                st.error(f"⚠ {e}")
        else:
            tahun = usia_pensiun - usia_skrg
            rows = proyeksi_pensiun(nominal, tambahan, rate_pct / 100, tahun, rutin.startswith("✅"))
            last = rows[-1]

            # Stat cards
            st.markdown(f"""
            <div class="result-hd">
                Proyeksi — {nama.upper()}
                <small>{tahun} tahun menuju pensiun</small>
            </div>
            <div class="stat-row">
                <div class="stat-card s-blue">
                    <div class="stat-lbl">Total Aset Pensiun</div>
                    <div class="stat-val">{fmt(last['aset'])}</div>
                </div>
                <div class="stat-card s-cyan">
                    <div class="stat-lbl">Total Modal Disetor</div>
                    <div class="stat-val">{fmt(last['modal'])}</div>
                </div>
                <div class="stat-card s-emerald">
                    <div class="stat-lbl">Total Keuntungan</div>
                    <div class="stat-val">{fmt(last['untung'])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Chart
            labels = [f"Thn {r['t']}" for r in rows]
            aset_data   = [r['aset']   for r in rows]
            modal_data  = [r['modal']  for r in rows]
            untung_data = [r['untung'] for r in rows]

            chart_type = st.radio(
                "Tampilan Grafik",
                ["📈 Garis", "📊 Batang", "🌊 Area"],
                horizontal=True, key="p_chart_type"
            )

            fig = go.Figure()

            if chart_type == "📊 Batang":
                fig.add_trace(go.Bar(name="Total Aset",    x=labels, y=aset_data,   marker_color="#4361ee", opacity=0.85))
                fig.add_trace(go.Bar(name="Modal Disetor", x=labels, y=modal_data,  marker_color="#0ea5e9", opacity=0.85))
                fig.add_trace(go.Bar(name="Keuntungan",    x=labels, y=untung_data, marker_color="#10b981", opacity=0.85))
                fig.update_layout(barmode="group")
            elif chart_type == "🌊 Area":
                fig.add_trace(go.Scatter(name="Total Aset",    x=labels, y=aset_data,   fill="tozeroy", mode="lines", line=dict(color="#4361ee", width=3), fillcolor="rgba(67,97,238,0.15)"))
                fig.add_trace(go.Scatter(name="Modal Disetor", x=labels, y=modal_data,  fill="tozeroy", mode="lines", line=dict(color="#0ea5e9", width=2, dash="dash"), fillcolor="rgba(14,165,233,0.10)"))
                fig.add_trace(go.Scatter(name="Keuntungan",    x=labels, y=untung_data, fill="tozeroy", mode="lines", line=dict(color="#10b981", width=2), fillcolor="rgba(16,185,129,0.10)"))
            else:
                fig.add_trace(go.Scatter(name="Total Aset",    x=labels, y=aset_data,   mode="lines+markers", line=dict(color="#4361ee", width=3), marker=dict(size=6)))
                fig.add_trace(go.Scatter(name="Modal Disetor", x=labels, y=modal_data,  mode="lines+markers", line=dict(color="#0ea5e9", width=2, dash="dash"), marker=dict(size=5)))
                fig.add_trace(go.Scatter(name="Keuntungan",    x=labels, y=untung_data, mode="lines+markers", line=dict(color="#10b981", width=2), marker=dict(size=5)))

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#f0f2f9",
                font=dict(family="Inter, sans-serif", color="#6b7a8f"),
                height=380,
                margin=dict(l=0, r=0, t=20, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(tickformat=",.0f", gridcolor="rgba(230,234,244,0.8)"),
                xaxis=dict(gridcolor="rgba(230,234,244,0.8)"),
                hovermode="x unified",
            )
            fig.update_traces(
                hovertemplate="%{y:,.0f}<extra>%{fullData.name}</extra>"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Tabel ringkasan per 5 tahun
            with st.expander("📋 Lihat Tabel Proyeksi Lengkap"):
                import pandas as pd
                df = pd.DataFrame(rows)
                df.columns = ["Tahun", "Total Aset (Rp)", "Modal Disetor (Rp)", "Keuntungan (Rp)"]
                df["Total Aset (Rp)"]   = df["Total Aset (Rp)"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
                df["Modal Disetor (Rp)"] = df["Modal Disetor (Rp)"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
                df["Keuntungan (Rp)"]   = df["Keuntungan (Rp)"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
                st.dataframe(df, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
#  TAB 2 — KALKULATOR KREDIT
# ════════════════════════════════════════════════════════════
with tab_kredit:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Data Pengajuan Kredit")

    col1, col2 = st.columns(2)

    with col1:
        nama_kredit = st.text_input("Nama Peminjam *", placeholder="cth. Andi Wijaya", key="k_nama")
        pokok = st.number_input("Jumlah Kredit / Pokok (Rp) *", min_value=0.0, value=500_000_000.0, step=10_000_000.0, format="%.0f", key="k_pokok")
        tenor = st.number_input("Tenor (tahun) *", min_value=1, max_value=30, value=5, step=1, key="k_tenor")

    with col2:
        tujuan = st.text_input("Tujuan Kredit", placeholder="cth. Renovasi Rumah", value="Konsumtif", key="k_tujuan")
        rate_kredit = st.number_input("Suku Bunga Tahunan (%) *", min_value=0.0, max_value=100.0, value=12.0, step=0.1, key="k_rate")

    jenis = st.radio(
        "Jenis Pembayaran",
        ["📊 Anuitas (angsuran tetap)", "📉 Pokok Tetap (angsuran menurun)"],
        horizontal=True, key="k_jenis"
    )
    jenis_val = "anuitas" if jenis.startswith("📊") else "pokok_tetap"

    hitung_kredit = st.button("Hitung Simulasi Kredit →", type="primary", use_container_width=True, key="btn_kredit")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Validasi & Kalkulasi ──────────────────────────────
    if hitung_kredit:
        errors = []
        if not nama_kredit.strip():
            errors.append("Nama peminjam tidak boleh kosong.")
        if pokok <= 0:
            errors.append("Jumlah kredit harus lebih dari 0.")
        if tenor < 1:
            errors.append("Tenor minimal 1 tahun.")

        if errors:
            for e in errors:
                st.error(f"⚠ {e}")
        else:
            bulan = tenor * 12
            hasil = kalkulator_kredit(pokok, rate_kredit, bulan, jenis_val)
            rows = hasil["rows"]
            total_bunga = hasil["total_bunga"]
            total_bayar = pokok + total_bunga
            angsuran_pertama = rows[0]["angsuran"]
            label_angsuran = "Tetap per Bulan" if jenis_val == "anuitas" else "Pertama per Bulan"

            # Stat cards
            st.markdown(f"""
            <div class="result-hd">
                Simulasi Kredit — {nama_kredit.upper()}
                <small>{bulan} bulan · {tujuan}</small>
            </div>
            <div class="stat-row">
                <div class="stat-card s-rose">
                    <div class="stat-lbl">Total Kredit (Pokok)</div>
                    <div class="stat-val">{fmt(pokok)}</div>
                </div>
                <div class="stat-card s-amber">
                    <div class="stat-lbl">Total Bunga</div>
                    <div class="stat-val">{fmt(total_bunga)}</div>
                </div>
                <div class="stat-card s-purple">
                    <div class="stat-lbl">Total Pembayaran</div>
                    <div class="stat-val">{fmt(total_bayar)}</div>
                </div>
            </div>
            <div class="stat-row">
                <div class="stat-card s-pink stat-full">
                    <div class="stat-lbl">Angsuran {label_angsuran}</div>
                    <div class="stat-val">{fmt(angsuran_pertama)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Chart
            labels_k = [f"Bln {r['b']}" for r in rows]
            sisa_data    = [r["sisa"]    for r in rows]
            bunga_data   = [r["bunga"]   for r in rows]
            pokok_b_data = [r["pokok"]   for r in rows]

            chart_type_k = st.radio(
                "Tampilan Grafik",
                ["📈 Garis", "📊 Batang", "🌊 Area"],
                horizontal=True, key="k_chart_type"
            )

            fig2 = go.Figure()

            if chart_type_k == "📊 Batang":
                fig2.add_trace(go.Bar(name="Sisa Kredit",    x=labels_k, y=sisa_data,    marker_color="#ef4444", opacity=0.85))
                fig2.add_trace(go.Bar(name="Bunga Bulanan",  x=labels_k, y=bunga_data,   marker_color="#f59e0b", opacity=0.85))
                fig2.add_trace(go.Bar(name="Pokok Bulanan",  x=labels_k, y=pokok_b_data, marker_color="#0ea5e9", opacity=0.85))
                fig2.update_layout(barmode="group")
            elif chart_type_k == "🌊 Area":
                fig2.add_trace(go.Scatter(name="Sisa Kredit",   x=labels_k, y=sisa_data,    fill="tozeroy", mode="lines", line=dict(color="#ef4444", width=3), fillcolor="rgba(239,68,68,0.15)"))
                fig2.add_trace(go.Scatter(name="Bunga Bulanan", x=labels_k, y=bunga_data,   fill="tozeroy", mode="lines", line=dict(color="#f59e0b", width=2), fillcolor="rgba(245,158,11,0.10)"))
                fig2.add_trace(go.Scatter(name="Pokok Bulanan", x=labels_k, y=pokok_b_data, fill="tozeroy", mode="lines", line=dict(color="#0ea5e9", width=2), fillcolor="rgba(14,165,233,0.10)"))
            else:
                fig2.add_trace(go.Scatter(name="Sisa Kredit",   x=labels_k, y=sisa_data,    mode="lines+markers", line=dict(color="#ef4444", width=3), marker=dict(size=5)))
                fig2.add_trace(go.Scatter(name="Bunga Bulanan", x=labels_k, y=bunga_data,   mode="lines+markers", line=dict(color="#f59e0b", width=2, dash="dash"), marker=dict(size=4)))
                fig2.add_trace(go.Scatter(name="Pokok Bulanan", x=labels_k, y=pokok_b_data, mode="lines+markers", line=dict(color="#0ea5e9", width=2), marker=dict(size=4)))

            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#f0f2f9",
                font=dict(family="Inter, sans-serif", color="#6b7a8f"),
                height=380,
                margin=dict(l=0, r=0, t=20, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(tickformat=",.0f", gridcolor="rgba(230,234,244,0.8)"),
                xaxis=dict(gridcolor="rgba(230,234,244,0.8)"),
                hovermode="x unified",
            )
            fig2.update_traces(
                hovertemplate="%{y:,.0f}<extra>%{fullData.name}</extra>"
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Tabel amortisasi
            with st.expander("📋 Lihat Tabel Amortisasi Lengkap"):
                import pandas as pd
                df2 = pd.DataFrame(rows)
                df2.columns = ["Bulan", "Angsuran (Rp)", "Pokok (Rp)", "Bunga (Rp)", "Sisa Kredit (Rp)"]
                for col in ["Angsuran (Rp)", "Pokok (Rp)", "Bunga (Rp)", "Sisa Kredit (Rp)"]:
                    df2[col] = df2[col].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
                st.dataframe(df2, use_container_width=True, hide_index=True)


# ── Footer ─────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding-top:1.5rem;
     border-top:1px solid #e6eaf4; font-size:.7rem; color:#9aa8b9;
     letter-spacing:.06em; font-family:'Inter',sans-serif;">
  © 2025 · Dashboard Keuangan Cerdas · Dibuat dengan ❤️
</div>
""", unsafe_allow_html=True)
