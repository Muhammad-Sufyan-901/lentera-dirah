using System.Collections.Generic;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering.Universal;
using UnityEngine.UI;

namespace LenteraDirah.Editor
{
    public static class PlayModeSmokeTest
    {
        private static readonly int[] EnemyCountPerLevel = { 3, 4, 5 };
        private static readonly string[][] LontarNamesPerLevel =
        {
            new[] { "Lontar_1_1", "Lontar_1_2", "Lontar_1_3" },
            new[] { "Lontar_2_1", "Lontar_2_2", "Lontar_2_3" },
            new[] { "Lontar_3_1", "Lontar_3_2", "Lontar_3_3" }
        };

        private static readonly List<string> results = new List<string>();
        private static int failures;
        private static int stage;
        private static int phase;
        private static float stageStarted;
        private static bool active;

        private static GameManager gameManager;
        private static PlayerController player;
        private static LevelManager levelManager;
        private static EnemyShadowAI[] enemies;
        private static float energyBefore;
        private static float radiusBefore;
        private static double runStarted;
        private static bool hadBestScore;
        private static int originalBestScore;
        private static int originalDifficulty;
        private static bool hadBgm;
        private static float originalBgm;

        public static void Run()
        {
            hadBestScore = PlayerPrefs.HasKey(GameManager.BestScorePrefsKey);
            originalBestScore = PlayerPrefs.GetInt(GameManager.BestScorePrefsKey, 0);
            originalDifficulty = PlayerPrefs.GetInt(DifficultySettings.PrefsKey, (int)DifficultyLevel.Normal);
            hadBgm = PlayerPrefs.HasKey(AudioManager.BgmPrefsKey);
            originalBgm = PlayerPrefs.GetFloat(AudioManager.BgmPrefsKey, 0.35f);

            PlayerPrefs.DeleteKey(GameManager.BestScorePrefsKey);
            DifficultySettings.Set(DifficultyLevel.Normal);

            EditorSceneManager.OpenScene(ProjectConfigurator.ScenePath, OpenSceneMode.Single);

            EditorSettings.enterPlayModeOptionsEnabled = true;
            EditorSettings.enterPlayModeOptions = EnterPlayModeOptions.DisableDomainReload;

            stage = 0;
            failures = 0;
            results.Clear();
            active = true;
            runStarted = EditorApplication.timeSinceStartup;

            EditorApplication.update += Tick;
            EditorApplication.isPlaying = true;
        }

        private static void Tick()
        {
            if (!active)
            {
                return;
            }

            if (EditorApplication.timeSinceStartup - runStarted > 120d)
            {
                Check("timeout", false);
                Finish();
                return;
            }

            if (!EditorApplication.isPlaying)
            {
                return;
            }

            switch (stage)
            {
                case 0: StageBoot(); break;
                case 1: StageEnergyDecay(); break;
                case 2: StageBurst(); break;
                case 3: StageStunRecovery(); break;
                case 4: StageCollect(1); break;
                case 5: StageVictory(1); break;
                case 6: StageCollect(2); break;
                case 7: StageVictory(2); break;
                case 8: StageCollect(3); break;
                case 9: StageVictory(3); break;
                default: Finish(); break;
            }
        }

