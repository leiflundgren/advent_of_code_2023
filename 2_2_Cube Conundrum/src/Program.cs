﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace advent_of_code
{
    public class Program
    {

        public static Set MasterSet = new Set(12,13, 14);

        public static void Main(string[] args)
        {
            string path = Environment.CurrentDirectory;
            Console.WriteLine("Path: " + path);

            path = Path.GetFullPath(Path.Combine(path, "..\\..\\..\\..\\input.txt"));
            Console.WriteLine("Path: " + path);

            string[] lines = File.ReadAllLines(path);

            int sum = 0;

            foreach (string line in lines)
            {
                if (string.IsNullOrEmpty(line)) continue;

                Game g = Game.Parse(line);

                Set min_required = g.MinRequired();

                sum += min_required.PowerOf;
            }

            Console.WriteLine($"{sum}"); // 3099

        }
    }
}
