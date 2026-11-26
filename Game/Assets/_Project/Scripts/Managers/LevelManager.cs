using UnityEngine;

namespace LenteraDirah
{
    /// <summary>Mengaktifkan satu level dalam scene dan mengatur posisi pemain/kamera.</summary>
    public class LevelManager : MonoBehaviour
    {
        [SerializeField] private LevelController[] levels;
        [SerializeField] private PlayerController player;
        [SerializeField] private CameraFollow2D cameraFollow;

        public int LevelCount => levels != null ? levels.Length : 0;
        public LevelController Current { get; private set; }

        public string CurrentLevelName => Current != null ? Current.LevelName : "Desa Girah";
        public string CurrentObjective => Current != null ? Current.Objective : string.Empty;

        private void Awake()
        {
            if (levels != null && levels.Length > 0)
            {
                Current = levels[0];
            }
        }

        public void LoadLevel(int number)
        {
            if (levels == null || levels.Length == 0)
            {
                return;
            }

            int index = Mathf.Clamp(number - 1, 0, levels.Length - 1);

            foreach (LevelController level in levels)
            {
                if (level != null)
                {
                    level.gameObject.SetActive(false);
                }
            }

            Current = levels[index];
            Current.gameObject.SetActive(true);
            Current.Prepare();

            if (player != null)
            {
                player.ResetForLevel(Current.SpawnPosition);
            }

            if (cameraFollow != null)
            {
                cameraFollow.SnapToTarget();
            }
        }
    }
}
