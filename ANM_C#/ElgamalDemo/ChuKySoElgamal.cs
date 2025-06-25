using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace ElgamalDemo
{
    class ChuKySoElgamal
    {
        public BigInteger P { get; private set; }

        public BigInteger G { get; private set; }

        public BigInteger Y { get; private set; }

        public BigInteger A { get; private set; }

        public void taoKhoa(int n)
        {
            P = timNTLon(n); //So bitlength cua P
            do
            {
                G = RandomBigInteger(P - 1);
            } while (G <= 1 || G >= P - 1 || !CheckG(G, P));
            // A: khóa bí mật, 1 < A < P-1
            do
            {
                A = RandomBigInteger(P - 1);
            } while (A <= 1 || A >= P - 1);

            //Y = ModPow(G, A, P);
        }

        public BigInteger HashMessage(string message)
        {
            //Băm văn bản
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(message));
                return new BigInteger(hashBytes, isUnsigned: true, isBigEndian: true);
            }
        }

        public (BigInteger r, BigInteger s) ky(string message, BigInteger p, BigInteger g, BigInteger y, BigInteger a, BigInteger k)
        {
            BigInteger H = HashMessage(message);
            BigInteger kInv = timNgichDao(k, p - 1);
            BigInteger r = ModPow(g, k, p);
            BigInteger s = kInv * (H - a * r) % (p - 1);
            if (s < 0) s += (p - 1);
            return (r, s);
        }

        public bool kiemtra(string message, BigInteger p, BigInteger g, BigInteger y, BigInteger r, BigInteger s)
        {
            if (r <= 0 || r >= p) return false;
            if (s < 0 || s >= p - 1) return false;

            BigInteger H = HashMessage(message);
            BigInteger left = ModPow(g, H, p);
            BigInteger right = (ModPow(y, r, p) * ModPow(r, s, p)) % p;

            return left == right;
        }
        public bool CheckP(BigInteger soP)
        {
            return CheckNTLon(soP);
        }
        public bool CheckG(BigInteger g, BigInteger p)
        {
            if (g <= 1 || g >= p)
                return false;

            HashSet<BigInteger> values = new HashSet<BigInteger>();
            BigInteger t;
            int maxSize = 10000;

            for (BigInteger i = 1; i < p; i++)
            {
                t = BigInteger.ModPow(g, i, p);
                if (values.Contains(t))
                    return false;
                values.Add(t);

                if (values.Count > maxSize)
                    return true;
            }
            return true;
        }
        public bool CheckA(BigInteger a, BigInteger p)
        {
            if(a < 1 || a >= p - 1)
            {
                return false;
            }
            return true;
        }

        public BigInteger TaoK(BigInteger p)
        {
            BigInteger K;
            do
            {
                K = RandomBigInteger(p - 1);
            } while (GCD(K, p - 1) != 1);
            return K;
        }
        public bool CheckK(BigInteger k, BigInteger p)
        {
            if (k < 1 || k >= p - 1)
            {
                return false;
            }
            return true;
        }

        public BigInteger RandomBigInteger(BigInteger max)
        {
            if (max <= 1)
                throw new ArgumentException("max phải lớn hơn 1");

            using (var rng = RandomNumberGenerator.Create())
            {
                int byteCount = max.ToByteArray().Length;
                byte[] bytes = new byte[byteCount];
                BigInteger result;

                do
                {
                    rng.GetBytes(bytes);
                    bytes[bytes.Length - 1] &= 0x7F; // đảm bảo dương
                    result = new BigInteger(bytes);
                }
                while (result <= 0 || result >= max);

                return result;
            }
        }
        public BigInteger GCD(BigInteger a, BigInteger b)
        {
            //Ham tim UCLN
            while (b != 0)
            {
                BigInteger temp = b;
                b = a % b;
                a = temp;
            }
            return BigInteger.Abs(a);
        }
        public bool CheckNTLon(BigInteger n)
        {
            int k = 10;
            if (n < 2) return false;
            if (n == 2 || n == 3) return true;
            if (n % 2 == 0) return false;

            BigInteger d = n - 1;
            int r = 0;
            while (d % 2 == 0)
            {
                d /= 2;
                r++;
            }

            RandomNumberGenerator rng = RandomNumberGenerator.Create();
            byte[] bytes = new byte[n.ToByteArray().LongLength];

            for (int i = 0; i < k; i++)
            {
                BigInteger a;
                do
                {
                    rng.GetBytes(bytes);
                    a = new BigInteger(bytes, isUnsigned: true);
                } while (a < 2 || a >= n - 2);

                BigInteger x = BigInteger.ModPow(a, d, n);
                if (x == 1 || x == n - 1)
                    continue;

                bool continueOuter = false;
                for (int j = 0; j < r - 1; j++)
                {
                    x = BigInteger.ModPow(x, 2, n);
                    if (x == n - 1)
                    {
                        continueOuter = true;
                        break;
                    }
                }

                if (continueOuter)
                    continue;

                return false;
            }

            return true;
        }

        public BigInteger timNTLon(int bitLength)
        {
            if (bitLength < 2)
                throw new ArgumentException("bitLength phải >= 2");

            BigInteger number;
            int byteLength = (bitLength + 7) / 8; // làm tròn lên để đủ số byte
            byte[] bytes = new byte[byteLength];
            RandomNumberGenerator rng = RandomNumberGenerator.Create();

            do
            {
                rng.GetBytes(bytes);

                // Đảm bảo bit cao nhất = 1 để đạt đúng độ dài bit yêu cầu
                int bitIndex = bitLength - 1;
                bytes[bytes.Length - 1] |= (byte)(1 << (bitIndex % 8));

                // Đảm bảo số lẻ
                bytes[0] |= 0x01;

                number = new BigInteger(bytes, isUnsigned: true, isBigEndian: true);
            }
            while (!CheckNTLon(number));

            return number;
        }

        public BigInteger ModPow(BigInteger a, BigInteger b, BigInteger n)
        {
            //a^b mod n
            return BigInteger.ModPow(a, b, n);
        }
        public BigInteger timNgichDao(BigInteger a, BigInteger m)
        {
            BigInteger m0 = m, t, q;
            BigInteger x0 = 0, x1 = 1;

            if (m == 1)
                return 0;

            while (a > 1)
            {
                q = a / m;
                t = m;

                m = a % m;
                a = t;

                t = x0;
                x0 = x1 - q * x0;
                x1 = t;
            }

            if (x1 < 0)
                x1 += m0;

            return x1;
        }
    }
}
