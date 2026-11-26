using System.Collections;
using UnityEngine;
using UnityEngine.UI;

namespace LenteraDirah
{
    public class UIManager : MonoBehaviour
    {
        private const string FullscreenPrefsKey = "ld_fullscreen";

        private static readonly Color Gold = new Color(1f, 0.721f, 0.302f, 1f);
        private static readonly Color Cyan = new Color(0.392f, 0.784f, 1f, 1f);

        [Header("Panel")]
        [SerializeField] private GameObject mainMenuPanel;
        [SerializeField] private GameObject difficultySelectPanel;
        [SerializeField] private GameObject howToPlayPanel;
        [SerializeField] private GameObject dialogPanel;
        [SerializeField] private GameObject hudPanel;
        [SerializeField] private GameObject pausePanel;
        [SerializeField] private GameObject victoryPanel;
        [SerializeField] private GameObject gameOverPanel;
        [SerializeField] private GameObject settingsPanel;
        [SerializeField] private GameObject creditsPanel;

        [Header("HUD")]
        [SerializeField] private Text lontarText;
        [SerializeField] private Text energyText;
        [SerializeField] private Text hintText;
        [SerializeField] private Text timerText;
        [SerializeField] private Text lightStatusText;
        [SerializeField] private Text levelText;
        [SerializeField] private Text scoreText;
        [SerializeField] private Image energyFill;
        [SerializeField] private Image[] hearts;

        [Header("Dialog & Layar Akhir")]
        [SerializeField] private Text dialogText;
        [SerializeField] private Text victoryHeading;
        [SerializeField] private Text victoryText;
        [SerializeField] private Text victoryRankText;
        [SerializeField] private Text victoryLevelScoreText;
        [SerializeField] private Text victoryTotalText;
        [SerializeField] private Text victoryBestText;
        [SerializeField] private Text gameOverText;
        [SerializeField] private Text gameOverScoreText;

        [Header("Tombol")]
        [SerializeField] private Button startButton;
        [SerializeField] private Button howToPlayButton;
        [SerializeField] private Button howToPlayCloseButton;
        [SerializeField] private Button quitButton;
        [SerializeField] private Button dialogButton;
        [SerializeField] private Button victoryButton;
        [SerializeField] private Button victoryMenuButton;
        [SerializeField] private Button gameOverButton;
        [SerializeField] private Button gameOverMenuButton;
        [SerializeField] private Button settingsButton;
        [SerializeField] private Button creditsButton;
        [SerializeField] private Button creditsCloseButton;
        [SerializeField] private Button resumeButton;
        [SerializeField] private Button pauseSettingsButton;
        [SerializeField] private Button pauseMenuButton;
        [SerializeField] private Button settingsCloseButton;
        [SerializeField] private Button difficultyBackButton;
        [SerializeField] private Button[] difficultyButtons;

        [Header("Pengaturan")]
        [SerializeField] private Slider bgmSlider;
        [SerializeField] private Slider sfxSlider;
        [SerializeField] private Text bgmValueText;
        [SerializeField] private Text sfxValueText;
        [SerializeField] private Button fullscreenButton;
        [SerializeField] private Text fullscreenLabel;

        private Coroutine hintRoutine;
        private bool fullscreenOn;