        private static void StageBoot()
        {
            if (Wait(0.8f))
            {
                return;
            }

            gameManager = GameManager.Instance;
            player = Object.FindAnyObjectByType<PlayerController>();
            levelManager = Object.FindAnyObjectByType<LevelManager>();
            LevelController[] levels = Object.FindObjectsByType<LevelController>(FindObjectsInactive.Include, FindObjectsSortMode.None);

            Check("GameManager tersedia", gameManager != null);
            Check("Player tersedia", player != null);
            Check("LevelManager tersedia", levelManager != null);
            Check("3 level tersedia", levels.Length == 3, $"jumlah={levels.Length}");

            if (gameManager == null || player == null || levelManager == null)
            {
                Finish();
                return;
            }

            Check("State awal MainMenu", gameManager.State == GameState.MainMenu, gameManager.State.ToString());
            Check("Level awal adalah Desa Girah", gameManager.CurrentLevel == 1 && levelManager.CurrentLevelName.Contains("Desa Girah"));

            gameManager.OpenDifficultySelect();
            Check("Menu -> DifficultySelect", gameManager.State == GameState.DifficultySelect, gameManager.State.ToString());

            GameObject difficultyPanel = FindSceneObject("Difficulty_Panel");
            Check("Panel Pilih Kesulitan tampil", difficultyPanel != null && difficultyPanel.activeSelf);
            Check("Tiga tombol kesulitan tersedia",
                difficultyPanel != null &&
                HasDescendant(difficultyPanel, "StartDifficulty_Mudah") &&
                HasDescendant(difficultyPanel, "StartDifficulty_Normal") &&
                HasDescendant(difficultyPanel, "StartDifficulty_Sulit"));

            gameManager.StartGame(DifficultyLevel.Normal);
            Check("DifficultySelect -> IntroDialog", gameManager.State == GameState.IntroDialog, gameManager.State.ToString());
            Check("Mulai di level 1", gameManager.CurrentLevel == 1, gameManager.CurrentLevel.ToString());

            gameManager.AcknowledgeDialog();
            Check("Dialog -> Playing", gameManager.State == GameState.Playing, gameManager.State.ToString());

            GameObject hud = GameObject.Find("HUD_Panel");
            GameObject menu = GameObject.Find("MainMenu_Panel");
            Check("HUD aktif saat Playing", hud != null && hud.activeSelf);
            Check("MainMenu non-aktif", menu == null || !menu.activeSelf);

            enemies = Object.FindObjectsByType<EnemyShadowAI>(FindObjectsSortMode.None);
            Check("Level 1 memiliki 3 musuh", enemies.Length == 3, $"jumlah={enemies.Length}");

            GameObject settingsPanel = FindSceneObject("Settings_Panel");
            GameObject creditsPanel = FindSceneObject("Credits_Panel");
            GameObject pausePanel = FindSceneObject("Pause_Panel");
            Check("Panel Pengaturan tersedia", settingsPanel != null);
            Check("Panel Kredit tersedia", creditsPanel != null);
            Check("Panel Jeda tersedia", pausePanel != null);

            gameManager.Pause();
            Check("Playing -> Paused", gameManager.State == GameState.Paused, gameManager.State.ToString());
            Check("Time.timeScale 0 saat Jeda", Mathf.Approximately(Time.timeScale, 0f), Time.timeScale.ToString("0.00"));

            Button pauseSettings = FindSceneObject("PauseSettingsButton") != null
                ? FindSceneObject("PauseSettingsButton").GetComponent<Button>()
                : null;
            pauseSettings?.onClick.Invoke();
            Check("Tombol Pengaturan di Jeda membuka panel", settingsPanel != null && settingsPanel.activeSelf);

            Button settingsClose = FindSceneObject("SettingsCloseButton") != null
                ? FindSceneObject("SettingsCloseButton").GetComponent<Button>()
                : null;
            settingsClose?.onClick.Invoke();
            Check("Panel Pengaturan dapat ditutup", settingsPanel != null && !settingsPanel.activeSelf);
            Check("Jeda tetap aktif setelah menutup Pengaturan", gameManager.State == GameState.Paused,
                gameManager.State.ToString());

            gameManager.Resume();
            Check("Paused -> Playing", gameManager.State == GameState.Playing, gameManager.State.ToString());

            AudioManager audio = AudioManager.Instance;
            float originalBgmNow = audio != null ? audio.BgmVolume : 0f;
            audio?.SetBgmVolume(0.42f);
            Check("Volume BGM dapat diubah & tersimpan",
                audio != null && Mathf.Approximately(audio.BgmVolume, 0.42f) &&
                Mathf.Approximately(PlayerPrefs.GetFloat(AudioManager.BgmPrefsKey, -1f), 0.42f),
                audio != null ? audio.BgmVolume.ToString("0.00") : "tidak ada");
            audio?.SetBgmVolume(originalBgmNow);

            float detectNormal = enemies[0].CurrentDetectRadius;
            DifficultySettings.Set(DifficultyLevel.Sulit);
            player.ApplyDifficulty();
            enemies[0].ApplyDifficulty();
            float detectSulit = enemies[0].CurrentDetectRadius;
            Check("Kesulitan Sulit memperluas deteksi musuh", detectSulit > detectNormal + 0.5f,
                $"{detectNormal:0.00} -> {detectSulit:0.00}");

            DifficultySettings.Set(DifficultyLevel.Normal);
            player.ApplyDifficulty();
            enemies[0].ApplyDifficulty();
            Check("Kesulitan Normal kembali diterapkan",
                Mathf.Abs(enemies[0].CurrentDetectRadius - detectNormal) < 0.05f,
                enemies[0].CurrentDetectRadius.ToString("0.00"));

            Advance();
        }

