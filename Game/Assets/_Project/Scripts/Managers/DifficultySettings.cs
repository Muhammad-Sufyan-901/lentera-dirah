using UnityEngine;

namespace LenteraDirah
{
    public enum DifficultyLevel
    {
        Mudah = 0,
        Normal = 1,
        Sulit = 2
    }

    /// <summary>
    /// Tingkat kesulitan disimpan di PlayerPrefs dan diterapkan saat scene dimuat
    /// (PlayerController.Start / EnemyShadowAI.Start). Tidak ada save progres.
    /// </summary>
    public static class DifficultySettings
    {
        public const string PrefsKey = "ld_difficulty";

        public static DifficultyLevel Current { get; private set; } = Load();

        public static string DisplayName
        {
            get
            {
                switch (Current)
                {
                    case DifficultyLevel.Mudah: return "MUDAH";
                    case DifficultyLevel.Sulit: return "SULIT";
                    default: return "NORMAL";
                }
            }
        }

        public static string Description
        {
            get
            {
                switch (Current)
                {
                    case DifficultyLevel.Mudah: return "Cahaya bertahan lebih lama, bayangan lebih lambat.";
                    case DifficultyLevel.Sulit: return "Cahaya cepat habis, bayangan lebih peka dan cepat.";
                    default: return "Pengalaman sesuai GDD: 2% energi per detik.";
                }
            }
        }

        /// <summary>Pengali laju penyusutan energi lentera.</summary>
        public static float DecayMultiplier
        {
            get
            {
                switch (Current)
                {
                    case DifficultyLevel.Mudah: return 0.75f;
                    case DifficultyLevel.Sulit: return 1.35f;
                    default: return 1f;
                }
            }
        }

        /// <summary>Pengali kecepatan patroli dan pengejaran Bayangan Wabah.</summary>
        public static float EnemySpeedMultiplier
        {
            get
            {
                switch (Current)
                {
                    case DifficultyLevel.Mudah: return 0.85f;
                    case DifficultyLevel.Sulit: return 1.15f;
                    default: return 1f;
                }
            }
        }

        /// <summary>Pengali radius deteksi dan radius lepas Bayangan Wabah.</summary>
        public static float EnemyDetectMultiplier
        {
            get
            {
                switch (Current)
                {
                    case DifficultyLevel.Mudah: return 0.8f;
                    case DifficultyLevel.Sulit: return 1.25f;
                    default: return 1f;
                }
            }
        }

        /// <summary>Pengali skor akhir: makin sulit, makin tinggi.</summary>
        public static float ScoreMultiplier
        {
            get
            {
                switch (Current)
                {
                    case DifficultyLevel.Mudah: return 1f;
                    case DifficultyLevel.Sulit: return 1.5f;
                    default: return 1.25f;
                }
            }
        }

        public static void Set(DifficultyLevel level)
        {
            Current = level;
            PlayerPrefs.SetInt(PrefsKey, (int)level);
            PlayerPrefs.Save();
        }

        private static DifficultyLevel Load()
        {
            int value = PlayerPrefs.GetInt(PrefsKey, (int)DifficultyLevel.Normal);

            if (value < (int)DifficultyLevel.Mudah || value > (int)DifficultyLevel.Sulit)
            {
                value = (int)DifficultyLevel.Normal;
            }

            return (DifficultyLevel)value;
        }
    }
}