        private void Awake()
        {
            if (startButton != null)
            {
                startButton.onClick.AddListener(OnStartClicked);
            }

            if (quitButton != null)
            {
                quitButton.onClick.AddListener(OnQuitClicked);
            }

            if (howToPlayButton != null)
            {
                howToPlayButton.onClick.AddListener(ShowHowToPlay);
            }

            if (howToPlayCloseButton != null)
            {
                howToPlayCloseButton.onClick.AddListener(HideHowToPlay);
            }

            if (dialogButton != null)
            {
                dialogButton.onClick.AddListener(OnDialogClicked);
            }

            if (victoryButton != null)
            {
                victoryButton.onClick.AddListener(OnVictoryAction);
            }

            if (victoryMenuButton != null)
            {
                victoryMenuButton.onClick.AddListener(ReturnToMenu);
            }

            if (gameOverButton != null)
            {
                gameOverButton.onClick.AddListener(OnRetryClicked);
            }

            if (gameOverMenuButton != null)
            {
                gameOverMenuButton.onClick.AddListener(ReturnToMenu);
            }

            if (settingsButton != null)
            {
                settingsButton.onClick.AddListener(ShowSettings);
            }

            if (pauseSettingsButton != null)
            {
                pauseSettingsButton.onClick.AddListener(ShowSettings);
            }

            if (settingsCloseButton != null)
            {
                settingsCloseButton.onClick.AddListener(HideSettings);
            }

            if (creditsButton != null)
            {
                creditsButton.onClick.AddListener(ShowCredits);
            }

            if (creditsCloseButton != null)
            {
                creditsCloseButton.onClick.AddListener(HideCredits);
            }

            if (resumeButton != null)
            {
                resumeButton.onClick.AddListener(ResumeGame);
            }

            if (pauseMenuButton != null)
            {
                pauseMenuButton.onClick.AddListener(ReturnToMenu);
            }

            if (difficultyBackButton != null)
            {
                difficultyBackButton.onClick.AddListener(OnDifficultyBackClicked);
            }

            if (fullscreenButton != null)
            {
                fullscreenButton.onClick.AddListener(ToggleFullscreen);
            }

            if (bgmSlider != null)
            {
                bgmSlider.onValueChanged.AddListener(OnBgmChanged);
            }

            if (sfxSlider != null)
            {
                sfxSlider.onValueChanged.AddListener(OnSfxChanged);
            }

            if (difficultyButtons != null)
            {
                for (int i = 0; i < difficultyButtons.Length; i++)
                {
                    int index = i;

                    if (difficultyButtons[i] != null)
                    {
                        difficultyButtons[i].onClick.AddListener(() => OnDifficultyChosen((DifficultyLevel)index));
                    }
                }
            }
        }

        private void Start()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.StateChanged += HandleStateChanged;
                GameManager.Instance.LontarChanged += HandleLontarChanged;
                GameManager.Instance.HealthChanged += HandleHealthChanged;
                GameManager.Instance.EnergyChanged += HandleEnergyChanged;
                GameManager.Instance.HintChanged += HandleHintChanged;
                GameManager.Instance.LevelChanged += HandleLevelChanged;
                GameManager.Instance.ScoreChanged += HandleScoreChanged;

                HandleStateChanged(GameManager.Instance.State);
                HandleLontarChanged(GameManager.Instance.LontarCollected);
                HandleHealthChanged(GameManager.Instance.Health);
                HandleEnergyChanged(GameManager.Instance.CurrentEnergy);
                HandleLevelChanged(GameManager.Instance.CurrentLevel);
                HandleScoreChanged(GameManager.Instance.TotalScore);
            }