        private static void StageEnergyDecay()
        {
            if (stageStarted <= 0f)
            {
                stageStarted = Time.realtimeSinceStartup;
            }

            if (Time.realtimeSinceStartup - stageStarted < 0.1f)
            {
                energyBefore = player.Energy;
                Light2D lantern = player.GetComponentInChildren<Light2D>();
                radiusBefore = lantern != null ? lantern.pointLightOuterRadius : 0f;
                return;
            }

            if (Time.realtimeSinceStartup - stageStarted < 1.3f)
            {
                return;
            }

            float decayed = energyBefore - player.Energy;
            Check("Light decay ~2%/detik", decayed > 1.2f && decayed < 4f, $"turun={decayed:0.00}%");

            float exposureHigh = player.ExposureMultiplier;
            float detectHigh = enemies[0].CurrentDetectRadius;

            player.AddEnergy(-75f);
            float exposureLow = player.ExposureMultiplier;
            float detectLow = enemies[0].CurrentDetectRadius;

            Check("Lentera terang memperbesar deteksi musuh", detectHigh > detectLow + 0.4f,
                $"{detectHigh:0.00} -> {detectLow:0.00}");
            Check("Exposure terang > redup", exposureHigh > exposureLow + 0.2f,
                $"{exposureHigh:0.00} -> {exposureLow:0.00}");

            Light2D lanternAfter = player.GetComponentInChildren<Light2D>();
            float radiusLow = lanternAfter != null ? lanternAfter.pointLightOuterRadius : 0f;
            Check("Radius Light 2D menyusut saat energi rendah", radiusLow < radiusBefore - 0.5f, $"{radiusBefore:0.00} -> {radiusLow:0.00}");

            player.AddEnergy(100f);
            Check("Minyak mengisi energi maksimal", Mathf.Approximately(player.Energy, 100f), player.Energy.ToString("0"));
            Check("Exposure kembali penuh saat energi 100%", player.ExposureMultiplier > 1.25f, player.ExposureMultiplier.ToString("0.00"));

            Advance();
        }

        private static void StageBurst()
        {
            if (phase == 0)
            {
                EnemyShadowAI target = enemies[0];
                Rigidbody2D body = player.GetComponent<Rigidbody2D>();
                Vector2 position = (Vector2)target.transform.position + Vector2.left * 2.2f;
                body.position = position;
                player.transform.position = position;
                phase = 1;
                stageStarted = Time.realtimeSinceStartup;
                return;
            }

            if (phase == 1)
            {
                if (Time.realtimeSinceStartup - stageStarted < 0.3f)
                {
                    return;
                }

                if (player.State == PlayerState.Hurt)
                {
                    return;
                }

                energyBefore = player.Energy;
                MethodInfo burst = typeof(PlayerController).GetMethod("TryHolyLightBurst", BindingFlags.Instance | BindingFlags.NonPublic);

                Check("Method Holy Light Burst ditemukan", burst != null);
                burst?.Invoke(player, null);

                float spent = energyBefore - player.Energy;
                Check("Burst memakai ~15% energi", spent > 12f && spent < 18f, $"pakai={spent:0.0}%");
                Check("Musuh terkena Stun", enemies[0].State == EnemyState.Stunned, enemies[0].State.ToString());
                Advance();
            }
        }

