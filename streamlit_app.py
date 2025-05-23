import streamlit as st

st.set_page_config(page_title="Rekomendasi Makanan", page_icon="🍧", layout="centered")

# Sidebar Navigasi
page = st.sidebar.selectbox("Pilih Halaman", ["Rekomendasi Makanan", "Tentang Aplikasi"])

# Data kalori per gram makanan
calories_per_gram = {
    "Susu rendah lemak": 0.5,
    "Sayuran hijau": 0.2,
    "Protein hewani dan nabati": 1.5,
    "Karbohidrat kompleks (nasi merah, oatmeal)": 1.3,
    "Sayuran & buah segar": 0.5,
    "Protein (telur, ayam, tahu)": 1.5,
    "Makanan tinggi kalsium": 0.7,
    "Ikan berlemak (salmon, sarden)": 2.0,
    "Sayur berserat tinggi": 0.4,
    "Karbohidrat sehat (ubi, roti gandum)": 1.2,
    "Pisang": 0.9,
    "Air mineral yang cukup": 0,
    "Makanan cepat saji": 2.5,
    "Minuman bersoda": 0.4,
    "Makanan tinggi gula": 4.0,
    "Gorengan": 3.0,
    "Makanan olahan": 2.0,
    "Terlalu banyak kafein": 0,
    "Makanan asin": 1.5,
    "Daging merah berlebihan": 2.5,
    "Gula tinggi": 4.0,
    "Camilan manis": 4.0,
    "Minuman manis": 0.5,
    "Lemak jenuh": 9.0,
}

# Fungsi rekomendasi makanan
def get_food_recommendations(age, gender, activity_level, weight):
    recommended = {}
    to_avoid = {}
    adjustment_factor = weight / 60.0

    if age < 18:
        recommended.update({
            "Susu rendah lemak": 250,
            "Sayuran hijau": 100,
            "Protein hewani dan nabati": 150
        })
        to_avoid.update({
            "Makanan cepat saji": 200,
            "Minuman bersoda": 330,
            "Makanan tinggi gula": 100
        })
    elif 18 <= age <= 50:
        recommended.update({
            "Karbohidrat kompleks (nasi merah, oatmeal)": 200,
            "Sayuran & buah segar": 300,
            "Protein (telur, ayam, tahu)": 200
        })
        to_avoid.update({
            "Gorengan": 150,
            "Makanan olahan": 180,
            "Terlalu banyak kafein": 200
        })
    else:
        recommended.update({
            "Makanan tinggi kalsium": 250,
            "Ikan berlemak (salmon, sarden)": 150,
            "Sayur berserat tinggi": 200
        })
        to_avoid.update({
            "Makanan asin": 150,
            "Daging merah berlebihan": 200,
            "Gula tinggi": 100
        })

    if activity_level == "Tinggi":
        recommended.update({
            "Karbohidrat sehat (ubi, roti gandum)": 250,
            "Pisang": 120,
            "Air mineral yang cukup": 2000
        })
    elif activity_level == "Rendah":
        to_avoid.update({
            "Camilan manis": 100,
            "Minuman manis": 250,
            "Lemak jenuh": 70
        })

    final_recommended = {}
    for food in recommended:
        gram = recommended[food] * adjustment_factor
        cal = int(gram * calories_per_gram.get(food, 1))
        final_recommended[food] = {"gram": int(gram), "kalori": cal}

    final_to_avoid = {}
    for food in to_avoid:
        adjusted = to_avoid[food] * adjustment_factor
        gram = int(min(adjusted, to_avoid[food] * 1.3))
        cal = int(gram * calories_per_gram.get(food, 1))
        final_to_avoid[food] = {"gram": gram, "kalori": cal}

    return final_recommended, final_to_avoid

# Fungsi efek baik dan risiko
def generate_effects(recommended_foods, avoided_foods):
    efek_baik = []
    risiko = []

    if "Sayuran hijau" in recommended_foods or "Sayuran & buah segar" in recommended_foods:
        efek_baik.append("Meningkatkan sistem imun dan pencernaan")
    if "Protein" in "".join(recommended_foods.keys()):
        efek_baik.append("Mendukung pertumbuhan dan perbaikan sel")
    if "Karbohidrat kompleks" in recommended_foods or "Karbohidrat sehat (ubi, roti gandum)" in recommended_foods:
        efek_baik.append("Memberi energi lebih stabil sepanjang hari")
    if "Ikan berlemak (salmon, sarden)" in recommended_foods:
        efek_baik.append("Menjaga kesehatan jantung dan otak")

    if "Gorengan" in avoided_foods or "Makanan cepat saji" in avoided_foods:
        risiko.append("Risiko kolesterol tinggi dan gangguan jantung")
    if "Minuman bersoda" in avoided_foods or "Minuman manis" in avoided_foods:
        risiko.append("Meningkatkan risiko diabetes dan obesitas")
    if "Gula tinggi" in avoided_foods or "Makanan tinggi gula" in avoided_foods:
        risiko.append("Gangguan metabolisme dan resistensi insulin")
    if "Makanan asin" in avoided_foods:
        risiko.append("Peningkatan tekanan darah dan gangguan ginjal")

    return efek_baik, risiko

