using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.UI;

namespace LenteraDirah.Editor
{
    /// <summary>
    /// Renders scripted gameplay clips (win / lose) from play mode into PNG frames.
    /// One script step is executed per captured frame (1:1 lock-step) so the
    /// timeline is deterministic even though the editor loop runs faster than
    /// the renderer. Frames are later encoded with ffmpeg.
    /// </summary>
    public static class PlayModeGameplayRecorder
    {
        private const int Width = 1280;
        private const int Height = 720;
        private const int Fps = 30;
        private const int MaxFrames = 20000;

        private static string mode;
        private static string frameDirectory;
        private static bool active;
        private static bool captureReady;
        private static bool pendingCapture;
        private static bool failed;
        private static int frameIndex;
        private static int tailFrames;
        private static double runStarted;

        private static Camera sceneCamera;
        private static Canvas sceneCanvas;
        private static PlayerController player;
        private static RenderTexture renderTexture;
        private static Texture2D texture;
        private static readonly Stack<IEnumerator> routines = new Stack<IEnumerator>();

        private static bool walking;
        private static Vector2 walkTarget;

        [MenuItem("Tools/Lentera Dirah/Record Gameplay Clip (Win)", priority = 30)]
        public static void RecordWin()
        {
            Begin("win");
        }

        [MenuItem("Tools/Lentera Dirah/Record Gameplay Clip (Lose)", priority = 31)]
        public static void RecordLose()
        {
            Begin("lose");
        }

        private static void Begin(string which)
        {
            mode = which;
            string root = Path.GetFullPath(Path.Combine(Application.dataPath, "..", "..", "Gameplay Record"));
            frameDirectory = Path.Combine(root, "frames_" + which);

            if (Directory.Exists(frameDirectory))
            {
                Directory.Delete(frameDirectory, true);
            }

            Directory.CreateDirectory(frameDirectory);

            EditorSceneManager.OpenScene(ProjectConfigurator.ScenePath, OpenSceneMode.Single);

            EditorSettings.enterPlayModeOptionsEnabled = true;
            EditorSettings.enterPlayModeOptions = EnterPlayModeOptions.DisableDomainReload;

            active = true;
            captureReady = false;
            pendingCapture = false;
            failed = false;
            frameIndex = 0;
            tailFrames = 0;
            walking = false;
            routines.Clear();
            runStarted = EditorApplication.timeSinceStartup;

            EditorApplication.update += Tick;
            RenderPipelineManager.endCameraRendering += OnCameraRendered;
            EditorApplication.isPlaying = true;
        }

        private static void Tick()
        {
            if (!active)
            {
                return;
            }

            if (EditorApplication.timeSinceStartup - runStarted > 900d)
            {
                Debug.LogError("[Recorder] timeout");
                failed = true;
                Finish();
                return;
            }

            if (!EditorApplication.isPlaying)
            {
                return;
            }

            if (!captureReady)
            {
                Prepare();
                return;
            }

            // Wait until the frame requested by the previous step has been rendered.
            if (pendingCapture)
            {
                return;
            }

            if (frameIndex >= MaxFrames)
            {
                Debug.LogError("[Recorder] frame cap reached");
                failed = true;
                Finish();
                return;
            }

            if (routines.Count == 0)
            {
                tailFrames--;

                if (tailFrames <= 0)
                {
                    Finish();
                }

                return;
            }

            UpdateWalking();

            bool frameConsumed;

            try
            {
                frameConsumed = AdvanceScript();
            }
            catch (Exception exception)
            {
                Debug.LogError($"[Recorder] script error: {exception}");
                failed = true;
                Finish();
                return;
            }

            if (!frameConsumed)
            {
                tailFrames = 24;
                return;
            }

            pendingCapture = true;
        }

        private static void SetScript(IEnumerator sequence)
        {
            routines.Clear();
            routines.Push(sequence);
        }

