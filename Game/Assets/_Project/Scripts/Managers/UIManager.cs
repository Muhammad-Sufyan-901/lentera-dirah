using System.Collections;
using UnityEngine;
using UnityEngine.UI;

namespace LenteraDirah
{
    public class UIManager : MonoBehaviour
    {
        private static readonly Color Gold = new Color(1f, 0.721f, 0.302f, 1f);
        private static readonly Color DimGold = new Color(1f, 0.721f, 0.302f, 0.25f);

        [Header("Panel")]
        [SerializeField] private GameObject mainMenuPanel;
        [SerializeField] private GameObject dialogPanel;
        [SerializeField] private GameObject hudPanel;
        [SerializeField] private GameObject victoryPanel;
        [SerializeField] private GameObject gameOverPanel;

        [Header("HUD")]
        [SerializeField] private Text lontarText;
        [SerializeField] private Text energyText;
        [SerializeField] private Text hintText;
        [SerializeField] private Image energyFill;
        [SerializeField] private Image[] hearts;

        [Header("Dialog & Layar Akhir")]
        [SerializeField] private Text dialogText;
        [SerializeField] private Text victoryText;
        [SerializeField] private Text gameOverText;

        [Header("Tombol")]
        [SerializeField] private Button startButton;
        [SerializeField] private Button dialogButton;
        [SerializeField] private Button victoryButton;
        [SerializeField] private Button gameOverButton;

        private Coroutine hintRoutine;

        private void Awake()
        {
            if (startButton != null)
            {
                startButton.onClick.AddListener(OnStartClicked);
            }

            if (dialogButton != null)
            {
                dialogButton.onClick.AddListener(OnDialogClicked);
            }

            if (victoryButton != null)
            {
                victoryButton.onClick.AddListener(OnRestartClicked);
            }

            if (gameOverButton != null)
            {
                gameOverButton.onClick.AddListener(OnRestartClicked);
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

                HandleStateChanged(GameManager.Instance.State);
                HandleLontarChanged(GameManager.Instance.LontarCollected);
                HandleHealthChanged(GameManager.Instance.Health);
                HandleEnergyChanged(100f);
            }
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
        }

        private void OnStartClicked()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.StartPurification();
            }
        }

        private void OnDialogClicked()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.AcknowledgeDialog();
            }
        }

        private void OnRestartClicked()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.RestartScene();
            }
        }

        private void HandleStateChanged(GameState state)
        {
            SetActive(mainMenuPanel, state == GameState.MainMenu);
            SetActive(dialogPanel, state == GameState.IntroDialog);
            SetActive(hudPanel, state == GameState.Playing);
            SetActive(victoryPanel, state == GameState.Victory);
            SetActive(gameOverPanel, state == GameState.GameOver);

            if (state == GameState.IntroDialog && dialogText != null && GameManager.Instance != null)
            {
                dialogText.text = GameManager.Instance.IntroDialog;
            }

            if (state == GameState.Victory && victoryText != null && GameManager.Instance != null)
            {
                victoryText.text = GameManager.Instance.VictoryDialog;
            }

            if (state == GameState.GameOver && gameOverText != null && GameManager.Instance != null)
            {
                gameOverText.text = GameManager.Instance.LastGameOverReason;
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

        private IEnumerator ClearHintAfterDelay(float delay)
        {
            yield return new WaitForSeconds(delay);

            if (hintText != null)
            {
                hintText.text = string.Empty;
            }
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
