using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering.Universal;
using UnityEngine.UI;

namespace LenteraDirah.Editor
{
    public static class PlayModePreviewCapture
    {
        private const int Width = 1600;
        private const int Height = 900;

        private static int state;
        private static int frames;
        private static double stateTime;
        private static bool active;
        private static Camera sceneCamera;
        private static Canvas sceneCanvas;
        private static RenderTexture renderTexture;
        private static bool hadBestScore;
        private static int originalBestScore;
        private static int originalDifficulty;
        private static Light2D globalLight;
        private static float originalGlobalIntensity;

        public static void Run()
        {
            hadBestScore = PlayerPrefs.HasKey(GameManager.BestScorePrefsKey);
            originalBestScore = PlayerPrefs.GetInt(GameManager.BestScorePrefsKey, 0);
            originalDifficulty = PlayerPrefs.GetInt(DifficultySettings.PrefsKey, (int)DifficultyLevel.Normal);
            PlayerPrefs.DeleteKey(GameManager.BestScorePrefsKey);
            DifficultySettings.Set(DifficultyLevel.Normal);

            EditorSceneManager.OpenScene(ProjectConfigurator.ScenePath, OpenSceneMode.Single);

            EditorSettings.enterPlayModeOptionsEnabled = true;
            EditorSettings.enterPlayModeOptions = EnterPlayModeOptions.DisableDomainReload;

            active = true;
            state = 0;
            frames = 0;

            EditorApplication.update += Tick;
            EditorApplication.isPlaying = true;

            Debug.Log("[LenteraDirah] Preview capture (menu, kesulitan, 3 level, hasil) dimulai.");
        }

        private static void Tick()
        {
            if (!active || !EditorApplication.isPlaying)
            {
                return;
            }

            if (state == 0)
            {
                if (Time.realtimeSinceStartup < 1.5f)
                {
                    return;
                }

                if (!PrepareRenderTarget())
                {
                    return;
                }

                PlayerController player = Object.FindAnyObjectByType<PlayerController>();

                if (player != null)
                {
                    player.SetRecordingInvulnerable(true);
                }

                state = 1;
                frames = 0;
                return;
            }

            frames++;

            switch (state)
            {
                case 1:
                    if (Ready(4))
                    {
                        SaveRenderTarget("preview_menu.png");
                        TryInvoke("SettingsButton");
                        Next(2);
                    }

                    break;

                case 2:
                    if (Ready(4))
                    {
                        SaveRenderTarget("preview_settings.png");
                        TryInvoke("SettingsCloseButton");
                        TryInvoke("CreditsButton");
                        Next(3);
                    }

                    break;

                case 3:
                    if (Ready(4))
                    {
                        SaveRenderTarget("preview_credits.png");
                        TryInvoke("CreditsCloseButton");
                        TryInvoke("HowToPlayButton");
                        Next(4);
                    }

                    break;

                case 4:
                    if (Ready(4))
                    {
                        SaveRenderTarget("preview_howto.png");
                        TryInvoke("HowToPlayCloseButton");
                        TryInvoke("StartButton");
                        Next(5);
                    }

                    break;

                case 5:
                    if (Ready(4))
                    {
                        SaveRenderTarget("preview_difficulty.png");
                        TryInvoke("StartDifficulty_Normal");
                        Next(6);
                    }

                    break;

                case 6:
                    if (Ready(6))
                    {
                        SaveRenderTarget("preview_dialog.png");
                        GameManager.Instance.AcknowledgeDialog();
                        Next(7);
                        stateTime = Time.realtimeSinceStartup;
                    }

                    break;

                case 7:
                    if (Time.realtimeSinceStartup - stateTime < 1.2f)
                    {
                        return;
                    }

                    SaveRenderTarget("preview_gameplay.png");
                    GameManager.Instance.Pause();
                    Next(8);
                    break;

                case 8:
                    if (Ready(4))
                    {
                        SaveRenderTarget("preview_pause.png");
                        GameManager.Instance.Resume();
                        ZoomOut();
                        stateTime = Time.realtimeSinceStartup;
                        Next(9);
                    }

                    break;

                case 9:
                    if (Ready(5))
                    {
                        SaveRenderTarget("preview_world.png");
                        RestoreCamera();
                        ForceVictory();
                        Next(10);
                    }

                    break;

                case 10:
                    if (Ready(5))
                    {
                        SaveRenderTarget("preview_victory.png");
                        TryInvoke("ActionButton");
                        Next(11);
                        stateTime = Time.realtimeSinceStartup;
                    }

                    break;

                case 11:
                    if (Time.realtimeSinceStartup - stateTime < 1.2f)
                    {
                        return;
                    }

                    SaveRenderTarget("preview_level2.png");
                    ZoomOut();
                    Next(12);
                    break;

                case 12:
                    if (Ready(5))
                    {
                        SaveRenderTarget("preview_level2_world.png");
                        RestoreCamera();
                        ForceVictory();
                        Next(13);
                    }

                    break;

                case 13:
                    if (Ready(5))
                    {
                        SaveRenderTarget("preview_victory2.png");
                        TryInvoke("ActionButton");
                        Next(14);
                        stateTime = Time.realtimeSinceStartup;
                    }

                    break;

                case 14:
                    if (Time.realtimeSinceStartup - stateTime < 1.2f)
                    {
                        return;
                    }

                    SaveRenderTarget("preview_level3.png");
                    ZoomOut();
                    Next(15);
                    break;

                case 15:
                    if (Ready(5))
                    {
                        SaveRenderTarget("preview_level3_world.png");
                        RestoreCamera();
                        GameManager.Instance.RequestGameOver("Lentera Suci padam. Kegelapan wabah menelan Bahula...");
                        Next(16);
                    }

                    break;

                case 16:
                    if (Ready(5))
                    {
                        SaveRenderTarget("preview_gameover.png");
                        TryInvoke("ActionButton");
                        Next(17);
                        stateTime = Time.realtimeSinceStartup;
                    }

                    break;

                case 17:
                    if (Time.realtimeSinceStartup - stateTime < 0.6f)
                    {
                        return;
                    }

                    ForceVictory();
                    Next(18);
                    break;

                case 18:
                    if (Ready(5))
                    {
                        SaveRenderTarget("preview_victory3.png");
                        Finish();
                    }

                    break;
            }
        }