            InitializeSettings();
        }

        private void OnDestroy()
        {
            if (GameManager.Instance == null)
            {
                return;
            }

            GameManager.Instance.StateChanged -= HandleStateChanged;
            GameManager.Instance.LontarChanged -= HandleLontarChanged;
            GameManager.Instance.HealthChanged -= HandleHealthChanged;
            GameManager.Instance.EnergyChanged -= HandleEnergyChanged;
            GameManager.Instance.HintChanged -= HandleHintChanged;
            GameManager.Instance.LevelChanged -= HandleLevelChanged;
            GameManager.Instance.ScoreChanged -= HandleScoreChanged;
        }

        private void OnStartClicked()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OpenDifficultySelect();
            }
        }

        private void OnDifficultyChosen(DifficultyLevel difficulty)
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.StartGame(difficulty);
            }
        }

        private void OnDifficultyBackClicked()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.CancelDifficultySelect();
            }
        }

        private void OnDialogClicked()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.AcknowledgeDialog();
            }
        }

        private void OnVictoryAction()
        {
            if (GameManager.Instance == null)
            {
                return;
            }

            if (GameManager.Instance.IsFinalLevel)
            {
                GameManager.Instance.ReturnToMainMenu();
            }
            else
            {
                GameManager.Instance.AdvanceToNextLevel();
            }
        }

        private void OnRetryClicked()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.RetryLevel();
            }
        }

        private void OnQuitClicked()
        {
#if UNITY_EDITOR
            UnityEditor.EditorApplication.isPlaying = false;
#else
            Application.Quit();
#endif
        }

        private void Update()
        {
            if (settingsPanel != null && settingsPanel.activeSelf)
            {
                if (Input.GetKeyDown(KeyCode.Escape))
                {
                    HideSettings();
                }

                return;
            }

            if (creditsPanel != null && creditsPanel.activeSelf)
            {
                if (Input.GetKeyDown(KeyCode.Escape))
                {
                    HideCredits();
                }

                return;
            }

            if (howToPlayPanel != null && howToPlayPanel.activeSelf)
            {
                if (Input.GetKeyDown(KeyCode.Escape))
                {
                    HideHowToPlay();
                }

                return;
            }

            if (GameManager.Instance == null)
            {
                return;
            }

            if (GameManager.Instance.State == GameState.DifficultySelect)
            {
                if (Input.GetKeyDown(KeyCode.Escape))
                {
                    GameManager.Instance.CancelDifficultySelect();
                }

                return;
            }

            if (GameManager.Instance.State == GameState.Playing || GameManager.Instance.IsPaused)
            {
                UpdateTimer();
            }

            if (GameManager.Instance.IsPaused)
            {
                if (Input.GetKeyDown(KeyCode.Escape))
                {
                    GameManager.Instance.Resume();
                }

                return;
            }

            if (GameManager.Instance.IsPlaying && Input.GetKeyDown(KeyCode.Escape))
            {
                GameManager.Instance.Pause();
            }
        }

        private void InitializeSettings()
        {
            AudioManager audio = AudioManager.Instance;

            if (audio != null)
            {
                if (bgmSlider != null)
                {
                    bgmSlider.SetValueWithoutNotify(audio.BgmVolume);
                }

                if (sfxSlider != null)
                {
                    sfxSlider.SetValueWithoutNotify(audio.SfxVolume);
                }

                UpdateVolumeLabels(audio.BgmVolume, audio.SfxVolume);
            }

            if (PlayerPrefs.HasKey(FullscreenPrefsKey))
            {
                fullscreenOn = PlayerPrefs.GetInt(FullscreenPrefsKey, 1) == 1;
                Screen.fullScreen = fullscreenOn;
            }
            else
            {
                fullscreenOn = Screen.fullScreen;
            }

            UpdateFullscreenLabel();
        }

        private void UpdateTimer()
        {
            if (timerText != null && GameManager.Instance != null)
            {
                timerText.text = $"WAKTU  {FormatTime(GameManager.Instance.RunElapsed)}";
            }
        }

        public void ShowHowToPlay()
        {
            if (howToPlayPanel != null)
            {
                howToPlayPanel.SetActive(true);
            }
        }

        public void HideHowToPlay()
        {
            if (howToPlayPanel != null)
            {
                howToPlayPanel.SetActive(false);
            }
        }

        public void ShowSettings()
        {
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(true);
                UpdateFullscreenLabel();
            }
        }

        public void HideSettings()
        {
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(false);
            }

            PlayerPrefs.Save();
        }

        public void ShowCredits()
        {
            if (creditsPanel != null)
            {
                creditsPanel.SetActive(true);
            }
        }

        public void HideCredits()
        {
            if (creditsPanel != null)
            {
                creditsPanel.SetActive(false);
            }
        }

        private void ResumeGame()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.Resume();
            }
        }

        private void ReturnToMenu()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.ReturnToMainMenu();
            }
        }

        private void OnBgmChanged(float value)
        {
            if (AudioManager.Instance != null)
            {
                AudioManager.Instance.SetBgmVolume(value);
                UpdateVolumeLabels(AudioManager.Instance.BgmVolume, AudioManager.Instance.SfxVolume);
            }
        }

        private void OnSfxChanged(float value)
        {
            if (AudioManager.Instance != null)
            {
                AudioManager.Instance.SetSfxVolume(value);
                UpdateVolumeLabels(AudioManager.Instance.BgmVolume, AudioManager.Instance.SfxVolume);
            }
        }

        private void UpdateVolumeLabels(float bgm, float sfx)
        {
            if (bgmValueText != null)
            {
                bgmValueText.text = $"{bgm * 100f:0}%";
            }

            if (sfxValueText != null)
            {
                sfxValueText.text = $"{sfx * 100f:0}%";
            }
        }

        private void ToggleFullscreen()
        {
            fullscreenOn = !fullscreenOn;
            Screen.fullScreen = fullscreenOn;
            PlayerPrefs.SetInt(FullscreenPrefsKey, fullscreenOn ? 1 : 0);
            PlayerPrefs.Save();
            UpdateFullscreenLabel();
        }

        private void UpdateFullscreenLabel()
        {
            if (fullscreenLabel != null)
            {
                fullscreenLabel.text = fullscreenOn ? "LAYAR PENUH: AKTIF" : "LAYAR PENUH: NONAKTIF";
            }
        }

        private void HandleStateChanged(GameState state)
        {
            if (state != GameState.MainMenu && state != GameState.DifficultySelect)
            {
                HideHowToPlay();
                HideCredits();
            }

            if (state != GameState.Paused)
            {
                SetActive(pausePanel, false);
            }

            if (state != GameState.MainMenu && state != GameState.Paused && state != GameState.DifficultySelect)
            {
                HideSettings();
            }

            SetActive(mainMenuPanel, state == GameState.MainMenu);
            SetActive(difficultySelectPanel, state == GameState.DifficultySelect);
            SetActive(dialogPanel, state == GameState.IntroDialog);
            SetActive(hudPanel, state == GameState.Playing || state == GameState.Paused);
            SetActive(pausePanel, state == GameState.Paused);
            SetActive(victoryPanel, state == GameState.Victory);
            SetActive(gameOverPanel, state == GameState.GameOver);

            if (state == GameState.IntroDialog && dialogText != null && GameManager.Instance != null)
            {
                dialogText.text = GameManager.Instance.IntroDialog;
            }

            if (state == GameState.Victory && GameManager.Instance != null)
            {
                HandleVictory(GameManager.Instance);
            }

            if (state == GameState.GameOver && GameManager.Instance != null)
            {
                if (gameOverText != null)
                {
                    gameOverText.text = GameManager.Instance.LastGameOverReason;
                }

                if (gameOverScoreText != null)
                {
                    gameOverScoreText.text = $"SKOR TOTAL: {GameManager.Instance.TotalScore:N0}";
                }
            }
        }

        private void HandleVictory(GameManager manager)
        {
            if (victoryHeading != null)
            {
                victoryHeading.text = manager.IsFinalLevel
                    ? "SEMUA LEVEL SELESAI"
                    : $"LEVEL {manager.CurrentLevel} SELESAI";
            }

            if (victoryText != null)
            {
                victoryText.text = manager.VictoryDialog;
            }

            if (victoryRankText != null)
            {
                victoryRankText.text = manager.LastRank;
            }

            if (victoryLevelScoreText != null)
            {
                victoryLevelScoreText.text = $"SKOR LEVEL: {manager.LastLevelScore:N0}";
            }

            if (victoryTotalText != null)
            {
                victoryTotalText.text = $"SKOR TOTAL: {manager.TotalScore:N0}";
            }

            if (victoryBestText != null)
            {
                victoryBestText.text = manager.IsFinalLevel
                    ? (manager.IsNewRecord
                        ? $"REKOR BARU! SKOR TERBAIK: {manager.BestScore:N0}"
                        : $"SKOR TERBAIK: {manager.BestScore:N0}")
                    : string.Empty;
            }

            Button primary = victoryButton;

            if (primary != null)
            {
                Text label = primary.GetComponentInChildren<Text>();

                if (label != null)
                {
                    label.text = manager.IsFinalLevel ? "SELESAI" : "LEVEL BERIKUTNYA";
                }
            }
        }

        private void HandleLontarChanged(int count)
        {
            if (lontarText != null)
            {
                lontarText.text = $"LONTAR SUCI: {count} / {GameManager.TotalLontar}";
            }
        }

        private void HandleHealthChanged(int health)
        {
            if (hearts == null)
            {
                return;
            }

            for (int i = 0; i < hearts.Length; i++)
            {
                if (hearts[i] == null)
                {
                    continue;
                }

                hearts[i].color = i < health ? Color.white : new Color(1f, 1f, 1f, 0.18f);
            }
        }

        private void HandleEnergyChanged(float energy)
        {
            float percent = Mathf.Clamp01(energy / 100f);

            if (energyFill != null)
            {
                energyFill.fillAmount = percent;
                energyFill.color = Color.Lerp(new Color(0.85f, 0.25f, 0.25f, 1f), Gold, Mathf.InverseLerp(0.15f, 0.6f, percent));
            }

            if (energyText != null)
            {
                energyText.text = $"ENERGI LENTERA: {energy:0}%";
            }

            if (lightStatusText != null)
            {
                float exposure = Mathf.Lerp(0.7f, 1.3f, percent);
                int delta = Mathf.RoundToInt((exposure - 1f) * 100f / 5f) * 5;
                string sign = delta >= 0 ? "+" : string.Empty;

                if (percent >= 0.66f)
                {
                    lightStatusText.text = $"CAHAYA: TERANG  ·  deteksi musuh {sign}{delta}%";
                    lightStatusText.color = Gold;
                }
                else if (percent <= 0.34f)
                {
                    lightStatusText.text = $"CAHAYA: REDUP  ·  deteksi musuh {sign}{delta}%";
                    lightStatusText.color = Cyan;
                }
                else
                {
                    lightStatusText.text = $"CAHAYA: SEIMBANG  ·  deteksi musuh {sign}{delta}%";
                    lightStatusText.color = new Color(0.88f, 0.88f, 0.92f, 1f);
                }
            }
        }

        private void HandleHintChanged(string message)
        {
            if (hintText == null)
            {
                return;
            }

            hintText.text = message;

            if (hintRoutine != null)
            {
                StopCoroutine(hintRoutine);
            }

            if (!string.IsNullOrEmpty(message))
            {
                hintRoutine = StartCoroutine(ClearHintAfterDelay(7f));
            }
        }

        private void HandleLevelChanged(int level)
        {
            if (levelText != null && GameManager.Instance != null)
            {
                levelText.text = $"LEVEL {level}/{GameManager.Instance.LevelCount} — {GameManager.Instance.CurrentLevelName}";
            }
        }

        private void HandleScoreChanged(int score)
        {
            if (scoreText != null)
            {
                scoreText.text = $"SKOR: {score:N0}";
            }
        }

        private IEnumerator ClearHintAfterDelay(float delay)
        {
            yield return new WaitForSeconds(delay);

            if (hintText != null)
            {
                hintText.text = string.Empty;
            }
        }

        private static string FormatTime(float seconds)
        {
            int total = Mathf.Max(0, Mathf.FloorToInt(seconds));
            return $"{total / 60:00}:{total % 60:00}";
        }

        private static void SetActive(GameObject panel, bool active)
        {
            if (panel != null && panel.activeSelf != active)
            {
                panel.SetActive(active);
            }
        }
    }
}
