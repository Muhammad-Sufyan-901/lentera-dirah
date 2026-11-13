using UnityEngine;
using UnityEngine.Rendering.Universal;

namespace LenteraDirah
{
    public class AltarPurification : MonoBehaviour
    {
        [Header("Syarat Penyucian")]
        [SerializeField] private int requiredLontar = GameManager.TotalLontar;

        [Header("Visual Segel")]
        [SerializeField] private Light2D altarLight;
        [SerializeField] private SpriteRenderer spriteRenderer;
        [SerializeField] private Color sealedColor = new Color(0.27f, 0.18f, 0.3f, 1f);
        [SerializeField] private Color unsealedColor = new Color(1f, 0.721f, 0.302f, 1f);
        [SerializeField] private float sealedIntensity = 0.25f;
        [SerializeField] private float unsealedIntensity = 2.6f;

        public bool IsUnsealed => isUnsealed;

        private bool isUnsealed;
        private float pulseTime;

        private void Start()
        {
            ApplySealedVisual();
        }

        private void Update()
        {
            if (!isUnsealed &&
                GameManager.Instance != null &&
                GameManager.Instance.LontarCollected >= requiredLontar)
            {
                Unseal();
            }

            if (isUnsealed && altarLight != null)
            {
                pulseTime += Time.deltaTime;
                altarLight.intensity = unsealedIntensity + Mathf.Sin(pulseTime * 2f) * 0.35f;
            }
        }

        public void Unseal()
        {
            if (isUnsealed)
            {
                return;
            }

            isUnsealed = true;

            if (altarLight != null)
            {
                altarLight.color = unsealedColor;
                altarLight.intensity = unsealedIntensity;
            }

            if (spriteRenderer != null)
            {
                spriteRenderer.color = Color.white;
            }

            if (GameManager.Instance != null)
            {
                GameManager.Instance.SetHint("Segel Altar Penyucian terbuka! Sentuh Altar untuk menyucikan Desa Girah.");
            }
        }

        private void ApplySealedVisual()
        {
            if (altarLight != null)
            {
                altarLight.color = sealedColor;
                altarLight.intensity = sealedIntensity;
            }

            if (spriteRenderer != null)
            {
                spriteRenderer.color = new Color(0.75f, 0.7f, 0.85f, 1f);
            }
        }

        private void OnTriggerEnter2D(Collider2D other)
        {
            if (!other.CompareTag("Player") || GameManager.Instance == null)
            {
                return;
            }

            if (isUnsealed)
            {
                GameManager.Instance.PurifyAltar();
                return;
            }

            GameManager.Instance.SetHint($"Altar Penyucian masih tersegel. Kumpulkan Lontar Suci ({GameManager.Instance.LontarCollected}/{requiredLontar}).");
        }
    }
}
