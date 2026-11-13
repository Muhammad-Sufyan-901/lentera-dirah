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
        private static readonly List<string> results = new List<string>();
        private static int failures;
        private static int stage;
        private static int phase;
        private static float stageStarted;
        private static bool active;

        private static GameManager gameManager;
        private static PlayerController player;
        private static EnemyShadowAI[] enemies;
        private static float energyBefore;
        private static float radiusBefore;
        private static double runStarted;

        public static void Run()
        {
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

            if (EditorApplication.timeSinceStartup - runStarted > 90d)
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
                case 0:
                    StageBoot();
                    break;
                case 1:
                    StageEnergyDecay();
                    break;
                case 2:
                    StageBurst();
                    break;
                case 3:
                    StageStunRecovery();
                    break;
                case 4:
                    StageCollect();
                    break;
                case 5:
                    StageVictory();
                    break;
                default:
                    Finish();
                    break;
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
            enemies = Object.FindObjectsByType<EnemyShadowAI>(FindObjectsSortMode.None);

            Check("GameManager tersedia", gameManager != null);
            Check("Player tersedia", player != null);
            Check("3 musuh tersedia", enemies != null && enemies.Length == 3, $"jumlah={enemies?.Length}");

            if (gameManager == null || player == null)
            {
                Finish();
                return;
            }

            Check("State awal MainMenu", gameManager.State == GameState.MainMenu, gameManager.State.ToString());

            gameManager.StartPurification();
            Check("Menu -> IntroDialog", gameManager.State == GameState.IntroDialog, gameManager.State.ToString());

            gameManager.AcknowledgeDialog();
            Check("Dialog -> Playing", gameManager.State == GameState.Playing, gameManager.State.ToString());

            GameObject hud = GameObject.Find("HUD_Panel");
            GameObject menu = GameObject.Find("MainMenu_Panel");
            Check("HUD aktif saat Playing", hud != null && hud.activeSelf);
            Check("MainMenu non-aktif", menu == null || !menu.activeSelf);

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

            player.AddEnergy(-50f);
            Light2D lanternAfter = player.GetComponentInChildren<Light2D>();
            float radiusLow = lanternAfter != null ? lanternAfter.pointLightOuterRadius : 0f;
            Check("Radius Light 2D menyusut saat energi rendah", radiusLow < radiusBefore - 0.5f, $"{radiusBefore:0.00} -> {radiusLow:0.00}");

            player.AddEnergy(100f);
            Check("Minyak mengisi energi maksimal", Mathf.Approximately(player.Energy, 100f), player.Energy.ToString("0"));

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

        private static void StageCollect()
        {
            if (stageStarted <= 0f)
            {
                stageStarted = Time.realtimeSinceStartup;

                foreach (EnemyShadowAI enemy in enemies)
                {
                    enemy.gameObject.SetActive(false);
                }

                return;
            }

            string[] itemNames = { "LontarSuci_Usada", "LontarSuci_Dharma", "LontarSuci_RwaBhineda" };
            int elapsedSteps = Mathf.FloorToInt((Time.realtimeSinceStartup - stageStarted) / 0.45f);

            if (elapsedSteps < itemNames.Length)
            {
                GameObject item = GameObject.Find(itemNames[elapsedSteps]);

                if (item != null)
                {
                    Rigidbody2D body = player.GetComponent<Rigidbody2D>();
                    body.position = item.transform.position;
                    player.transform.position = item.transform.position;
                }

                return;
            }

            if (!Wait(0.45f * (itemNames.Length + 1)))
            {
                return;
            }

            Check("3 Lontar terkumpul", gameManager.LontarCollected == 3, $"jumlah={gameManager.LontarCollected}");

            AltarPurification altar = Object.FindAnyObjectByType<AltarPurification>();
            Check("Segel Altar terbuka", altar != null && altar.IsUnsealed);

            Advance();
        }

        private static void StageVictory()
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

            Check("Altar memicu Victory", gameManager.State == GameState.Victory, gameManager.State.ToString());

            GameObject victoryPanel = GameObject.Find("Victory_Panel");
            Check("Panel Victory tampil", victoryPanel != null && victoryPanel.activeSelf);

            Advance();
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
            EditorApplication.Exit(failures == 0 ? 0 : 1);
        }
    }
}
