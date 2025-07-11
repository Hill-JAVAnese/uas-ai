from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_rules(filepath=None):
    if filepath is None:
        filepath = os.path.join(BASE_DIR, "data_penyakit_manusia.csv")

    try:
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            return list(csv.DictReader(csvfile))
    except FileNotFoundError:
        print(f"Error: File {filepath} tidak ditemukan.")
        return []
    except Exception as e:
        print(f"Error saat membaca CSV: {e}")
        return []

# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #
@app.route("/", methods=["GET", "POST"])
def index():
    gejala_options = {
        "Tidak Ada": "",
        "Demam": "Demam",
        "Batuk": "Batuk",
        "Pilek": "Pilek",
        "Sakit Tenggorokan": "Sakit Tenggorokan",
        "Sakit Kepala": "Sakit Kepala",
        "Nyeri Otot": "Nyeri Otot",
        "Lemas": "Lemas",
        "Mual": "Mual",
        "Muntah": "Muntah",
        "Diare": "Diare",
        "Ruam Kulit": "Ruam Kulit",
        "Sesak Napas": "Sesak Napas",
        "Pusing": "Pusing",
        "Muncul Bintik Merah": "Muncul Bintik Merah",
        "Nyeri Sendi": "Nyeri Sendi",
        "Sakit Perut": "Sakit Perut",
        "Kembung": "Kembung",
        "Menggigil": "Menggigil",
        "Kehilangan Nafsu Makan": "Kehilangan Nafsu Makan",
        "Gatal": "Gatal",
    }

    selected_symptom_values = []
    selected_symptoms_for_display = []
    hasil_diagnosis = []
    form_submitted = False

    if request.method == "POST":
        form_submitted = True
        input_gejala_keys = ["input_gejala_1", "input_gejala_2", "input_gejala_3"]
        selected_symptom_values = [
            request.form.get(g, "").strip() 
            for g in input_gejala_keys 
            if request.form.get(g, "").strip()
        ]

        for i, val in enumerate(selected_symptom_values):
            if val: 
                selected_symptoms_for_display.append(
                    {"label": f"Gejala Pilihan {i+1}", "value": val}
                )
        
        rules = load_rules()
        if not rules:
            print("Tidak ada aturan penyakit yang dimuat. Periksa file CSV.")
            pass

        for rule in rules:
            rule_defining_symptoms = [
                rule.get(f"Gejala{i}", "").strip() for i in range(1, 4) if rule.get(f"Gejala{i}", "").strip()
            ]
            if rule_defining_symptoms and all(
                symptom_from_rule in selected_symptom_values for symptom_from_rule in rule_defining_symptoms
            ):
                is_already_added = any(h["penyakit"] == rule.get("KemungkinanPenyakit", "Tidak Diketahui") for h in hasil_diagnosis)
                if not is_already_added:
                    hasil_diagnosis.append(
                        {
                            "penyakit": rule.get("KemungkinanPenyakit", "Tidak Diketahui"),
                            "penanganan": rule.get("PenangananUmum", "Konsultasikan dengan dokter."),
                        }
                    )

    return render_template(
        "index.html",
        gejala_options=gejala_options,
        hasil_diagnosis=hasil_diagnosis,
        selected_symptoms_for_display=selected_symptoms_for_display,
        form_submitted=form_submitted,
    )

# --------------------------------------------------------------------------- #
# Main entry point
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    app.run(debug=True, port=5003)
