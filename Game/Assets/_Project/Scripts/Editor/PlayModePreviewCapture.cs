using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
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

        public static void Run()
        {
            EditorSceneManager.OpenScene(ProjectConfigurator.ScenePath, OpenSceneMode.Single);

            EditorSettings.enterPlayModeOptionsEnabled = true;
            EditorSettings.enterPlayModeOptions = EnterPlayModeOptions.DisableDomainReload;

            active = true;
            state = 0;
            frames = 0;

            EditorApplication.update += Tick;
            EditorApplication.isPlaying = true;

            Debug.Log("[LenteraDirah] Preview capture (menu, dialog, gameplay) dimulai.");
        }

        private static void Tick()
        {
            if (!active)
            {
                return;
            }

            if (!EditorApplication.isPlaying)
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

                stateTime = Time.realtimeSinceStartup;
                state = 1;
                frames = 0;
                return;
            }

            frames++;

            switch (state)
            {
                case 1:
                    if (frames < 4)
                    {
                        return;
                    }

                    SaveRenderTarget("preview_menu.png");

                    if (TryInvoke("HowToPlayButton"))
                    {
                        state = 5;
                        frames = 0;
                        return;
                    }

                    GameManager.Instance.StartPurification();
                    state = 2;
                    frames = 0;
                    break;

                case 5:
                    if (frames < 4)
                    {
                        return;
                    }

                    SaveRenderTarget("preview_howto.png");
                    TryInvoke("HowToPlayCloseButton");
                    GameManager.Instance.StartPurification();
                    state = 2;
                    frames = 0;
                    break;

                case 2:
                    if (frames < 6)
                    {
                        return;
                    }

                    SaveRenderTarget("preview_dialog.png");
                    GameManager.Instance.AcknowledgeDialog();
                    state = 3;
                    frames = 0;
                    stateTime = Time.realtimeSinceStartup;
                    break;

                case 3:
                    if (Time.realtimeSinceStartup - stateTime < 1.2f)
                    {
                        return;
                    }

                    SaveRenderTarget("preview_gameplay.png");

                    CameraFollow2D follow = sceneCamera.GetComponent<CameraFollow2D>();
                    if (follow != null)
                    {
                        follow.enabled = false;
                    }

                    sceneCamera.orthographicSize = 21f;
                    sceneCamera.transform.position = new Vector3(22f, 16f, -10f);

                    state = 4;
                    frames = 0;
                    break;

                case 4:
                    if (frames < 5)
                    {
                        return;
                    }

                    SaveRenderTarget("preview_world.png");
                    Finish();
                    break;
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
            EditorApplication.Exit(0);
        }
    }
}