        private static void StageStunRecovery()
        {
            if (phase == 0)
            {
                Rigidbody2D body = player.GetComponent<Rigidbody2D>();
                body.position = new Vector2(21f, 7f);
                player.transform.position = new Vector3(21f, 7f, 0f);
                phase = 1;
                stageStarted = Time.realtimeSinceStartup;
                return;
            }

            if (!Wait(3.3f))
            {
                return;
            }

            Check("Stun berakhir setelah 3 detik", enemies[0].State != EnemyState.Stunned, enemies[0].State.ToString());
            Advance();
        }

        private static void StageCollect(int level)
        {
            string[] names = LontarNamesPerLevel[level - 1];

            if (stageStarted <= 0f)
            {
                stageStarted = Time.realtimeSinceStartup;

                foreach (EnemyShadowAI enemy in enemies)
                {
                    enemy.gameObject.SetActive(false);
                }

                return;
            }

            int elapsedSteps = Mathf.FloorToInt((Time.realtimeSinceStartup - stageStarted) / 0.45f);

            if (elapsedSteps < names.Length)
            {
                GameObject item = GameObject.Find(names[elapsedSteps]);

                if (item != null)
                {
                    Rigidbody2D body = player.GetComponent<Rigidbody2D>();
                    body.position = item.transform.position;
                    player.transform.position = item.transform.position;
                }

                return;
            }

            if (!Wait(0.45f * (names.Length + 1)))
            {
                return;
            }

            Check($"Level {level}: 3 Lontar terkumpul", gameManager.LontarCollected == 3, $"jumlah={gameManager.LontarCollected}");

            AltarPurification altar = Object.FindAnyObjectByType<AltarPurification>();
            Check($"Level {level}: segel Altar terbuka", altar != null && altar.IsUnsealed);

            Advance();
        }

        private static void StageVictory(int level)
        {
            if (stageStarted <= 0f)
            {
                stageStarted = Time.realtimeSinceStartup;
                AltarPurification altar = Object.FindAnyObjectByType<AltarPurification>();

                if (altar != null)
                {
                    Rigidbody2D body = player.GetComponent<Rigidbody2D>();
                    body.position = altar.transform.position;
                    player.transform.position = altar.transform.position;
                }

                return;
            }

            if (!Wait(0.6f))
            {
                return;
            }

            Check($"Level {level}: Altar memicu Victory", gameManager.State == GameState.Victory, gameManager.State.ToString());

            GameObject victoryPanel = GameObject.Find("Victory_Panel");
            Check($"Level {level}: panel hasil tampil", victoryPanel != null && victoryPanel.activeSelf);
            Check($"Level {level}: skor level dihitung", gameManager.LastLevelScore > 0, gameManager.LastLevelScore.ToString());
            Check($"Level {level}: skor total terakumulasi", gameManager.TotalScore >= gameManager.LastLevelScore,
                $"{gameManager.LastLevelScore} / {gameManager.TotalScore}");
            Check($"Level {level}: gelar terhitung", !string.IsNullOrEmpty(gameManager.LastRank), gameManager.LastRank);

            GameObject primary = FindDescendant(victoryPanel, "ActionButton");
            Text primaryLabel = primary != null ? primary.GetComponentInChildren<Text>() : null;

            if (level < 3)
            {
                Check($"Level {level}: tombol level berikutnya",
                    primaryLabel != null && primaryLabel.text.Contains("BERIKUTNYA"),
                    primaryLabel != null ? primaryLabel.text : "tidak ada");

                gameManager.AdvanceToNextLevel();
                Check($"Level {level} -> level {level + 1}", gameManager.State == GameState.Playing && gameManager.CurrentLevel == level + 1,
                    $"{gameManager.State} / {gameManager.CurrentLevel}");
                Check($"Level {level + 1}: nama level benar", levelManager.CurrentLevelName == ExpectedLevelName(level + 1),
                    levelManager.CurrentLevelName);
                Check($"Level {level + 1}: lontar direset", gameManager.LontarCollected == 0, gameManager.LontarCollected.ToString());
                Check($"Level {level + 1}: energi & nyawa penuh",
                    Mathf.Approximately(player.Energy, 100f) && player.Health == GameManager.MaxHealth,
                    $"{player.Energy:0} / {player.Health}");

                enemies = Object.FindObjectsByType<EnemyShadowAI>(FindObjectsSortMode.None);
                Check($"Level {level + 1}: {EnemyCountPerLevel[level]} musuh aktif",
                    enemies.Length == EnemyCountPerLevel[level], $"jumlah={enemies.Length}");
            }
            else
            {
                Check("Level 3 adalah level final", gameManager.IsFinalLevel);
                Check("Level 3: tombol selesai",
                    primaryLabel != null && primaryLabel.text.Contains("SELESAI"),
                    primaryLabel != null ? primaryLabel.text : "tidak ada");
                Check("Rekor skor tersimpan", gameManager.BestScore >= gameManager.TotalScore,
                    $"{gameManager.BestScore} / {gameManager.TotalScore}");

                gameManager.ReturnToMainMenu();
                GameObject menuPanel = GameObject.Find("MainMenu_Panel");
                Check("Kembali ke MainMenu", gameManager.State == GameState.MainMenu && menuPanel != null && menuPanel.activeSelf,
                    gameManager.State.ToString());
            }

            Advance();
        }

