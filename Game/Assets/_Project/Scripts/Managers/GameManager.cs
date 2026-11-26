using System;
using UnityEngine;

namespace LenteraDirah
{
    public enum GameState
    {
        MainMenu,
        DifficultySelect,
        IntroDialog,
        Playing,
        Paused,
        Victory,
        GameOver
    }

    public class GameManager : MonoBehaviour
    {
        public static GameManager Instance { get; private set; }

        public const int TotalLontar = 3;
        public const int MaxHealth = 3;
        public const string BestScorePrefsKey = "ld_best_score";
        public const int DefaultLevelCount = 3;

        private const float AgungTimeLimit = 150f;
        private const float TeladanTimeLimit = 240f;

        [Header("Referensi Sistem")]
        [SerializeField] private PlayerController player;
        [SerializeField] private UIManager uiManager;
        [SerializeField] private AudioManager audioManager;
        [SerializeField] private LevelManager levelManager;

        [Header("Naskah Dialog")]
        [TextArea(3, 8)]
        [SerializeField] private string introDialog =
            "Bahula, muridku... Kabut wabah dari Setra Gandamayu telah menyelimuti tiga wilayah: Desa Girah, " +
            "Hutan Bambu Lemah Tulis, dan Pelataran Setra Gandamayu. Bawalah Lentera Suci ini. Di setiap wilayah, " +
            "temukan 3 Lontar Kuno dan kembalikan ke Altar setempat. Ingatlah ajaran Rwa Bhineda: jangan gunakan " +
            "amarah, gunakan pancaran cahaya lenteramu (tombol SPACE) untuk menenangkan bayangan kegelapan yang " +
            "menghalangi jalanmu.";

        [TextArea(3, 8)]
        [SerializeField] private string victoryDialog =
            "Luar biasa, Bahula! Ketiga Lontar Suci telah kembali bersatu di Altar Penyucian. Cahaya pengetahuan " +
            "memulihkan keseimbangan wilayah ini, dan kabut wabah pun mereda.";

        [SerializeField] private string gameOverReason = "Lentera Suci padam...";

        public GameState State { get; private set; } = GameState.MainMenu;
        public int CurrentLevel { get; private set; } = 1;
        public int LontarCollected { get; private set; }
        public int Health { get; private set; } = MaxHealth;
        public string LastGameOverReason { get; private set; } = string.Empty;

        public float RunElapsed { get; private set; }
        public float LastRunSeconds { get; private set; }
        public float CurrentEnergy { get; private set; } = 100f;
        public string LastRank { get; private set; } = string.Empty;

        public int LastLevelScore { get; private set; }
        public int TotalScore { get; private set; }
        public int BestScore { get; private set; }
        public bool IsNewRecord { get; private set; }

        public string IntroDialog => introDialog;
        public string VictoryDialog => victoryDialog;
        public bool IsPlaying => State == GameState.Playing;
        public bool IsPaused => State == GameState.Paused;
        public int LevelCount => levelManager != null ? levelManager.LevelCount : DefaultLevelCount;
        public bool IsFinalLevel => CurrentLevel >= LevelCount;
        public string CurrentLevelName => levelManager != null ? levelManager.CurrentLevelName : "Desa Girah";
        public string CurrentObjective => levelManager != null ? levelManager.CurrentObjective : string.Empty;

        public event Action<GameState> StateChanged;
        public event Action<int> LontarChanged;
        public event Action<int> HealthChanged;
        public event Action<float> EnergyChanged;
        public event Action<string> HintChanged;
        public event Action<int> LevelChanged;
        public event Action<int> ScoreChanged;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            Time.timeScale = 1f;
        }

        private void Start()
        {
            BestScore = PlayerPrefs.GetInt(BestScorePrefsKey, 0);
            SetState(GameState.MainMenu);

            if (audioManager != null)
            {
                audioManager.PlayBgm();
            }
        }

        private void Update()
        {
            if (State == GameState.Playing)
            {
                RunElapsed += Time.deltaTime;
            }

            if (State == GameState.IntroDialog && Input.GetKeyDown(KeyCode.E))
            {
                AcknowledgeDialog();
            }
        }

        private void OnDestroy()
        {
            if (Instance == this)
            {
                Instance = null;
            }
        }

        public void OpenDifficultySelect()
        {
            if (State != GameState.MainMenu)
            {
                return;
            }

            SetState(GameState.DifficultySelect);
        }

        public void CancelDifficultySelect()
        {
            if (State != GameState.DifficultySelect)
            {
                return;
            }

            SetState(GameState.MainMenu);
        }

        public void StartGame(DifficultyLevel difficulty)
        {
            if (State != GameState.DifficultySelect)
            {
                return;
            }

            DifficultySettings.Set(difficulty);

            CurrentLevel = 1;
            TotalScore = 0;
            LastLevelScore = 0;
            LastRank = string.Empty;
            IsNewRecord = false;
            BestScore = PlayerPrefs.GetInt(BestScorePrefsKey, 0);
            ResetLevelCounters();

            if (levelManager != null)
            {
                levelManager.LoadLevel(CurrentLevel);
            }

            LontarChanged?.Invoke(0);
            LevelChanged?.Invoke(CurrentLevel);
            ScoreChanged?.Invoke(TotalScore);
            SetState(GameState.IntroDialog);
        }

        public void AcknowledgeDialog()
        {
            if (State != GameState.IntroDialog)
            {
                return;
            }

            ApplyDifficultySettings();
            RunElapsed = 0f;
            SetState(GameState.Playing);
            ShowLevelHint();
        }