        private static bool AdvanceScript()
        {
            while (routines.Count > 0)
            {
                IEnumerator routine = routines.Peek();

                if (!routine.MoveNext())
                {
                    routines.Pop();
                    continue;
                }

                if (routine.Current is IEnumerator nested)
                {
                    routines.Push(nested);
                    continue;
                }

                return true;
            }

            return false;
        }

        private static void Prepare()
        {
            if (GameManager.Instance == null)
            {
                return;
            }

            sceneCamera = UnityEngine.Object.FindAnyObjectByType<Camera>();
            sceneCanvas = UnityEngine.Object.FindAnyObjectByType<Canvas>();
            player = UnityEngine.Object.FindAnyObjectByType<PlayerController>();

            if (sceneCamera == null || sceneCanvas == null || player == null)
            {
                return;
            }

            sceneCanvas.renderMode = RenderMode.ScreenSpaceCamera;
            sceneCanvas.worldCamera = sceneCamera;
            sceneCanvas.planeDistance = 1f;
            sceneCanvas.sortingOrder = 100;

            renderTexture = new RenderTexture(Width, Height, 24, RenderTextureFormat.ARGB32);
            renderTexture.Create();
            sceneCamera.targetTexture = renderTexture;

            texture = new Texture2D(Width, Height, TextureFormat.RGB24, false);

            Time.captureFramerate = Fps;

            if (mode == "win")
            {
                player.SetRecordingInvulnerable(true);
            }

            captureReady = true;
            pendingCapture = true;
            SetScript(mode == "win" ? WinSequence() : LoseSequence());

            Debug.Log($"[Recorder] capturing '{mode}' at {Width}x{Height}@{Fps}fps");
        }

        private static void OnCameraRendered(ScriptableRenderContext context, Camera camera)
        {
            if (!active || !captureReady || !pendingCapture || camera != sceneCamera)
            {
                return;
            }

            RenderTexture previous = RenderTexture.active;
            RenderTexture.active = renderTexture;

            texture.ReadPixels(new Rect(0, 0, Width, Height), 0, 0);
            texture.Apply(false);

            RenderTexture.active = previous;

            File.WriteAllBytes(Path.Combine(frameDirectory, $"frame_{frameIndex:00000}.png"), texture.EncodeToPNG());

            frameIndex++;
            pendingCapture = false;

            if (frameIndex % 100 == 0)
            {
                Debug.Log($"[Recorder] {mode}: {frameIndex} frames");
            }
        }

        private static void UpdateWalking()
        {
            if (!walking || player == null)
            {
                return;
            }

            Vector2 delta = walkTarget - (Vector2)player.transform.position;

            if (delta.magnitude <= 0.35f)
            {
                walking = false;
                player.SetScriptedInput(Vector2.zero);
                return;
            }

            player.SetScriptedInput(delta.normalized);
        }

        // ------------------------------------------------------------------
        // Timeline helpers (each yield = one captured frame)
        // ------------------------------------------------------------------
        private static IEnumerator Wait(int frames)
        {
            for (int i = 0; i < frames; i++)
            {
                yield return null;
            }
        }

        private static IEnumerator WalkUntilArrived(int maxFrames)
        {
            int frames = 0;

            while (walking && frames < maxFrames)
            {
                frames++;
                yield return null;
            }

            if (walking)
            {
                walking = false;
                player.SetScriptedInput(Vector2.zero);
            }
        }

        private static void WalkTo(Vector2 target)
        {
            walkTarget = target;
            walking = true;
        }

        private static void Teleport(Vector2 position)
        {
            Rigidbody2D body = player.GetComponent<Rigidbody2D>();
            body.position = position;
            player.transform.position = position;

            if (sceneCamera != null)
            {
                sceneCamera.transform.position = new Vector3(position.x, position.y + 1f, sceneCamera.transform.position.z);
            }

            player.SetScriptedInput(Vector2.zero);
            walking = false;
        }

        private static void Click(string objectName)
        {
            GameObject target = GameObject.Find(objectName);

            if (target == null)
            {
                return;
            }

            Button button = target.GetComponent<Button>();
            button?.onClick.Invoke();
        }