        private static string ExpectedLevelName(int level)
        {
            switch (level)
            {
                case 2: return "Hutan Bambu Lemah Tulis";
                case 3: return "Pelataran Setra Gandamayu";
                default: return "Desa Girah Bagian Luar";
            }
        }

        private static bool HasDescendant(GameObject root, string name)
        {
            foreach (Transform candidate in root.GetComponentsInChildren<Transform>(true))
            {
                if (candidate.name == name)
                {
                    return true;
                }
            }

            return false;
        }

        private static GameObject FindDescendant(GameObject root, string name)
        {
            if (root == null)
            {
                return null;
            }

            foreach (Transform candidate in root.GetComponentsInChildren<Transform>(true))
            {
                if (candidate.name == name)
                {
                    return candidate.gameObject;
                }
            }

            return null;
        }

        private static GameObject FindSceneObject(string name)
        {
            Transform[] all = Object.FindObjectsByType<Transform>(FindObjectsInactive.Include, FindObjectsSortMode.None);

            foreach (Transform candidate in all)
            {
                if (candidate.name == name)
                {
                    return candidate.gameObject;
                }
            }

            return null;
        }

        private static bool Wait(float seconds)
        {
            if (stageStarted <= 0f)
            {
                stageStarted = Time.realtimeSinceStartup;
                return false;
            }

            return Time.realtimeSinceStartup - stageStarted >= seconds;
        }

        private static void Advance()
        {
            stage++;
            phase = 0;
            stageStarted = 0f;
        }

        private static void Check(string name, bool passed, string detail = "")
        {
            string line = $"[TEST] {(passed ? "PASS" : "FAIL")} {name}{(string.IsNullOrEmpty(detail) ? string.Empty : $" ({detail})")}";
            results.Add(line);
            Debug.Log(line);

            if (!passed)
            {
                failures++;
            }
        }

        private static void Finish()
        {
            active = false;
            EditorApplication.update -= Tick;

            Debug.Log($"[TEST] ===== RINGKASAN: {results.Count - failures}/{results.Count} PASS, {failures} FAIL =====");

            foreach (string line in results)
            {
                Debug.Log(line);
            }

            EditorSettings.enterPlayModeOptionsEnabled = false;

            if (hadBestScore)
            {
                PlayerPrefs.SetInt(GameManager.BestScorePrefsKey, originalBestScore);
            }
            else
            {
                PlayerPrefs.DeleteKey(GameManager.BestScorePrefsKey);
            }

            if (hadBgm)
            {
                PlayerPrefs.SetFloat(AudioManager.BgmPrefsKey, originalBgm);
            }
            else
            {
                PlayerPrefs.DeleteKey(AudioManager.BgmPrefsKey);
            }

            DifficultySettings.Set((DifficultyLevel)originalDifficulty);
            PlayerPrefs.Save();

            EditorApplication.Exit(failures == 0 ? 0 : 1);
        }
    }
}
