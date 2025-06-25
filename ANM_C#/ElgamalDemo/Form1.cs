using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.VariantTypes;
using System.Numerics;
using System.Text;
using UglyToad.PdfPig;
using UglyToad.PdfPig.Content;

namespace ElgamalDemo
{
    public partial class Form1 : Form
    {
        ChuKySoElgamal chuKySoElgamal = new ChuKySoElgamal();
        public Form1()
        {
            InitializeComponent();
        }



        private void btnRandomPGX_Click(object sender, EventArgs e)
        {
            // Kiểm tra nếu ô txtdodaikhoa trống
            if (string.IsNullOrWhiteSpace(txtdodaikhoa.Text))
            {
                MessageBox.Show("Vui lòng nhập độ dài khóa!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return; // Thoát hàm nếu chưa nhập
            }

            // Nếu có nhập, thực hiện tiếp
            int dodaikhoa;
            if (!int.TryParse(txtdodaikhoa.Text, out dodaikhoa))
            {
                MessageBox.Show("Vui lòng nhập đúng định dạng số cho độ dài khóa!", "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Tạo khóa với độ dài nhập vào
            chuKySoElgamal.taoKhoa(dodaikhoa);
            txtSoP.Text = chuKySoElgamal.P.ToString();
            txtSoG.Text = chuKySoElgamal.G.ToString();
            txtSoA.Text = chuKySoElgamal.A.ToString();
        }


        private void btnCheckP_Click(object sender, EventArgs e)
        {
            try
            {
                BigInteger soP = BigInteger.Parse(txtSoP.Text);
                if (chuKySoElgamal.CheckP(soP))
                {
                    MessageBox.Show("Số P thoả mãn!", "Thông báo", MessageBoxButtons.OK);
                }
                else
                {
                    MessageBox.Show("Số P không hợp lệ!", "Thông báo", MessageBoxButtons.OK);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Kiểm tra lại dữ liệu nhập", "Thông báo", MessageBoxButtons.OK);
            }
        }

        private void btnCheckG_Click(object sender, EventArgs e)
        {
            try
            {
                BigInteger soP = BigInteger.Parse(txtSoP.Text);
                BigInteger soG = BigInteger.Parse(txtSoG.Text);
                if (chuKySoElgamal.CheckG(soG, soP))
                {
                    MessageBox.Show("Số G hợp lệ", "Thông báo", MessageBoxButtons.OK);
                }
                else
                {
                    MessageBox.Show("Số G không thoả mãn", "Thông báo", MessageBoxButtons.OK);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Kiểm tra lại dữ liệu nhập", "Thông báo", MessageBoxButtons.OK);
            }
        }

        private void btnCheckA_Click(object sender, EventArgs e)
        {
            try
            {
                BigInteger soA = BigInteger.Parse(txtSoA.Text);
                BigInteger soP = BigInteger.Parse(txtSoP.Text);
                if (chuKySoElgamal.CheckA(soA, soP))
                {
                    MessageBox.Show("Số A Hợp lệ", "Thông báo");
                }
                else
                {
                    MessageBox.Show("Số A không thoả mãn", "Thông báo");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Kiểm tra lại dữ liệu nhập", "Thông báo");
            }
        }

        private void btnTaoKhoa_Click(object sender, EventArgs e)
        {
            try
            {
                BigInteger soA = BigInteger.Parse(txtSoA.Text);
                BigInteger soP = BigInteger.Parse(txtSoP.Text);
                BigInteger soG = BigInteger.Parse(txtSoG.Text);
                BigInteger soY = chuKySoElgamal.ModPow(soG, soA, soP);
                if (chuKySoElgamal.CheckA(soA, soP) && chuKySoElgamal.CheckG(soG, soP) && chuKySoElgamal.CheckP(soP))
                {
                    txtPublicKey.Text = soP.ToString() + "," + soG.ToString() + "," + soY.ToString();
                    txtPrivateKey.Text = soA.ToString();
                }
                else
                {
                    MessageBox.Show("Kiểm tra lại P, G, A", "Thông báo");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Kiểm tra lại dữ liệu nhập", "Thông báo");
            }
        }

        private void btnMoFile_Click(object sender, EventArgs e)
        {
            OpenFileDialog fileKi = new OpenFileDialog();
            fileKi.Filter = "Supported Files|*.txt;*.pdf;*.docx";
            if (fileKi.ShowDialog() == DialogResult.OK)
            {
                string path = fileKi.FileName;
                string extension = Path.GetExtension(path).ToLower();
                txtFilePath.Text = path;
                if (extension == ".txt")
                {
                    rtbThongDiep.Text = File.ReadAllText(path, System.Text.Encoding.UTF8);
                    MessageBox.Show("Tệp hợp lệ!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else if (extension == ".docx")
                {
                    using (WordprocessingDocument wordDoc = WordprocessingDocument.Open(path, false))
                    {
                        var body = wordDoc.MainDocumentPart.Document.Body;
                        StringBuilder sb = new StringBuilder();

                        foreach (var paragraph in body.Elements<DocumentFormat.OpenXml.Wordprocessing.Paragraph>())
                        {
                            sb.AppendLine(paragraph.InnerText);
                        }

                        rtbThongDiep.Text = sb.ToString();
                    }
                    MessageBox.Show("Tệp hợp lệ!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else if (extension == ".pdf")
                {
                    StringBuilder sb = new StringBuilder();

                    using (PdfDocument document = PdfDocument.Open(path))
                    {
                        foreach (Page page in document.GetPages())
                        {
                            sb.AppendLine(page.Text);
                        }
                    }

                    rtbThongDiep.Text = sb.ToString();
                    MessageBox.Show("Tệp hợp lệ!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show("Tệp không hợp lệ. Vui lòng chọn tệp định dạng .txt, .pdf hoặc .docx!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    txtFilePath.Text = string.Empty;
                    rtbThongDiep.Clear();
                }
            }
        }
        private void btnMoFile1_Click(object sender, EventArgs e)
        {
            OpenFileDialog fileKi = new OpenFileDialog();
            fileKi.Filter = "Supported Files|*.txt;*.pdf;*.docx";
            if (fileKi.ShowDialog() == DialogResult.OK)
            {
                string path = fileKi.FileName;
                string extension = Path.GetExtension(path).ToLower();
                txtFilePath1.Text = path;
                if (extension == ".txt")
                {
                    rtbVanBanKT.Text = File.ReadAllText(path, System.Text.Encoding.UTF8);
                    MessageBox.Show("Tệp hợp lệ!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else if (extension == ".docx")
                {
                    using (WordprocessingDocument wordDoc = WordprocessingDocument.Open(path, false))
                    {
                        var body = wordDoc.MainDocumentPart.Document.Body;
                        StringBuilder sb = new StringBuilder();

                        foreach (var paragraph in body.Elements<DocumentFormat.OpenXml.Wordprocessing.Paragraph>())
                        {
                            sb.AppendLine(paragraph.InnerText);
                        }

                        rtbVanBanKT.Text = sb.ToString();
                    }
                    MessageBox.Show("Tệp hợp lệ!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else if (extension == ".pdf")
                {
                    StringBuilder sb = new StringBuilder();

                    using (PdfDocument document = PdfDocument.Open(path))
                    {
                        foreach (Page page in document.GetPages())
                        {
                            sb.AppendLine(page.Text);
                        }
                    }
                    rtbVanBanKT.Text = sb.ToString();
                    MessageBox.Show("Tệp hợp lệ!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show("Tệp không hợp lệ. Vui lòng chọn tệp định dạng .txt, .pdf hoặc .docx!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    txtFilePath.Text = string.Empty;
                    rtbThongDiep.Clear();
                }
            }
        }

        private void btnRandomK_Click(object sender, EventArgs e)
        {
            try
            {
                BigInteger soP = BigInteger.Parse(txtSoP.Text);
                txtSoK.Text = chuKySoElgamal.TaoK(soP).ToString();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void btnCheckK_Click(object sender, EventArgs e)
        {
            try
            {
                BigInteger soK = BigInteger.Parse(txtSoK.Text);
                BigInteger soP = BigInteger.Parse(txtSoP.Text);
                if (chuKySoElgamal.CheckK(soK, soP))
                {
                    MessageBox.Show("Số K Hợp lệ", "Thông báo");
                }
                else
                {
                    MessageBox.Show("Số K không thoả mãn", "Thông báo");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Kiểm tra lại dữ liệu nhập", "Thông báo");
            }
        }

        private void btnKy_Click(object sender, EventArgs e)
        {
            try
            {
                string[] p = txtPublicKey.Text.Split(",");
                BigInteger soP = BigInteger.Parse(p[0].Trim());
                BigInteger soG = BigInteger.Parse(p[1].Trim());
                BigInteger soY = BigInteger.Parse(p[2].Trim());
                BigInteger soA = BigInteger.Parse(txtPrivateKey.Text);
                BigInteger soK = BigInteger.Parse(txtSoK.Text);

                if (rtbThongDiep.Text == "")
                {
                    MessageBox.Show("Không được để nội dung trống!", "Thông báo");
                }
                else
                {
                    BigInteger soR = chuKySoElgamal.ky(rtbThongDiep.Text, soP, soG, soY, soA, soK).r;
                    BigInteger soS = chuKySoElgamal.ky(rtbThongDiep.Text, soP, soG, soY, soA, soK).s;

                    rtbChuKyRS.Text = soR.ToString() + "," + soS.ToString();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Kiểm tra lại khoá công khai, khoá bí mật, số K", "Thông báo");
            }
        }

        private void btnSent_Click(object sender, EventArgs e)
        {
            rtbVanBanKT.Text = rtbThongDiep.Text;
            rtbChuKyKT.Text = rtbChuKyRS.Text;
        }

        private void btnReset_Click(object sender, EventArgs e)
        {
            if (CheckReset())
            {
                MessageBox.Show("Toàn bộ dữ liệu đã được reset!", "Thông báo");
            }
            else
            {
                txtSoP.Text = "";
                txtSoG.Text = "";
                txtSoA.Text = "";
                txtPublicKey.Text = "";
                txtPrivateKey.Text = "";
                txtFilePath.Text = "";
                rtbThongDiep.Text = "";
                txtSoK.Text = "";
                rtbChuKyRS.Text = "";
                txtFilePath1.Text = "";
                rtbVanBanKT.Text = "";
                rtbChuKyKT.Text = "";
            }
        }
        public bool CheckReset()
        {
            if (txtSoP.Text == "" && txtSoG.Text == "" && txtSoA.Text == "" &&
                txtPublicKey.Text == "" && txtPrivateKey.Text == "" &&
                txtFilePath.Text == "" && rtbThongDiep.Text == "" && txtSoK.Text == "" && rtbChuKyRS.Text == "" &&
                txtFilePath1.Text == "" && rtbVanBanKT.Text == "" && rtbChuKyKT.Text == "")
            {
                return true;
            }
            return false;
        }

        private void btnKiemTra_Click(object sender, EventArgs e)
        {
            try
            {
                string[] p = txtPublicKey.Text.Split(",");
                BigInteger soP = BigInteger.Parse(p[0].Trim());
                BigInteger soG = BigInteger.Parse(p[1].Trim());
                BigInteger soY = BigInteger.Parse(p[2].Trim());

                string[] t = rtbChuKyKT.Text.Split(",");
                BigInteger soR = BigInteger.Parse(t[0].Trim());
                BigInteger soS = BigInteger.Parse(t[1].Trim());
                if (rtbChuKyKT.Text == "" || rtbVanBanKT.Text == "")
                {
                    MessageBox.Show("Nội dung kiểm tra hoặc chữ ký trống", "Thông báo");
                }
                else if (rtbThongDiep.Text != rtbVanBanKT.Text && rtbChuKyRS.Text == rtbChuKyKT.Text)
                {
                    MessageBox.Show("Thông điệp bị thay đổi, chữ kí hợp lệ", "Thông báo");
                }
                else if (rtbThongDiep.Text == rtbVanBanKT.Text && rtbChuKyRS.Text != rtbChuKyKT.Text)
                {
                    MessageBox.Show("Thông điệp hợp lệ, chữ kí bị thay đổi", "Thông báo");
                }
                else if (rtbThongDiep.Text != rtbVanBanKT.Text && rtbChuKyRS.Text != rtbChuKyKT.Text)
                {
                    MessageBox.Show("Thông điệp và chữ kí đã bị thay đổi", "Thông báo");
                }
                else
                {
                    MessageBox.Show("Thông điệp hợp lệ, chữ kí không bị thay đổi", "Thông báo");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Kiểm tra dữ liệu nhập có thể trống hoặc sai!", "Thông báo");
            }
        }

        private void btnktradodaibit_Click(object sender, EventArgs e)
        {
            if (int.TryParse(txtdodaikhoa.Text, out int value))
            {
                if (value < 256)
                {
                    MessageBox.Show("Vui lòng nhập độ dài khóa >= 256 bit", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    txtdodaikhoa.Clear();
                }
                else
                {
                    MessageBox.Show("Số bit ngẫu nhiên hợp lệ!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            else if (!string.IsNullOrEmpty(txtdodaikhoa.Text))
            {
                MessageBox.Show("Vui lòng nhập số nguyên hợp lệ!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                txtdodaikhoa.Clear();
            }
        }

        private void button1_Click(object sender, EventArgs e)

        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "Text files (*.txt)|*.txt|PDF files (*.pdf)|*.pdf|Word files (*.docx)|*.docx";
            saveFileDialog.Title = "Chọn nơi lưu file";

            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                string filePath = saveFileDialog.FileName;

                try
                {
                    string extension = Path.GetExtension(filePath).ToLower();
                    string content = rtbThongDiep.Text;

                    if (extension == ".txt")
                    {
                        File.WriteAllText(filePath, content);
                    }
                    else if (extension == ".pdf")
                    {
                        // Tạm lưu text vào file .pdf (thực chất là file text với đuôi .pdf)
                        // Nếu muốn tạo file PDF thực sự => cần dùng thư viện iTextSharp hoặc PdfSharp
                        File.WriteAllText(filePath, content);
                    }
                    else if (extension == ".docx")
                    {
                        // Tạm lưu text vào file .docx (thực chất là file text với đuôi .docx)
                        // Nếu muốn tạo file Word chuẩn => cần dùng thư viện DocX hoặc OpenXml
                        File.WriteAllText(filePath, content);
                    }
                    else
                    {
                        MessageBox.Show("Định dạng file không hỗ trợ!", "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }

                    MessageBox.Show("Đã lưu file thành công!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Lỗi khi lưu file: " + ex.Message, "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "Text files (*.txt)|*.txt|PDF files (*.pdf)|*.pdf|Word files (*.docx)|*.docx";
            saveFileDialog.Title = "Chọn nơi lưu file";

            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                string filePath = saveFileDialog.FileName;

                try
                {
                    string extension = Path.GetExtension(filePath).ToLower();
                    string content = rtbVanBanKT.Text;

                    if (extension == ".txt")
                    {
                        File.WriteAllText(filePath, content);
                    }
                    else if (extension == ".pdf")
                    {
                        // Tạm lưu text vào file .pdf (thực chất là file text với đuôi .pdf)
                        // Nếu muốn tạo file PDF thực sự => cần dùng thư viện iTextSharp hoặc PdfSharp
                        File.WriteAllText(filePath, content);
                    }
                    else if (extension == ".docx")
                    {
                        // Tạm lưu text vào file .docx (thực chất là file text với đuôi .docx)
                        // Nếu muốn tạo file Word chuẩn => cần dùng thư viện DocX hoặc OpenXml
                        File.WriteAllText(filePath, content);
                    }
                    else
                    {
                        MessageBox.Show("Định dạng file không hỗ trợ!", "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }

                    MessageBox.Show("Đã lưu file thành công!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Lỗi khi lưu file: " + ex.Message, "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void label6_Click(object sender, EventArgs e)
        {

        }

        private void label12_Click(object sender, EventArgs e)
        {

        }
    }
}
