namespace ElgamalDemo
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            groupBox1 = new GroupBox();
            groupBox4 = new GroupBox();
            label6 = new Label();
            button2 = new Button();
            btnKiemTra = new Button();
            rtbChuKyKT = new RichTextBox();
            label11 = new Label();
            rtbVanBanKT = new RichTextBox();
            btnMoFile1 = new Button();
            txtFilePath1 = new TextBox();
            label10 = new Label();
            groupBox3 = new GroupBox();
            label13 = new Label();
            button1 = new Button();
            btnReset = new Button();
            btnKy = new Button();
            btnSent = new Button();
            rtbChuKyRS = new RichTextBox();
            label9 = new Label();
            btnRandomK = new Button();
            btnCheckK = new Button();
            txtSoK = new TextBox();
            label8 = new Label();
            txtFilePath = new TextBox();
            rtbThongDiep = new RichTextBox();
            btnMoFile = new Button();
            label7 = new Label();
            groupBox2 = new GroupBox();
            btnktradodaibit = new Button();
            txtdodaikhoa = new TextBox();
            label12 = new Label();
            btnTaoKhoa = new Button();
            txtPrivateKey = new TextBox();
            txtPublicKey = new TextBox();
            label5 = new Label();
            label4 = new Label();
            btnRandomPGX = new Button();
            btnCheckA = new Button();
            txtSoA = new TextBox();
            label3 = new Label();
            btnCheckG = new Button();
            txtSoG = new TextBox();
            label2 = new Label();
            btnCheckP = new Button();
            txtSoP = new TextBox();
            label1 = new Label();
            openFileDialog1 = new OpenFileDialog();
            openFileDialog2 = new OpenFileDialog();
            backgroundWorker1 = new System.ComponentModel.BackgroundWorker();
            backgroundWorker2 = new System.ComponentModel.BackgroundWorker();
            groupBox1.SuspendLayout();
            groupBox4.SuspendLayout();
            groupBox3.SuspendLayout();
            groupBox2.SuspendLayout();
            SuspendLayout();
            // 
            // groupBox1
            // 
            groupBox1.Controls.Add(groupBox4);
            groupBox1.Controls.Add(groupBox3);
            groupBox1.Controls.Add(groupBox2);
            groupBox1.Location = new Point(14, 16);
            groupBox1.Margin = new Padding(3, 4, 3, 4);
            groupBox1.Name = "groupBox1";
            groupBox1.Padding = new Padding(3, 4, 3, 4);
            groupBox1.Size = new Size(1859, 1148);
            groupBox1.TabIndex = 0;
            groupBox1.TabStop = false;
            groupBox1.Text = "KÝ VĂN BẢN";
            // 
            // groupBox4
            // 
            groupBox4.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            groupBox4.BackColor = Color.MistyRose;
            groupBox4.Controls.Add(label6);
            groupBox4.Controls.Add(button2);
            groupBox4.Controls.Add(btnKiemTra);
            groupBox4.Controls.Add(rtbChuKyKT);
            groupBox4.Controls.Add(label11);
            groupBox4.Controls.Add(rtbVanBanKT);
            groupBox4.Controls.Add(btnMoFile1);
            groupBox4.Controls.Add(txtFilePath1);
            groupBox4.Controls.Add(label10);
            groupBox4.Location = new Point(951, 504);
            groupBox4.Margin = new Padding(3, 4, 3, 4);
            groupBox4.Name = "groupBox4";
            groupBox4.Padding = new Padding(3, 4, 3, 4);
            groupBox4.Size = new Size(900, 548);
            groupBox4.TabIndex = 1;
            groupBox4.TabStop = false;
            groupBox4.Text = "KIỂM TRA";
            // 
            // label6
            // 
            label6.AutoSize = true;
            label6.Location = new Point(15, 31);
            label6.Name = "label6";
            label6.Size = new Size(145, 20);
            label6.TabIndex = 18;
            label6.Text = "Tên thông điệp nhận";
            label6.Click += label6_Click;
            // 
            // button2
            // 
            button2.BackColor = Color.SpringGreen;
            button2.FlatAppearance.BorderColor = Color.Black;
            button2.FlatStyle = FlatStyle.Flat;
            button2.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            button2.ForeColor = Color.SteelBlue;
            button2.Location = new Point(581, 418);
            button2.Margin = new Padding(3, 4, 3, 4);
            button2.Name = "button2";
            button2.Size = new Size(125, 49);
            button2.TabIndex = 17;
            button2.Text = "Lưu file";
            button2.UseVisualStyleBackColor = false;
            button2.Click += button2_Click;
            // 
            // btnKiemTra
            // 
            btnKiemTra.BackColor = SystemColors.ActiveCaption;
            btnKiemTra.FlatAppearance.BorderColor = Color.Black;
            btnKiemTra.FlatStyle = FlatStyle.Flat;
            btnKiemTra.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnKiemTra.ForeColor = Color.Crimson;
            btnKiemTra.Location = new Point(240, 430);
            btnKiemTra.Margin = new Padding(3, 4, 3, 4);
            btnKiemTra.Name = "btnKiemTra";
            btnKiemTra.Size = new Size(177, 38);
            btnKiemTra.TabIndex = 16;
            btnKiemTra.Text = "Kiểm tra chữ kí";
            btnKiemTra.UseVisualStyleBackColor = false;
            btnKiemTra.Click += btnKiemTra_Click;
            // 
            // rtbChuKyKT
            // 
            rtbChuKyKT.Location = new Point(22, 322);
            rtbChuKyKT.Margin = new Padding(3, 4, 3, 4);
            rtbChuKyKT.Name = "rtbChuKyKT";
            rtbChuKyKT.Size = new Size(820, 77);
            rtbChuKyKT.TabIndex = 14;
            rtbChuKyKT.Text = "";
            // 
            // label11
            // 
            label11.AutoSize = true;
            label11.Location = new Point(7, 265);
            label11.Name = "label11";
            label11.Size = new Size(56, 20);
            label11.TabIndex = 15;
            label11.Text = "Chữ ký:";
            // 
            // rtbVanBanKT
            // 
            rtbVanBanKT.Location = new Point(15, 143);
            rtbVanBanKT.Margin = new Padding(3, 4, 3, 4);
            rtbVanBanKT.Name = "rtbVanBanKT";
            rtbVanBanKT.Size = new Size(827, 78);
            rtbVanBanKT.TabIndex = 14;
            rtbVanBanKT.Text = "";
            // 
            // btnMoFile1
            // 
            btnMoFile1.BackColor = Color.FromArgb(255, 192, 255);
            btnMoFile1.FlatAppearance.BorderColor = Color.Black;
            btnMoFile1.FlatStyle = FlatStyle.Flat;
            btnMoFile1.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnMoFile1.ForeColor = Color.SteelBlue;
            btnMoFile1.Location = new Point(714, 55);
            btnMoFile1.Margin = new Padding(3, 4, 3, 4);
            btnMoFile1.Name = "btnMoFile1";
            btnMoFile1.Size = new Size(83, 36);
            btnMoFile1.TabIndex = 2;
            btnMoFile1.Text = "Nhập file";
            btnMoFile1.UseVisualStyleBackColor = false;
            btnMoFile1.Click += btnMoFile1_Click;
            // 
            // txtFilePath1
            // 
            txtFilePath1.Location = new Point(15, 69);
            txtFilePath1.Margin = new Padding(3, 4, 3, 4);
            txtFilePath1.Name = "txtFilePath1";
            txtFilePath1.Size = new Size(563, 27);
            txtFilePath1.TabIndex = 1;
            // 
            // label10
            // 
            label10.AutoSize = true;
            label10.Location = new Point(15, 108);
            label10.Name = "label10";
            label10.Size = new Size(121, 20);
            label10.TabIndex = 0;
            label10.Text = "Thông điệp nhận";
            // 
            // groupBox3
            // 
            groupBox3.BackColor = Color.FromArgb(192, 255, 192);
            groupBox3.Controls.Add(label13);
            groupBox3.Controls.Add(button1);
            groupBox3.Controls.Add(btnReset);
            groupBox3.Controls.Add(btnKy);
            groupBox3.Controls.Add(btnSent);
            groupBox3.Controls.Add(rtbChuKyRS);
            groupBox3.Controls.Add(label9);
            groupBox3.Controls.Add(btnRandomK);
            groupBox3.Controls.Add(btnCheckK);
            groupBox3.Controls.Add(txtSoK);
            groupBox3.Controls.Add(label8);
            groupBox3.Controls.Add(txtFilePath);
            groupBox3.Controls.Add(rtbThongDiep);
            groupBox3.Controls.Add(btnMoFile);
            groupBox3.Controls.Add(label7);
            groupBox3.Location = new Point(8, 504);
            groupBox3.Margin = new Padding(3, 4, 3, 4);
            groupBox3.Name = "groupBox3";
            groupBox3.Padding = new Padding(3, 4, 3, 4);
            groupBox3.Size = new Size(900, 548);
            groupBox3.TabIndex = 1;
            groupBox3.TabStop = false;
            groupBox3.Text = "KÝ VĂN BẢN";
            // 
            // label13
            // 
            label13.AutoSize = true;
            label13.Location = new Point(9, 31);
            label13.Name = "label13";
            label13.Size = new Size(135, 20);
            label13.TabIndex = 15;
            label13.Text = "Tên thông điệp gửi";
            // 
            // button1
            // 
            button1.BackColor = Color.SpringGreen;
            button1.FlatAppearance.BorderColor = Color.Black;
            button1.FlatStyle = FlatStyle.Flat;
            button1.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            button1.ForeColor = Color.SteelBlue;
            button1.Location = new Point(610, 418);
            button1.Margin = new Padding(3, 4, 3, 4);
            button1.Name = "button1";
            button1.Size = new Size(125, 49);
            button1.TabIndex = 14;
            button1.Text = "Lưu file";
            button1.UseVisualStyleBackColor = false;
            button1.Click += button1_Click;
            // 
            // btnReset
            // 
            btnReset.BackColor = Color.FromArgb(255, 255, 192);
            btnReset.FlatAppearance.BorderColor = Color.Black;
            btnReset.FlatStyle = FlatStyle.Flat;
            btnReset.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnReset.ForeColor = Color.Navy;
            btnReset.Location = new Point(462, 423);
            btnReset.Margin = new Padding(3, 4, 3, 4);
            btnReset.Name = "btnReset";
            btnReset.Size = new Size(86, 45);
            btnReset.TabIndex = 13;
            btnReset.Text = "Reset";
            btnReset.UseVisualStyleBackColor = false;
            btnReset.Click += btnReset_Click;
            // 
            // btnKy
            // 
            btnKy.BackColor = SystemColors.ActiveCaption;
            btnKy.FlatAppearance.BorderColor = Color.Black;
            btnKy.FlatStyle = FlatStyle.Flat;
            btnKy.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnKy.ForeColor = Color.Blue;
            btnKy.Location = new Point(284, 422);
            btnKy.Margin = new Padding(3, 4, 3, 4);
            btnKy.Name = "btnKy";
            btnKy.Size = new Size(99, 45);
            btnKy.TabIndex = 11;
            btnKy.Text = "Ký tài liệu";
            btnKy.UseVisualStyleBackColor = false;
            btnKy.Click += btnKy_Click;
            // 
            // btnSent
            // 
            btnSent.BackColor = Color.FromArgb(255, 192, 128);
            btnSent.FlatAppearance.BorderColor = Color.Black;
            btnSent.FlatStyle = FlatStyle.Flat;
            btnSent.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnSent.ForeColor = Color.Blue;
            btnSent.Location = new Point(74, 421);
            btnSent.Margin = new Padding(3, 4, 3, 4);
            btnSent.Name = "btnSent";
            btnSent.Size = new Size(145, 45);
            btnSent.TabIndex = 10;
            btnSent.Text = "Chuyển dữ liệu";
            btnSent.UseVisualStyleBackColor = false;
            btnSent.Click += btnSent_Click;
            // 
            // rtbChuKyRS
            // 
            rtbChuKyRS.Location = new Point(20, 322);
            rtbChuKyRS.Margin = new Padding(3, 4, 3, 4);
            rtbChuKyRS.Name = "rtbChuKyRS";
            rtbChuKyRS.Size = new Size(813, 77);
            rtbChuKyRS.TabIndex = 9;
            rtbChuKyRS.Text = "";
            // 
            // label9
            // 
            label9.AutoSize = true;
            label9.Location = new Point(9, 287);
            label9.Name = "label9";
            label9.Size = new Size(88, 20);
            label9.TabIndex = 8;
            label9.Text = "Chữ ký (r, s):\r\n";
            // 
            // btnRandomK
            // 
            btnRandomK.BackColor = Color.FromArgb(255, 192, 192);
            btnRandomK.FlatAppearance.BorderColor = Color.Black;
            btnRandomK.FlatStyle = FlatStyle.Flat;
            btnRandomK.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnRandomK.ForeColor = Color.Blue;
            btnRandomK.Location = new Point(747, 242);
            btnRandomK.Margin = new Padding(3, 4, 3, 4);
            btnRandomK.Name = "btnRandomK";
            btnRandomK.Size = new Size(86, 31);
            btnRandomK.TabIndex = 7;
            btnRandomK.Text = "Random k";
            btnRandomK.UseVisualStyleBackColor = false;
            btnRandomK.Click += btnRandomK_Click;
            // 
            // btnCheckK
            // 
            btnCheckK.BackColor = Color.Cyan;
            btnCheckK.FlatAppearance.BorderColor = Color.Black;
            btnCheckK.FlatStyle = FlatStyle.Flat;
            btnCheckK.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnCheckK.ForeColor = Color.Crimson;
            btnCheckK.Location = new Point(610, 242);
            btnCheckK.Margin = new Padding(3, 4, 3, 4);
            btnCheckK.Name = "btnCheckK";
            btnCheckK.Size = new Size(86, 31);
            btnCheckK.TabIndex = 6;
            btnCheckK.Text = "Kiểm tra k";
            btnCheckK.UseVisualStyleBackColor = false;
            btnCheckK.Click += btnCheckK_Click;
            // 
            // txtSoK
            // 
            txtSoK.Location = new Point(34, 244);
            txtSoK.Margin = new Padding(3, 4, 3, 4);
            txtSoK.Name = "txtSoK";
            txtSoK.Size = new Size(540, 27);
            txtSoK.TabIndex = 5;
            // 
            // label8
            // 
            label8.AutoSize = true;
            label8.Location = new Point(9, 249);
            label8.Name = "label8";
            label8.Size = new Size(18, 20);
            label8.TabIndex = 4;
            label8.Text = "K";
            // 
            // txtFilePath
            // 
            txtFilePath.Location = new Point(9, 69);
            txtFilePath.Margin = new Padding(3, 4, 3, 4);
            txtFilePath.Name = "txtFilePath";
            txtFilePath.Size = new Size(574, 27);
            txtFilePath.TabIndex = 3;
            // 
            // rtbThongDiep
            // 
            rtbThongDiep.Location = new Point(18, 142);
            rtbThongDiep.Margin = new Padding(3, 4, 3, 4);
            rtbThongDiep.Name = "rtbThongDiep";
            rtbThongDiep.Size = new Size(815, 78);
            rtbThongDiep.TabIndex = 2;
            rtbThongDiep.Text = "";
            // 
            // btnMoFile
            // 
            btnMoFile.BackColor = Color.FromArgb(255, 192, 255);
            btnMoFile.FlatAppearance.BorderColor = Color.Black;
            btnMoFile.FlatStyle = FlatStyle.Flat;
            btnMoFile.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnMoFile.ForeColor = Color.SteelBlue;
            btnMoFile.Location = new Point(709, 55);
            btnMoFile.Margin = new Padding(3, 4, 3, 4);
            btnMoFile.Name = "btnMoFile";
            btnMoFile.Size = new Size(86, 36);
            btnMoFile.TabIndex = 1;
            btnMoFile.Text = "Nhập file";
            btnMoFile.UseVisualStyleBackColor = false;
            btnMoFile.Click += btnMoFile_Click;
            // 
            // label7
            // 
            label7.AutoSize = true;
            label7.Location = new Point(9, 108);
            label7.Name = "label7";
            label7.Size = new Size(111, 20);
            label7.TabIndex = 0;
            label7.Text = "Thông điệp gửi";
            // 
            // groupBox2
            // 
            groupBox2.BackColor = SystemColors.Info;
            groupBox2.Controls.Add(btnktradodaibit);
            groupBox2.Controls.Add(txtdodaikhoa);
            groupBox2.Controls.Add(label12);
            groupBox2.Controls.Add(btnTaoKhoa);
            groupBox2.Controls.Add(txtPrivateKey);
            groupBox2.Controls.Add(txtPublicKey);
            groupBox2.Controls.Add(label5);
            groupBox2.Controls.Add(label4);
            groupBox2.Controls.Add(btnRandomPGX);
            groupBox2.Controls.Add(btnCheckA);
            groupBox2.Controls.Add(txtSoA);
            groupBox2.Controls.Add(label3);
            groupBox2.Controls.Add(btnCheckG);
            groupBox2.Controls.Add(txtSoG);
            groupBox2.Controls.Add(label2);
            groupBox2.Controls.Add(btnCheckP);
            groupBox2.Controls.Add(txtSoP);
            groupBox2.Controls.Add(label1);
            groupBox2.Location = new Point(6, 28);
            groupBox2.Margin = new Padding(3, 4, 3, 4);
            groupBox2.Name = "groupBox2";
            groupBox2.Padding = new Padding(3, 4, 3, 4);
            groupBox2.Size = new Size(1845, 460);
            groupBox2.TabIndex = 0;
            groupBox2.TabStop = false;
            groupBox2.Text = "TẠO KHOÁ";
            // 
            // btnktradodaibit
            // 
            btnktradodaibit.BackColor = SystemColors.ActiveBorder;
            btnktradodaibit.FlatAppearance.BorderColor = Color.Black;
            btnktradodaibit.FlatStyle = FlatStyle.Flat;
            btnktradodaibit.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            btnktradodaibit.ForeColor = Color.Crimson;
            btnktradodaibit.Location = new Point(1591, 33);
            btnktradodaibit.Margin = new Padding(3, 4, 3, 4);
            btnktradodaibit.Name = "btnktradodaibit";
            btnktradodaibit.Size = new Size(151, 31);
            btnktradodaibit.TabIndex = 18;
            btnktradodaibit.Text = "Kiểm tra độ dài bit";
            btnktradodaibit.UseVisualStyleBackColor = false;
            btnktradodaibit.Click += btnktradodaibit_Click;
            // 
            // txtdodaikhoa
            // 
            txtdodaikhoa.Location = new Point(192, 37);
            txtdodaikhoa.Margin = new Padding(3, 4, 3, 4);
            txtdodaikhoa.Name = "txtdodaikhoa";
            txtdodaikhoa.Size = new Size(1344, 27);
            txtdodaikhoa.TabIndex = 17;
            // 
            // label12
            // 
            label12.AutoSize = true;
            label12.Location = new Point(22, 40);
            label12.Name = "label12";
            label12.Size = new Size(150, 20);
            label12.TabIndex = 16;
            label12.Text = "Độ dài bit P, G, A(bit)";
            label12.Click += label12_Click;
            // 
            // btnTaoKhoa
            // 
            btnTaoKhoa.BackColor = SystemColors.ActiveCaption;
            btnTaoKhoa.FlatAppearance.BorderColor = Color.Black;
            btnTaoKhoa.FlatStyle = FlatStyle.Flat;
            btnTaoKhoa.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnTaoKhoa.ForeColor = Color.Blue;
            btnTaoKhoa.Location = new Point(815, 398);
            btnTaoKhoa.Margin = new Padding(3, 4, 3, 4);
            btnTaoKhoa.Name = "btnTaoKhoa";
            btnTaoKhoa.Size = new Size(205, 45);
            btnTaoKhoa.TabIndex = 14;
            btnTaoKhoa.Text = "Tạo khoá";
            btnTaoKhoa.UseVisualStyleBackColor = false;
            btnTaoKhoa.Click += btnTaoKhoa_Click;
            // 
            // txtPrivateKey
            // 
            txtPrivateKey.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            txtPrivateKey.ForeColor = Color.Black;
            txtPrivateKey.Location = new Point(273, 352);
            txtPrivateKey.Margin = new Padding(3, 4, 3, 4);
            txtPrivateKey.Name = "txtPrivateKey";
            txtPrivateKey.Size = new Size(1469, 27);
            txtPrivateKey.TabIndex = 13;
            // 
            // txtPublicKey
            // 
            txtPublicKey.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            txtPublicKey.ForeColor = Color.Black;
            txtPublicKey.Location = new Point(273, 293);
            txtPublicKey.Margin = new Padding(3, 4, 3, 4);
            txtPublicKey.Name = "txtPublicKey";
            txtPublicKey.Size = new Size(1469, 27);
            txtPublicKey.TabIndex = 12;
            // 
            // label5
            // 
            label5.AutoSize = true;
            label5.ForeColor = Color.Blue;
            label5.Location = new Point(22, 352);
            label5.Name = "label5";
            label5.Size = new Size(126, 20);
            label5.TabIndex = 11;
            label5.Text = "KHOÁ BÍ MẬT (A)";
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.ForeColor = Color.Blue;
            label4.Location = new Point(22, 293);
            label4.Name = "label4";
            label4.Size = new Size(187, 20);
            label4.TabIndex = 10;
            label4.Text = "KHOÁ CÔNG KHAI (P, G, Y)";
            // 
            // btnRandomPGX
            // 
            btnRandomPGX.BackColor = Color.FromArgb(255, 192, 192);
            btnRandomPGX.FlatAppearance.BorderColor = Color.Black;
            btnRandomPGX.FlatStyle = FlatStyle.Flat;
            btnRandomPGX.Font = new Font("Segoe UI", 9F, FontStyle.Bold);
            btnRandomPGX.ForeColor = Color.Blue;
            btnRandomPGX.Location = new Point(711, 240);
            btnRandomPGX.Margin = new Padding(3, 4, 3, 4);
            btnRandomPGX.Name = "btnRandomPGX";
            btnRandomPGX.Size = new Size(396, 31);
            btnRandomPGX.TabIndex = 9;
            btnRandomPGX.Text = "Sinh ngẫu nhiên P,G,A";
            btnRandomPGX.UseVisualStyleBackColor = false;
            btnRandomPGX.Click += btnRandomPGX_Click;
            // 
            // btnCheckA
            // 
            btnCheckA.BackColor = SystemColors.ActiveBorder;
            btnCheckA.FlatAppearance.BorderColor = Color.Black;
            btnCheckA.FlatStyle = FlatStyle.Flat;
            btnCheckA.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            btnCheckA.ForeColor = Color.Crimson;
            btnCheckA.Location = new Point(1591, 189);
            btnCheckA.Margin = new Padding(3, 4, 3, 4);
            btnCheckA.Name = "btnCheckA";
            btnCheckA.Size = new Size(151, 31);
            btnCheckA.TabIndex = 8;
            btnCheckA.Text = "Kiểm tra A";
            btnCheckA.UseVisualStyleBackColor = false;
            btnCheckA.Click += btnCheckA_Click;
            // 
            // txtSoA
            // 
            txtSoA.Location = new Point(192, 195);
            txtSoA.Margin = new Padding(3, 4, 3, 4);
            txtSoA.Name = "txtSoA";
            txtSoA.Size = new Size(1344, 27);
            txtSoA.TabIndex = 7;
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(22, 194);
            label3.Name = "label3";
            label3.Size = new Size(19, 20);
            label3.TabIndex = 6;
            label3.Text = "A";
            // 
            // btnCheckG
            // 
            btnCheckG.BackColor = SystemColors.ActiveBorder;
            btnCheckG.FlatAppearance.BorderColor = Color.Black;
            btnCheckG.FlatStyle = FlatStyle.Flat;
            btnCheckG.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            btnCheckG.ForeColor = Color.Crimson;
            btnCheckG.Location = new Point(1591, 135);
            btnCheckG.Margin = new Padding(3, 4, 3, 4);
            btnCheckG.Name = "btnCheckG";
            btnCheckG.Size = new Size(151, 31);
            btnCheckG.TabIndex = 5;
            btnCheckG.Text = "Kiểm tra G";
            btnCheckG.UseVisualStyleBackColor = false;
            btnCheckG.Click += btnCheckG_Click;
            // 
            // txtSoG
            // 
            txtSoG.Location = new Point(192, 137);
            txtSoG.Margin = new Padding(3, 4, 3, 4);
            txtSoG.Name = "txtSoG";
            txtSoG.Size = new Size(1344, 27);
            txtSoG.TabIndex = 4;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(22, 140);
            label2.Name = "label2";
            label2.Size = new Size(19, 20);
            label2.TabIndex = 3;
            label2.Text = "G";
            // 
            // btnCheckP
            // 
            btnCheckP.BackColor = SystemColors.ActiveBorder;
            btnCheckP.FlatAppearance.BorderColor = Color.Black;
            btnCheckP.FlatStyle = FlatStyle.Flat;
            btnCheckP.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            btnCheckP.ForeColor = Color.Crimson;
            btnCheckP.Location = new Point(1591, 85);
            btnCheckP.Margin = new Padding(3, 4, 3, 4);
            btnCheckP.Name = "btnCheckP";
            btnCheckP.Size = new Size(151, 31);
            btnCheckP.TabIndex = 2;
            btnCheckP.Text = "Kiểm tra P";
            btnCheckP.UseVisualStyleBackColor = false;
            btnCheckP.Click += btnCheckP_Click;
            // 
            // txtSoP
            // 
            txtSoP.Location = new Point(192, 85);
            txtSoP.Margin = new Padding(3, 4, 3, 4);
            txtSoP.Name = "txtSoP";
            txtSoP.Size = new Size(1344, 27);
            txtSoP.TabIndex = 1;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(22, 85);
            label1.Name = "label1";
            label1.Size = new Size(17, 20);
            label1.TabIndex = 0;
            label1.Text = "P";
            // 
            // openFileDialog1
            // 
            openFileDialog1.FileName = "openFileDialog1";
            // 
            // openFileDialog2
            // 
            openFileDialog2.FileName = "openFileDialog2";
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            AutoScroll = true;
            BackColor = SystemColors.ActiveCaption;
            ClientSize = new Size(1906, 1055);
            Controls.Add(groupBox1);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Margin = new Padding(3, 4, 3, 4);
            Name = "Form1";
            Text = "Elgamal signature";
            groupBox1.ResumeLayout(false);
            groupBox4.ResumeLayout(false);
            groupBox4.PerformLayout();
            groupBox3.ResumeLayout(false);
            groupBox3.PerformLayout();
            groupBox2.ResumeLayout(false);
            groupBox2.PerformLayout();
            ResumeLayout(false);
        }

        #endregion

        private GroupBox groupBox1;
        private GroupBox groupBox3;
        private GroupBox groupBox4;
        private TextBox txtSoK;
        private Label label8;
        private TextBox txtFilePath;
        private RichTextBox rtbThongDiep;
        private Button btnMoFile;
        private Label label7;
        private Button btnReset;
        private Button btnKy;
        private Button btnSent;
        private RichTextBox rtbChuKyRS;
        private Label label9;
        private Button btnRandomK;
        private Button btnCheckK;
        private Label label11;
        private RichTextBox rtbVanBanKT;
        private Button btnMoFile1;
        private TextBox txtFilePath1;
        private Label label10;
        private Button btnKiemTra;
        private RichTextBox rtbChuKyKT;
        private OpenFileDialog openFileDialog1;
        private OpenFileDialog openFileDialog2;
        private GroupBox groupBox2;
        private Button btnTaoKhoa;
        private TextBox txtPrivateKey;
        private TextBox txtPublicKey;
        private Label label5;
        private Label label4;
        private Button btnRandomPGX;
        private Button btnCheckA;
        private TextBox txtSoA;
        private Label label3;
        private Button btnCheckG;
        private TextBox txtSoG;
        private Label label2;
        private Button btnCheckP;
        private TextBox txtSoP;
        private Label label1;
        private System.ComponentModel.BackgroundWorker backgroundWorker1;
        private System.ComponentModel.BackgroundWorker backgroundWorker2;
        private Label label12;
        private TextBox txtdodaikhoa;
        private Button btnktradodaibit;
        private Button button1;
        private Button button2;
        private Label label6;
        private Label label13;
    }
}
