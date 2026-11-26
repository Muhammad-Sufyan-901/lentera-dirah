using System.Collections;
using UnityEngine;
using UnityEngine.Rendering.Universal;

namespace LenteraDirah
{
    public enum PlayerState
    {
        Idle,
        Walking,
        CastingLight,
        Hurt
    }

    [RequireComponent(typeof(Rigidbody2D))]
    public class PlayerController : MonoBehaviour
    {
        [Header("Pergerakan")]
        [SerializeField] private float moveSpeed = 4.5f;

        [Header("Energi Lentera")]
        [SerializeField] private float maxEnergy = 100f;
        [SerializeField] private float decayPerSecond = 2f;
        [SerializeField] private Light2D lanternLight;
        [SerializeField] private float maxOuterRadius = 6f;
        [SerializeField] private float minOuterRadius = 1.8f;
        [SerializeField] private float lanternIntensity = 1.4f;

        [Header("Holy Light Burst")]
        [SerializeField] private float burstCost = 15f;
        [SerializeField] private float burstCooldown = 4f;
        [SerializeField] private float burstRadius = 3.5f;
        [SerializeField] private float stunDuration = 3f;
        [SerializeField] private float castDuration = 0.3f;
        [SerializeField] private LayerMask enemyMask;

        [Header("Nyawa")]
        [SerializeField] private int maxHealth = GameManager.MaxHealth;
        [SerializeField] private float invulnerabilityDuration = 1f;

        [Header("Visual")]
        [SerializeField] private SpriteRenderer spriteRenderer;
        [SerializeField] private Animator animator;

        public PlayerState State { get; private set; } = PlayerState.Idle;
        public float Energy { get; private set; }
        public int Health { get; private set; }
        public bool IsInvulnerable => isInvulnerable;

        private Rigidbody2D body;
        private Vector2 moveInput;
        private Vector2 facing = Vector2.down;
        private float cooldownTimer;
        private float castBoost = 1f;
        private bool isInvulnerable;
        private string currentAnimation;

#if UNITY_EDITOR
        private Vector2 scriptedInput;
        private bool useScriptedInput;
        private bool recordingInvulnerable;

        public void SetScriptedInput(Vector2 input)
        {
            scriptedInput = input;
            useScriptedInput = true;
        }

        public void ClearScriptedInput()
        {
            useScriptedInput = false;
            scriptedInput = Vector2.zero;
        }

        public void SetRecordingInvulnerable(bool value)
        {
            recordingInvulnerable = value;
        }
#endif

        private void Awake()
        {
            body = GetComponent<Rigidbody2D>();
            Energy = maxEnergy;
            Health = maxHealth;
        }

        private void Start()
        {
            ApplyEnergyToLantern();

            if (GameManager.Instance != null)
            {
                GameManager.Instance.NotifyHealthChanged(Health);
                GameManager.Instance.NotifyEnergyChanged(Energy);
            }
        }

        private void Update()
        {
            bool playing = GameManager.Instance != null && GameManager.Instance.IsPlaying;

            if (!playing)
            {
                moveInput = Vector2.zero;
                PlayAnimation(true);
                return;
            }

            ReadInput();

            if (cooldownTimer > 0f)
            {
                cooldownTimer -= Time.deltaTime;
            }

            if (Input.GetKeyDown(KeyCode.Space))
            {
                TryHolyLightBurst();
            }

            DrainLanternEnergy();

            if (State != PlayerState.Hurt && State != PlayerState.CastingLight)
            {
                SetState(moveInput.sqrMagnitude > 0.001f ? PlayerState.Walking : PlayerState.Idle);
            }

            PlayAnimation(false);
        }

        private void FixedUpdate()
        {
            bool playing = GameManager.Instance != null && GameManager.Instance.IsPlaying;

            if (!playing || State == PlayerState.Hurt)
            {
                body.linearVelocity = Vector2.zero;
                return;
            }

            body.linearVelocity = moveInput * moveSpeed;
        }

        private void ReadInput()
        {
#if UNITY_EDITOR
            Vector2 raw = useScriptedInput
                ? scriptedInput
                : new Vector2(Input.GetAxisRaw("Horizontal"), Input.GetAxisRaw("Vertical"));
#else
            Vector2 raw = new Vector2(Input.GetAxisRaw("Horizontal"), Input.GetAxisRaw("Vertical"));
#endif

            if (raw.sqrMagnitude > 0.01f)
            {
                moveInput = raw.normalized;
                facing = Mathf.Abs(moveInput.x) >= Mathf.Abs(moveInput.y)
                    ? new Vector2(Mathf.Sign(moveInput.x), 0f)
                    : new Vector2(0f, Mathf.Sign(moveInput.y));
            }
            else
            {
                moveInput = Vector2.zero;
            }
        }

        private void DrainLanternEnergy()
        {
            if (Energy <= 0f)
            {
                return;
            }

            Energy = Mathf.Max(0f, Energy - decayPerSecond * Time.deltaTime);
            ApplyEnergyToLantern();

            if (GameManager.Instance != null)
            {
                GameManager.Instance.NotifyEnergyChanged(Energy);
            }

            if (Energy <= 0f && GameManager.Instance != null)
            {
                GameManager.Instance.RequestGameOver("Lentera Suci padam. Kegelapan wabah menelan Bahula...");
            }
        }

