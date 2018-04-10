using System;
using System.Linq;
using System.Text;

namespace bevrand.testsuite.Helpers
{
    public static class RandomNameGenerator
    {
        private static Random random = new Random();

        public static string RandomString(int length)
        {
            const string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
            return new string(Enumerable.Repeat(chars, length)
                .Select(s => s[random.Next(s.Length)]).ToArray());
        }

        public static string RandomEmail()
        {
            const string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            var firstPart = new string(Enumerable.Repeat(chars, 15)
                .Select(s => s[random.Next(s.Length)]).ToArray());
            var secondPart = new string(Enumerable.Repeat(chars, 6)
                .Select(s => s[random.Next(s.Length)]).ToArray());
            return $"{firstPart}@{secondPart}.nl";
        }
    }
}