# Halaman utama
if page == "Rekomendasi Makanan":
    st.markdown("""
        <div style="background-color: rgba(0, 102, 204, 0.7); padding:20px; border-radius:10px; color:white; text-align:center;">
            <h2>Rekomendasi Makanan Berdasarkan Aktivitas & Usia</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Masukkan Data Anda")

    age = st.number_input("Masukkan umur Anda (tahun)", min_value=1, max_value=100)
    weight = st.number_input("Masukkan berat badan Anda (kg)", min_value=1.0, max_value=200.0, step=0.1)
    gender = st.selectbox("Pilih jenis kelamin", ["Pria", "Wanita"])
    activity_level = st.selectbox("Tingkat aktivitas fisik Anda", ["Rendah", "Sedang", "Tinggi"])

    if st.button("Tampilkan Rekomendasi"):
        good_foods, avoid_foods = get_food_recommendations(age, gender, activity_level, weight)
        efek_baik, risiko = generate_effects(good_foods, avoid_foods)

        # Kebutuhan kalori
        if gender == "Pria":
            bmr = 10 * weight + 6.25 * 170 - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * 160 - 5 * age - 161

        if activity_level == "Rendah":
            kebutuhan_kalori = bmr * 1.2
        elif activity_level == "Sedang":
            kebutuhan_kalori = bmr * 1.55
        else:
            kebutuhan_kalori = bmr * 1.725

        st.subheader("🔥 Kebutuhan Kalori Harian Anda")
        st.markdown(f"""
            <div style="background-color: rgba(255, 165, 0, 0.3); padding: 15px; border-radius: 10px; color: black;">
                Perkiraan kebutuhan energi Anda adalah <b>{int(kebutuhan_kalori)} kalori per hari</b>.
            </div>
            """, unsafe_allow_html=True)

        # Tampilan semua makanan direkomendasikan dalam satu box biru
        rekomendasi_html = "<ul style='margin-left: 1em;'>"
        for f, v in good_foods.items():
            rekomendasi_html += f"<li><strong>{f}</strong>: {v['gram']} gram ({v['kalori']} kalori)</li>"
        rekomendasi_html += "</ul>"

        st.markdown(f"""
            <div style="background-color:#cce5ff; padding:20px; border-radius:10px;">
                <h4>Makanan yang Direkomendasikan:</h4>
                {rekomendasi_html}
            </div>
            """, unsafe_allow_html=True)

        # Tampilan semua makanan yang dihindari dalam satu box merah
        hindari_html = "<ul style='margin-left: 1em;'>"
        for f, v in avoid_foods.items():
            hindari_html += f"<li><strong>{f}</strong>: {v['gram']} gram ({v['kalori']} kalori)</li>"
        hindari_html += "</ul>"

        st.markdown(f"""
            <div style="background-color:#f8d7da; padding:20px; border-radius:10px; margin-top:20px;">
                <h4>Makanan yang Sebaiknya Dihindari:</h4>
                {hindari_html}
            </div>
            """, unsafe_allow_html=True)

        # Efek Baik
        if efek_baik:
            st.subheader("🌿 Efek Baik Jika Mengonsumsi Makanan yang Direkomendasikan:")
            st.markdown(f"""
                <div style="background-color: rgba(0, 153, 76, 0.2); padding: 15px; border-radius: 10px; color: black;">
                    {"<br>".join(["- " + item for item in efek_baik])}
                </div>
                """, unsafe_allow_html=True)

        # Risiko
        if risiko:
            st.subheader("⚠️ Risiko Jika Tidak Menghindari Makanan Tersebut:")
            st.markdown(f"""
                <div style="background-color: rgba(255, 204, 0, 0.2); padding: 15px; border-radius: 10px; color: black;">
                    {"<br>".join(["- " + item for item in risiko])}
                </div>
                """, unsafe_allow_html=True)

# Halaman Tentang
elif page == "Tentang Aplikasi":
    st.title("Tentang Aplikasi")
    st.markdown("""
    Aplikasi **Rekomendasi Makanan Berdasarkan Aktivitas & Usia** dibuat untuk memberikan panduan sederhana mengenai pola makan sehat berdasarkan kondisi individu.

    - Berdasarkan data umur, berat badan, dan aktivitas fisik
    - Rekomendasi bersifat umum dan bukan pengganti nasihat medis profesional

    💡 Dibuat dengan Streamlit oleh:
    - Rio Surya T
    - Trio Agung
    - Hazlia Mulya
    - M Rizqi
    - Bunga Sekar
    """)
