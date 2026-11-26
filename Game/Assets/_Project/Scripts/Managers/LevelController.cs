using UnityEngine;

namespace LenteraDirah
{
    /// <summary>Satu akar level: tilemap, props, musuh, item, altar, dan titik spawn.</summary>
    public class LevelController : MonoBehaviour
    {
        [Header("Identitas Level")]
        [SerializeField] private int levelNumber = 1;
        [SerializeField] private string levelName = "Desa Girah";
        [TextArea(1, 3)]
        [SerializeField] private string objective = "Kumpulkan 3 Lontar Suci lalu sentuh Altar Penyucian.";

        [Header("Spawn")]
        [SerializeField] private Transform spawnPoint;

        private EnemyShadowAI[] enemies;
        private CollectibleItem[] collectibles;
        private AltarPurification altar;
        private Vector3[] enemySpawnPositions;

        public int LevelNumber => levelNumber;
        public string LevelName => levelName;
        public string Objective => objective;
        public Vector3 SpawnPosition => spawnPoint != null ? spawnPoint.position : transform.position;

        private void Awake()
        {
            CacheContent();
        }

        /// <summary>Aktifkan ulang seluruh isi level untuk dimainkan dari awal.</summary>
        public void Prepare()
        {
            CacheContent();

            foreach (CollectibleItem item in collectibles)
            {
                if (item != null)
                {
                    item.ResetItem();
                }
            }

            if (altar != null)
            {
                altar.ResetAltar();
            }

            for (int i = 0; i < enemies.Length; i++)
            {
                if (enemies[i] != null)
                {
                    enemies[i].ResetForLevel(enemySpawnPositions[i]);
                }
            }
        }

        private void CacheContent()
        {
            enemies = GetComponentsInChildren<EnemyShadowAI>(true);
            collectibles = GetComponentsInChildren<CollectibleItem>(true);
            altar = GetComponentInChildren<AltarPurification>(true);

            if (enemySpawnPositions == null || enemySpawnPositions.Length != enemies.Length)
            {
                enemySpawnPositions = new Vector3[enemies.Length];

                for (int i = 0; i < enemies.Length; i++)
                {
                    enemySpawnPositions[i] = enemies[i].transform.position;
                }
            }
        }
    }
}
