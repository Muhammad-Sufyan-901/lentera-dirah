using UnityEngine;
using UnityEngine.Rendering.Universal;

namespace LenteraDirah
{
    public enum EnemyState
    {
        Patrol,
        Chase,
        Stunned
    }

    [RequireComponent(typeof(Rigidbody2D))]
    public class EnemyShadowAI : MonoBehaviour
    {
        [Header("Patroli")]
        [SerializeField] private Transform[] waypoints;
        [SerializeField] private float patrolSpeed = 2.2f;
        [SerializeField] private float arrivalDistance = 0.2f;

        [Header("Pengejaran")]
        [SerializeField] private PlayerController player;
        [SerializeField] private float chaseSpeed = 3.4f;
        [SerializeField] private float detectRadius = 4f;
        [SerializeField] private float loseRadius = 5.5f;

        [Header("Stun Rwa Bhineda")]
        [SerializeField] private float stunDuration = 3f;

        [Header("Visual")]
        [SerializeField] private SpriteRenderer spriteRenderer;
        [SerializeField] private Light2D auraLight;
        [SerializeField] private Color patrolTint = new Color(0.42f, 0.176f, 0.361f, 0.95f);
        [SerializeField] private Color stunnedTint = new Color(0.392f, 0.784f, 1f, 0.55f);

        public EnemyState State { get; private set; } = EnemyState.Patrol;
        public float StunRemaining => stunTimer;

        private Rigidbody2D body;
        private int waypointIndex;
        private float stunTimer;
        private float auraBaseIntensity = 0.55f;

        private void Awake()
        {
            body = GetComponent<Rigidbody2D>();

            if (auraLight != null)
            {
                auraBaseIntensity = auraLight.intensity;
            }
        }

        private void Start()
        {
            if (player == null)
            {
                player = FindAnyObjectByType<PlayerController>();
            }

            ApplyTint(patrolTint);
        }

        private void Update()
        {
            bool playing = GameManager.Instance != null && GameManager.Instance.IsPlaying;

            if (!playing)
            {
                body.linearVelocity = Vector2.zero;
                return;
            }

            if (State == EnemyState.Stunned)
            {
                stunTimer -= Time.deltaTime;

                if (auraLight != null)
                {
                    auraLight.intensity = auraBaseIntensity + Mathf.Abs(Mathf.Sin(Time.time * 6f)) * 0.6f;
                }

                if (stunTimer <= 0f)
                {
                    SetState(EnemyState.Patrol);
                }

                return;
            }

            if (player != null)
            {
                float distance = Vector2.Distance(transform.position, player.transform.position);

                if (State == EnemyState.Patrol && distance <= detectRadius)
                {
                    SetState(EnemyState.Chase);
                }
                else if (State == EnemyState.Chase && distance > loseRadius)
                {
                    SetState(EnemyState.Patrol);
                }
            }

            if (spriteRenderer != null && Mathf.Abs(body.linearVelocity.x) > 0.05f)
            {
                spriteRenderer.flipX = body.linearVelocity.x < 0f;
            }
        }

        private void FixedUpdate()
        {
            bool playing = GameManager.Instance != null && GameManager.Instance.IsPlaying;

            if (!playing || State == EnemyState.Stunned)
            {
                body.linearVelocity = Vector2.zero;
                return;
            }

            if (State == EnemyState.Chase && player != null)
            {
                Vector2 direction = ((Vector2)player.transform.position - (Vector2)transform.position).normalized;
                body.linearVelocity = direction * chaseSpeed;
                return;
            }

            PatrolStep();
        }

        private void PatrolStep()
        {
            if (waypoints == null || waypoints.Length == 0)
            {
                body.linearVelocity = Vector2.zero;
                return;
            }

            Transform target = waypoints[waypointIndex];

            if (target == null)
            {
                body.linearVelocity = Vector2.zero;
                return;
            }

            Vector2 delta = (Vector2)target.position - (Vector2)transform.position;

            if (delta.magnitude <= arrivalDistance)
            {
                waypointIndex = (waypointIndex + 1) % waypoints.Length;
                return;
            }

            body.linearVelocity = delta.normalized * patrolSpeed;
        }

        public void Stun(float duration)
        {
            if (State == EnemyState.Stunned)
            {
                stunTimer = Mathf.Max(stunTimer, duration);
                return;
            }

            stunTimer = duration > 0f ? duration : stunDuration;
            SetState(EnemyState.Stunned);

            if (body != null)
            {
                body.linearVelocity = Vector2.zero;
            }
        }

        private void SetState(EnemyState next)
        {
            State = next;

            switch (next)
            {
                case EnemyState.Stunned:
                    ApplyTint(stunnedTint);
                    break;
                default:
                    ApplyTint(patrolTint);
                    if (auraLight != null)
                    {
                        auraLight.intensity = auraBaseIntensity;
                    }
                    break;
            }
        }

        private void ApplyTint(Color tint)
        {
            if (spriteRenderer != null)
            {
                spriteRenderer.color = tint;
            }
        }

        private void OnTriggerStay2D(Collider2D other)
        {
            TryDamage(other);
        }

        private void OnCollisionStay2D(Collision2D collision)
        {
            TryDamage(collision.collider);
        }

        private void TryDamage(Collider2D other)
        {
            if (other == null || State == EnemyState.Stunned)
            {
                return;
            }

            if (!other.CompareTag("Player"))
            {
                return;
            }

            PlayerController target = other.GetComponent<PlayerController>();

            if (target == null)
            {
                target = other.GetComponentInParent<PlayerController>();
            }

            if (target == null)
            {
                target = player;
            }

            if (target != null)
            {
                target.TakeDamage(1);
            }
        }

        private void OnDrawGizmosSelected()
        {
            Gizmos.color = new Color(0.42f, 0.176f, 0.361f, 0.8f);
            Gizmos.DrawWireSphere(transform.position, detectRadius);
            Gizmos.color = new Color(0.392f, 0.784f, 1f, 0.5f);
            Gizmos.DrawWireSphere(transform.position, loseRadius);
        }
    }
}
