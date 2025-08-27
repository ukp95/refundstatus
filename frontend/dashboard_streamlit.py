import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="SabPaisa DJB Refund Dashboard", layout="wide", page_icon="💸")

# Custom colored SabPaisa heading
st.markdown(
    """
    <div style='text-align:center; margin-top:1.5em; margin-bottom:1.5em;'>
        <span style="font-family:'Poppins',Arial,sans-serif;font-size:2.7em;font-weight:800;letter-spacing:1.5px;">
            <span style="color:#ff9800;">Sab</span><span style="color:#3d3dd7;">Paisa</span>
            <span style="color:#0a3c7d;"> DJB Refund Dashboard</span>
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .stButton>button {background: linear-gradient(90deg, #0a3c7d 60%, #00b386 100%); color: #fff; font-weight: 700; border-radius: 8px;}
    .stTextInput>div>input {border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

API = "http://localhost:8000"

st.sidebar.header("Upload & Search")

# Upload Excel
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx", "xls"])
if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    with st.spinner("Uploading..."):
        try:
            r = requests.post(f"{API}/upload-excel/", files=files)
            if r.ok:
                st.sidebar.success("Excel uploaded successfully!")
            else:
                st.sidebar.error(r.json().get("detail", "Upload failed"))
        except Exception as e:
            st.sidebar.error(f"Upload failed: {e}")

# Search Transactions
st.header("Search Transactions")
col1, col2, col3 = st.columns(3)
with col1:
    spTransId = st.text_input("Transaction ID", key="spTransId")
with col2:
    clienttransId = st.text_input("clienttransId", key="clienttransId")
with col3:
    firm = st.text_input("Bidding Firm Name", key="firm")

if st.button("Search"):
    params = {}
    if spTransId: params["spTransId"] = spTransId
    if clienttransId: params["clienttransId"] = clienttransId
    if firm: params["Bidding_Firm_Name"] = firm
    with st.spinner("Searching..."):
        try:
            r = requests.get(f"{API}/search/", params=params)
            if r.ok:
                data = r.json()
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                    st.success(f"Total Results: {len(df)}")
                    # Download buttons
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download CSV", csv, "Refund_Search_Results.csv", "text/csv")
                    excel = io.BytesIO()
                    df.to_excel(excel, index=False)
                    st.download_button("Download Excel", excel.getvalue(), "Refund_Search_Results.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                else:
                    st.warning("No results.")
            else:
                st.error("Search failed: " + r.text)
        except Exception as e:
            st.error(f"Search failed: {e}")

# Generate Receipt
st.header("Generate Receipt")
receipt_id = st.text_input("Enter Transaction ID for Receipt", key="receiptTransId")
if st.button("Generate Receipt"):
    if not receipt_id:
        st.warning("Please enter a Transaction ID")
    else:
        with st.spinner("Fetching receipt..."):
            try:
                r = requests.get(f"{API}/search/", params={"spTransId": receipt_id})
                if r.ok:
                    data = r.json()
                    if data:
                        row = data[0]
                        st.subheader("Payment Receipt")
                        # Format as HTML table
                        def format_receipt_html(row):
                            html = """
                            <div style='max-width:480px;margin:0 auto;border:2px solid #0a3c7d;border-radius:12px;padding:1.5em 1.2em 1.2em 1.2em;background:#fff;box-shadow:0 2px 16px #0a3c7d22;'>
                                <div style='text-align:center;font-size:1.5em;font-weight:700;color:#0a3c7d;margin-bottom:0.5em;'>SabPaisa DJB Refund Receipt</div>
                                <table style='width:100%;border-collapse:collapse;'>
                        """
                            for k, v in row.items():
                                html += f"<tr><td style='font-weight:600;color:#0a3c7d;padding:0.5em 0.7em;border-bottom:1px solid #e0e6ed;'>{k}</td><td style='padding:0.5em 0.7em;border-bottom:1px solid #e0e6ed;color:#333;'>{v}</td></tr>"
                            html += """
                                </table>
                                <div style='text-align:center;margin-top:1.2em;font-size:1em;color:#555;'>Thank you for using SabPaisa!</div>
                            </div>
                        """
                            return html

                        receipt_html = format_receipt_html(row)
                        st.markdown(receipt_html, unsafe_allow_html=True)

                        # PDF download using fpdf
                        from fpdf import FPDF
                        import tempfile
                        import os
                        # Download DejaVuSans.ttf from https://github.com/dejavu-fonts/dejavu-fonts/blob/master/ttf/DejaVuSans.ttf
                        # and place it in the same directory as this script (frontend/)
                        FONT_PATH = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
                        class PDF(FPDF):
                            def header(self):
                                self.set_fill_color(10, 60, 125)
                                self.rect(0, 0, 210, 20, 'F')
                                self.set_font('DejaVu', 'B', 16)
                                self.set_text_color(255,255,255)
                                self.cell(0, 12, 'SabPaisa Payment Receipt', 0, 1, 'C')
                                self.ln(2)
                            def footer(self):
                                self.set_y(-20)
                                self.set_font('DejaVu', 'I', 10)
                                self.set_text_color(0,179,134)
                                self.cell(0, 10, 'Thank you for using SabPaisa!', 0, 1, 'C')
                                self.set_text_color(120,120,120)
                                self.cell(0, 8, 'For support: +91 6201791054 | sabpaisa@srslive.in', 0, 0, 'C')

                        pdf = PDF()
                        pdf.add_page()
                        pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
                        pdf.add_font('DejaVu', 'B', FONT_PATH, uni=True)
                        pdf.add_font('DejaVu', 'I', FONT_PATH, uni=True)
                        pdf.set_font('DejaVu', '', 12)
                        pdf.set_text_color(10,60,125)
                        for k, v in row.items():
                            pdf.cell(60, 10, str(k), 1, 0, 'L', False)
                            pdf.set_text_color(60,60,60)
                            pdf.cell(120, 10, str(v), 1, 1, 'L', False)
                            pdf.set_text_color(10,60,125)

                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                            pdf.output(tmp_pdf.name, "F")
                            tmp_pdf.flush()
                            with open(tmp_pdf.name, "rb") as f:
                                st.download_button("Download Receipt as PDF", f, file_name="Receipt.pdf", mime="application/pdf")
                    else:
                        st.warning("Transaction not found.")
                else:
                    st.error("Error generating receipt: " + r.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown("<div style='text-align:center;color:#0a3c7d;font-weight:600;'>Helpline: <a href='tel:+916201791054' style='color:#0a3c7d;text-decoration:none;'>+91 6201791054</a> | Email: <a href='mailto:sabpaisa@srslive.in' style='color:#0a3c7d;text-decoration:none;'>sabpaisa@srslive.in</a></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;color:#0a3c7d;font-size:1em;font-weight:600;letter-spacing:0.5px;'>&copy; 2025 SabPaisa. All Rights Reserved.</div>", unsafe_allow_html=True)
