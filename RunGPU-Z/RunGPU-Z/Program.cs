using System;
using System.Diagnostics;

namespace RunGPU_Z
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Process gpuZ = new Process();
            gpuZ.StartInfo.FileName = "C:\\Program Files (x86)\\GPU-Z\\GPU-Z.exe";
            gpuZ.StartInfo.Arguments = "-minimized";
            gpuZ.Start();
        }
    }
}
