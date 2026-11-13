using UnityEngine;
using UnityEngine.Rendering.Universal;

namespace LenteraDirah
{
    public enum CollectibleType
    {
        Lontar,
        Oil
    }

    public class CollectibleItem : MonoBehaviour
    {
        [Header("Jenis Item")]
        [SerializeField] private CollectibleType itemType = CollectibleType.Lontar;
        [SerializeField] private string lontarName = "Lontar Usada";
        [TextArea(2, 4)]
        [SerializeField] private string wisdomQuote = string.Empty;
        [SerializeField] private float energyAmount = 35f;

        [Header("Animasi Mengambang")]
        [SerializeField] private float floatAmplitude = 0.12f;
        [SerializeField] private float floatFrequency = 2.2f;

        [Header("Visual")]
        [SerializeField] private Light2D glowLight;
        [SerializeField] private float glowBaseIntensity = 0.9f;

        private Vector3 basePosition;
        private bool collected;

        private void Start()
        {
            basePosition = transform.position;
        }

        private void Update()
        {
            float wave = Mathf.Sin(Time.time * floatFrequency);
            transform.position = basePosition + Vector3.up * (wave * floatAmplitude);

            if (glowLight != null)
            {
                glowLight.intensity = glowBaseIntensity + wave * 0.25f;
            }
        }

        private void OnTriggerEnter2D(Collider2D other)
        {
            if (collected || !other.CompareTag("Player"))
            {
                return;
            }

            PlayerController player = other.GetComponent<PlayerController>();

            if (player == null)
            {
                player = other.GetComponentInParent<PlayerController>();
            }

            if (player == null || GameManager.Instance == null)
            {
                return;
            }

            collected = true;

            if (itemType == CollectibleType.Lontar)
            {
                GameManager.Instance.CollectLontar(lontarName, wisdomQuote);
            }
            else
            {
                player.AddEnergy(energyAmount);

                if (AudioManager.Instance != null)
                {
                    AudioManager.Instance.PlaySfx(AudioManager.Sfx.Oil);
                }

                GameManager.Instance.SetHint($"Minyak Obor: energi lentera +{energyAmount:0}%.");
            }

            Destroy(gameObject);
        }
    }
}