        public void AdvanceToNextLevel()
        {
            if (State != GameState.Victory || IsFinalLevel)
            {
                return;
            }

            CurrentLevel++;
            ResetLevelCounters();

            if (levelManager != null)
            {
                levelManager.LoadLevel(CurrentLevel);
            }

            ApplyDifficultySettings();
            LontarChanged?.Invoke(0);
            LevelChanged?.Invoke(CurrentLevel);
            SetState(GameState.Playing);
            ShowLevelHint();
        }

        public void RetryLevel()
        {
            if (State != GameState.GameOver)
            {
                return;
            }

            ResetLevelCounters();

            if (levelManager != null)
            {
                levelManager.LoadLevel(CurrentLevel);
            }

            ApplyDifficultySettings();
            LontarChanged?.Invoke(0);
            LevelChanged?.Invoke(CurrentLevel);
            SetState(GameState.Playing);
            ShowLevelHint();
        }

        public void CollectLontar(string lontarName, string wisdomQuote)
        {
            if (State != GameState.Playing)
            {
                return;
            }

            LontarCollected = Mathf.Clamp(LontarCollected + 1, 0, TotalLontar);
            LontarChanged?.Invoke(LontarCollected);

            if (audioManager != null)
            {
                audioManager.PlaySfx(AudioManager.Sfx.Lontar);
            }

            SetHint($"{lontarName} ditemukan ({LontarCollected}/{TotalLontar})! {wisdomQuote}");

            if (LontarCollected >= TotalLontar)
            {
                SetHint($"Ketiga Lontar lengkap! Bawa Bahula ke Altar Penyucian di {CurrentLevelName}.");
            }
        }

        public void NotifyHealthChanged(int health)
        {
            Health = Mathf.Clamp(health, 0, MaxHealth);
            HealthChanged?.Invoke(Health);
        }

        public void NotifyEnergyChanged(float energy)
        {
            CurrentEnergy = Mathf.Clamp(energy, 0f, 100f);
            EnergyChanged?.Invoke(CurrentEnergy);
        }

        public void SetHint(string message)
        {
            HintChanged?.Invoke(message);
        }

        public void PurifyAltar()
        {
            if (State != GameState.Playing || LontarCollected < TotalLontar)
            {
                return;
            }

            if (audioManager != null)
            {
                audioManager.PlaySfx(AudioManager.Sfx.Victory);
            }

            LastRunSeconds = RunElapsed;
            LastRank = CalculateRank(LastRunSeconds, Health);
            LastLevelScore = CalculateLevelScore(LastRunSeconds, Health, CurrentEnergy);
            TotalScore += LastLevelScore;

            BestScore = PlayerPrefs.GetInt(BestScorePrefsKey, 0);
            IsNewRecord = false;

            if (IsFinalLevel && TotalScore > BestScore)
            {
                BestScore = TotalScore;
                IsNewRecord = true;
                PlayerPrefs.SetInt(BestScorePrefsKey, BestScore);
                PlayerPrefs.Save();
            }

            ScoreChanged?.Invoke(TotalScore);
            SetState(GameState.Victory);
        }

        public void RequestGameOver(string reason)
        {
            if (State != GameState.Playing)
            {
                return;
            }

            LastGameOverReason = string.IsNullOrEmpty(reason) ? gameOverReason : reason;
            SetState(GameState.GameOver);
        }

        public void Pause()
        {
            if (State != GameState.Playing)
            {
                return;
            }

            Time.timeScale = 0f;
            SetState(GameState.Paused);
        }

        public void Resume()
        {
            if (State != GameState.Paused)
            {
                return;
            }

            Time.timeScale = 1f;
            SetState(GameState.Playing);
        }

        public void ReturnToMainMenu()
        {
            Time.timeScale = 1f;
            SetState(GameState.MainMenu);
        }

        private void ShowLevelHint()
        {
            SetHint($"LEVEL {CurrentLevel} — {CurrentLevelName}: {CurrentObjective}");
        }

        private void ResetLevelCounters()
        {
            LontarCollected = 0;
            Health = MaxHealth;
            CurrentEnergy = 100f;
            RunElapsed = 0f;
        }

        private void ApplyDifficultySettings()
        {
            if (player != null)
            {
                player.ApplyDifficulty();
            }

            EnemyShadowAI[] shadows = UnityEngine.Object.FindObjectsByType<EnemyShadowAI>(FindObjectsSortMode.None);

            foreach (EnemyShadowAI shadow in shadows)
            {
                shadow.ApplyDifficulty();
            }
        }

        private static string CalculateRank(float seconds, int health)
        {
            if (seconds <= AgungTimeLimit && health >= MaxHealth)
            {
                return "PENYUCI AGUNG";
            }

            if (seconds <= TeladanTimeLimit && health >= 2)
            {
                return "MURID TELADAN";
            }

            return "PEJALAN MALAM";
        }

        private static int CalculateLevelScore(float seconds, int health, float energy)
        {
            int timeBonus = Mathf.Max(0, 600 - Mathf.RoundToInt(seconds) * 5);
            int healthBonus = health * 100;
            int energyBonus = Mathf.RoundToInt(energy) * 2;
            const int completionBonus = 500;

            return Mathf.RoundToInt((completionBonus + timeBonus + healthBonus + energyBonus) * DifficultySettings.ScoreMultiplier);
        }

        private void SetState(GameState next)
        {
            State = next;

            if (player != null)
            {
                player.OnGameStateChanged(next);
            }

            if (next == GameState.Victory || next == GameState.GameOver ||
                next == GameState.MainMenu || next == GameState.DifficultySelect)
            {
                SetHint(string.Empty);
            }

            StateChanged?.Invoke(next);
        }
    }
}
