using UnityEngine;

namespace LenteraDirah
{
    public class CameraFollow2D : MonoBehaviour
    {
        [SerializeField] private Transform target;
        [SerializeField] private float smoothTime = 0.15f;
        [SerializeField] private Vector2 offset = Vector2.zero;
        [SerializeField] private bool clampToBounds;
        [SerializeField] private Vector2 minBounds = new Vector2(-100f, -100f);
        [SerializeField] private Vector2 maxBounds = new Vector2(100f, 100f);

        private Vector3 velocity;

        private void LateUpdate()
        {
            if (target == null)
            {
                return;
            }

            Vector3 desired = new Vector3(target.position.x + offset.x, target.position.y + offset.y, transform.position.z);

            if (clampToBounds)
            {
                desired.x = Mathf.Clamp(desired.x, minBounds.x, maxBounds.x);
                desired.y = Mathf.Clamp(desired.y, minBounds.y, maxBounds.y);
            }

            transform.position = Vector3.SmoothDamp(transform.position, desired, ref velocity, smoothTime);
        }

        public void SetBounds(Vector2 min, Vector2 max)
        {
            clampToBounds = true;
            minBounds = min;
            maxBounds = max;
        }
    }
}