        private static bool Ready(int requiredFrames)
        {
            return frames >= requiredFrames;
        }

        private static void Next(int nextState)
        {
            state = nextState;
            frames = 0;
        }

        private static void ForceVictory()
        {
            GameManager manager = GameManager.Instance;

            if (manager == null)
            {
                return;
            }

            manager.CollectLontar("Lontar Suci", "Cahaya pengetahuan memulihkan keseimbangan.");
            manager.CollectLontar("Lontar Suci", "Kebenaran dijaga melalui perbuatan baik.");
            manager.CollectLontar("Lontar Suci", "Terang dan gelap saling menyeimbangkan.");
            manager.PurifyAltar();
        }

        private static void ZoomOut()
        {
            CameraFollow2D follow = sceneCamera.GetComponent<CameraFollow2D>();

            if (follow != null)
            {
                follow.enabled = false;
            }

            sceneCamera.orthographicSize = 21f;
            sceneCamera.transform.position = new Vector3(22f, 16f, -10f);

            if (globalLight == null)
            {
                Light2D[] lights = Object.FindObjectsByType<Light2D>(FindObjectsSortMode.None);

                foreach (Light2D light in lights)
                {
                    if (light.lightType == Light2D.LightType.Global)
                    {
                        globalLight = light;
                        originalGlobalIntensity = light.intensity;
                        break;
                    }
                }
            }

            if (globalLight != null)
            {
                globalLight.intensity = 0.32f;
            }
        }

        private static void RestoreCamera()
        {
            sceneCamera.orthographicSize = 8f;

            if (globalLight != null)
            {
                globalLight.intensity = originalGlobalIntensity;
            }

            CameraFollow2D follow = sceneCamera.GetComponent<CameraFollow2D>();

            if (follow != null)
            {
                follow.enabled = true;
                follow.SnapToTarget();
            }
        }

        private static bool PrepareRenderTarget()
        {
            sceneCamera = Object.FindAnyObjectByType<Camera>();
            sceneCanvas = Object.FindAnyObjectByType<Canvas>();

            if (sceneCamera == null || sceneCanvas == null)
            {
                return false;
            }

            sceneCanvas.renderMode = RenderMode.ScreenSpaceCamera;
            sceneCanvas.worldCamera = sceneCamera;
            sceneCanvas.planeDistance = 1f;
            sceneCanvas.sortingOrder = 100;

            renderTexture = new RenderTexture(Width, Height, 24, RenderTextureFormat.ARGB32);
            renderTexture.Create();
            sceneCamera.targetTexture = renderTexture;

            return true;
        }

        private static bool TryInvoke(string objectName)
        {
            GameObject target = GameObject.Find(objectName);

            if (target == null)
            {
                return false;
            }

            Button button = target.GetComponent<Button>();

            if (button == null)
            {
                return false;
            }

            button.onClick.Invoke();
            return true;
        }

        private static void SaveRenderTarget(string fileName)
        {
            RenderTexture previous = RenderTexture.active;
            RenderTexture.active = renderTexture;

            Texture2D texture = new Texture2D(Width, Height, TextureFormat.RGB24, false);
            texture.ReadPixels(new Rect(0, 0, Width, Height), 0, 0);
            texture.Apply();

            RenderTexture.active = previous;

            string directory = Path.GetFullPath(Path.Combine(Application.dataPath, "../Docs"));
            Directory.CreateDirectory(directory);
            string path = Path.Combine(directory, fileName);
            File.WriteAllBytes(path, texture.EncodeToPNG());

            Object.Destroy(texture);
            Debug.Log($"[LenteraDirah] Preview disimpan: {path}");
        }

        private static void Finish()
        {
            active = false;
            EditorApplication.update -= Tick;

            if (sceneCamera != null)
            {
                sceneCamera.targetTexture = null;
            }

            if (renderTexture != null)
            {
                renderTexture.Release();
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

            DifficultySettings.Set((DifficultyLevel)originalDifficulty);
            PlayerPrefs.Save();

            EditorApplication.Exit(0);
        }
    }
}