        private void ApplyEnergyToLantern()
        {
            if (lanternLight == null)
            {
                return;
            }

            float percent = Mathf.Clamp01(Energy / maxEnergy);
            lanternLight.pointLightOuterRadius = Mathf.Lerp(minOuterRadius, maxOuterRadius, percent) * castBoost;
            lanternLight.pointLightInnerRadius = Mathf.Lerp(0.25f, 0.9f, percent) * castBoost;
            lanternLight.intensity = lanternIntensity;
        }

        private void TryHolyLightBurst()
        {
            if (State == PlayerState.Hurt || cooldownTimer > 0f || Energy < burstCost)
            {
                return;
            }

            Energy -= burstCost;
            cooldownTimer = burstCooldown;
            ApplyEnergyToLantern();

            if (GameManager.Instance != null)
            {
                GameManager.Instance.NotifyEnergyChanged(Energy);
            }

            if (AudioManager.Instance != null)
            {
                AudioManager.Instance.PlaySfx(AudioManager.Sfx.Burst);
            }

            Collider2D[] hits = Physics2D.OverlapCircleAll(transform.position, burstRadius, enemyMask);

            foreach (Collider2D hit in hits)
            {
                EnemyShadowAI enemy = hit.GetComponentInParent<EnemyShadowAI>();
                if (enemy != null)
                {
                    enemy.Stun(stunDuration);
                }
            }

            StartCoroutine(CastLightRoutine());
        }

        private IEnumerator CastLightRoutine()
        {
            SetState(PlayerState.CastingLight);

            float elapsed = 0f;

            while (elapsed < castDuration)
            {
                elapsed += Time.deltaTime;
                float phase = Mathf.Clamp01(elapsed / castDuration);
                castBoost = Mathf.Lerp(2.4f, 1f, phase);
                ApplyEnergyToLantern();
                yield return null;
            }

            castBoost = 1f;
            ApplyEnergyToLantern();
            SetState(PlayerState.Idle);
        }

        public void AddEnergy(float amount)
        {
            Energy = Mathf.Clamp(Energy + amount, 0f, maxEnergy);
            ApplyEnergyToLantern();

            if (GameManager.Instance != null)
            {
                GameManager.Instance.NotifyEnergyChanged(Energy);
            }
        }

        public void TakeDamage(int amount = 1)
        {
#if UNITY_EDITOR
            if (recordingInvulnerable)
            {
                return;
            }
#endif

            if (isInvulnerable || State == PlayerState.Hurt)
            {
                return;
            }

            if (GameManager.Instance != null && !GameManager.Instance.IsPlaying)
            {
                return;
            }

            Health = Mathf.Max(0, Health - amount);

            if (GameManager.Instance != null)
            {
                GameManager.Instance.NotifyHealthChanged(Health);
            }

            if (AudioManager.Instance != null)
            {
                AudioManager.Instance.PlaySfx(AudioManager.Sfx.Hurt);
            }

            if (Health <= 0)
            {
                if (GameManager.Instance != null)
                {
                    GameManager.Instance.RequestGameOver("Nyawa Bahula habis. Bayangan wabah menguasai Desa Girah...");
                }

                return;
            }

            StartCoroutine(HurtRoutine());
        }

        private IEnumerator HurtRoutine()
        {
            isInvulnerable = true;
            SetState(PlayerState.Hurt);

            Color original = spriteRenderer != null ? spriteRenderer.color : Color.white;
            float elapsed = 0f;

            while (elapsed < invulnerabilityDuration)
            {
                elapsed += Time.deltaTime;

                if (spriteRenderer != null)
                {
                    spriteRenderer.color = Mathf.Repeat(elapsed, 0.2f) < 0.1f
                        ? new Color(1f, 0.35f, 0.35f, 0.85f)
                        : original;
                }

                yield return null;
            }

            if (spriteRenderer != null)
            {
                spriteRenderer.color = original;
            }

            isInvulnerable = false;
            SetState(PlayerState.Idle);
        }

        public void OnGameStateChanged(GameState state)
        {
            if (state != GameState.Playing)
            {
                moveInput = Vector2.zero;

                if (body != null)
                {
                    body.linearVelocity = Vector2.zero;
                }

                if (state == GameState.Victory || state == GameState.GameOver)
                {
                    SetState(PlayerState.Idle);
                }
            }
        }

        private void SetState(PlayerState next)
        {
            if (State == next)
            {
                return;
            }

            State = next;
        }

        private void PlayAnimation(bool force)
        {
            if (animator == null)
            {
                return;
            }

            string direction = DirectionName(facing);
            string clip = State == PlayerState.Walking ? $"Walk_{direction}" : $"Idle_{direction}";

            if (!force && clip == currentAnimation)
            {
                return;
            }

            currentAnimation = clip;
            animator.Play(clip, 0, 0f);
        }

        private static string DirectionName(Vector2 dir)
        {
            if (Mathf.Abs(dir.x) >= Mathf.Abs(dir.y))
            {
                return dir.x < 0f ? "Left" : "Right";
            }

            return dir.y < 0f ? "Down" : "Up";
        }

        private void OnDrawGizmosSelected()
        {
            Gizmos.color = new Color(0.392f, 0.784f, 1f, 0.6f);
            Gizmos.DrawWireSphere(transform.position, burstRadius);
        }
    }
}
