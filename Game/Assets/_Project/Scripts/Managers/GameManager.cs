using System;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace LenteraDirah
{
    public enum GameState
    {
        MainMenu,
        IntroDialog,
        Playing,
        Victory,
        GameOver
    }

    public class GameManager : MonoBehaviour
    {
        public static GameManager Instance { get; private set; }

        public const int TotalLontar = 3;
        public const int MaxHealth = 3;

        [Header("Referensi Sistem")]
        [SerializeField] private PlayerController player;
        [SerializeField] private UIManager uiManager;
        [SerializeField] private AudioManager audioManager;

        [Header("Naskah Dialog")]
        [TextArea(3, 8)]
        [SerializeField] private string introDialog =
            "Bahula, muridku... Kabut wabah dari Setra Gandamayu telah menyelimuti Desa Girah. " +
            "Bawalah Lentera Suci ini. Temukan 3 Lontar Kuno yang tercecer di penjuru desa dan " +
            "kembalikan ke Altar Tengah. Ingatlah ajaran Rwa Bhineda: jangan gunakan amarah, " +
            "gunakan pancaran cahaya lenteramu (tombol SPACE) untuk menenangkan bayangan kegelapan " +
            "yang menghalangi jalanmu.";

        [TextArea(3, 8)]
        [SerializeField] private string victoryDialog =
            "Luar biasa, Bahula! Ketiga Lontar Suci—Usada, Dharma, dan Rwa Bhineda—telah kembali " +
            "bersatu di Altar Penyucian. Cahaya pengetahuan kini memulihkan keseimbangan Desa Girah, " +
            "dan kabut wabah pun mereda.";

        [SerializeField] private string gameOverReason = "Lentera Suci padam...";

        public GameState State { get; private set; } = GameState.MainMenu;
        public int LontarCollected { get; private set; }
        public int Health { get; private set; } = MaxHealth;
        public string LastGameOverReason { get; private set; } = string.Empty;

        public string IntroDialog => introDialog;
        public string VictoryDialog => victoryDialog;
        public bool IsPlaying => State == GameState.Playing;

        public event Action<GameState> StateChanged;
        public event Action<int> LontarChanged;
        public event Action<int> HealthChanged;
        public event Action<float> EnergyChanged;
        public event Action<string> HintChanged;

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
            SetState(GameState.MainMenu);
            if (audioManager != null)
            {
                audioManager.PlayBgm();
            }
        }

        private void Update()
        {
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

        public void StartPurification()
        {
            if (State != GameState.MainMenu)
            {
                return;
            }

            SetState(GameState.IntroDialog);
        }

        public void AcknowledgeDialog()
        {
            if (State != GameState.IntroDialog)
            {
                return;
            }

            SetState(GameState.Playing);
            SetHint("Cari 3 Lontar Suci. Tekan SPACE untuk Holy Light Burst.");
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
                SetHint("Ketiga Lontar Suci lengkap! Bawa Bahula ke Altar Penyucian di tengah desa.");
            }
        }

        public void NotifyHealthChanged(int health)
        {
            Health = Mathf.Clamp(health, 0, MaxHealth);
            HealthChanged?.Invoke(Health);
        }

        public void NotifyEnergyChanged(float energy)
        {
            EnergyChanged?.Invoke(energy);
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

        public void RestartScene()
        {
            Time.timeScale = 1f;
            SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
        }

        private void SetState(GameState next)
        {
            State = next;

            if (player != null)
            {
                player.OnGameStateChanged(next);
            }

            if (next == GameState.Victory || next == GameState.GameOver)
            {
                SetHint(string.Empty);
            }

            StateChanged?.Invoke(next);
        }
    }
}