        private static void Burst()
        {
            MethodInfo method = typeof(PlayerController).GetMethod("TryHolyLightBurst", BindingFlags.Instance | BindingFlags.NonPublic);
            method?.Invoke(player, null);
        }

        // ------------------------------------------------------------------
        // Clips
        // ------------------------------------------------------------------
        private static IEnumerator WinSequence()
        {
            yield return Wait(45);              // main menu
            Click("HowToPlayButton");
            yield return Wait(45);              // how-to panel
            Click("HowToPlayCloseButton");
            yield return Wait(15);

            GameManager.Instance.StartPurification();
            yield return Wait(35);              // intro dialog
            GameManager.Instance.AcknowledgeDialog();
            yield return Wait(10);

            WalkTo(new Vector2(21.5f, 12.5f));  // walk through the gate to the plaza
            yield return WalkUntilArrived(150);

            WalkTo(new Vector2(22f, 16.1f));    // sealed altar hint
            yield return WalkUntilArrived(100);
            yield return Wait(20);

            Teleport(new Vector2(21.5f, 25.5f)); // north sector
            yield return Wait(10);
            WalkTo(new Vector2(21f, 27f));       // Lontar Usada
            yield return WalkUntilArrived(90);
            yield return Wait(20);

            Teleport(new Vector2(14f, 17.6f));   // west corridor: enemy + burst
            yield return Wait(12);
            Burst();
            yield return Wait(50);

            Teleport(new Vector2(10f, 18f));     // west room: lantern oil
            yield return Wait(10);
            WalkTo(new Vector2(10f, 16.4f));
            yield return WalkUntilArrived(80);
            yield return Wait(15);

            Teleport(new Vector2(6f, 18f));      // west Lontar Dharma
            yield return Wait(10);
            WalkTo(new Vector2(6f, 16.4f));
            yield return WalkUntilArrived(80);
            yield return Wait(15);

            Teleport(new Vector2(37f, 18f));     // east Lontar Rwa Bhineda
            yield return Wait(10);
            WalkTo(new Vector2(37f, 16.4f));
            yield return WalkUntilArrived(80);
            yield return Wait(20);

            Teleport(new Vector2(22f, 19.6f));   // altar is unsealed now
            yield return Wait(15);
            WalkTo(new Vector2(22f, 16.2f));
            yield return WalkUntilArrived(100);
            yield return Wait(90);               // victory panel
        }

        private static IEnumerator LoseSequence()
        {
            yield return Wait(40);              // main menu
            GameManager.Instance.StartPurification();
            yield return Wait(30);
            GameManager.Instance.AcknowledgeDialog();
            yield return Wait(10);

            WalkTo(new Vector2(21.5f, 12.5f));
            yield return WalkUntilArrived(150);

            Teleport(new Vector2(14f, 18.6f));   // let a shadow hit Bahula
            yield return Wait(10);
            WalkTo(new Vector2(14f, 17.4f));
            yield return WalkUntilArrived(60);
            yield return Wait(38);               // one hit + hurt flash

            Teleport(new Vector2(22f, 18.5f));
            yield return Wait(15);
            player.AddEnergy(-(player.Energy - 0.3f)); // leave a sliver so decay triggers game over
            yield return Wait(110);
        }

        private static void Finish()
        {
            active = false;
            captureReady = false;
            pendingCapture = false;

            EditorApplication.update -= Tick;
            RenderPipelineManager.endCameraRendering -= OnCameraRendered;

            if (sceneCamera != null)
            {
                sceneCamera.targetTexture = null;
            }

            if (renderTexture != null)
            {
                renderTexture.Release();
                UnityEngine.Object.DestroyImmediate(renderTexture);
            }

            if (texture != null)
            {
                UnityEngine.Object.DestroyImmediate(texture);
            }

            EditorSettings.enterPlayModeOptionsEnabled = false;

            Debug.Log($"[Recorder] '{mode}' finished with {frameIndex} frames");

            EditorApplication.Exit(failed ? 1 : 0);
        }
    }
}
