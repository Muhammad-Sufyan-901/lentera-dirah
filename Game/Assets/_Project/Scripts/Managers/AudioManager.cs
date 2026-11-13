using UnityEngine;

namespace LenteraDirah
{
    public class AudioManager : MonoBehaviour
    {
        public enum Sfx
        {
            Lontar,
            Burst,
            Oil,
            Hurt,
            Victory
        }

        public static AudioManager Instance { get; private set; }

        [Header("Audio Clip")]
        [SerializeField] private AudioClip bgmClip;
        [SerializeField] private AudioClip sfxLontar;
        [SerializeField] private AudioClip sfxBurst;
        [SerializeField] private AudioClip sfxOil;
        [SerializeField] private AudioClip sfxHurt;
        [SerializeField] private AudioClip sfxVictory;

        [Header("Pengaturan")]
        [Range(0f, 1f)] [SerializeField] private float bgmVolume = 0.35f;
        [Range(0f, 1f)] [SerializeField] private float sfxVolume = 0.85f;

        private AudioSource bgmSource;
        private AudioSource sfxSource;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;

            bgmSource = gameObject.AddComponent<AudioSource>();
            bgmSource.loop = true;
            bgmSource.playOnAwake = false;
            bgmSource.volume = bgmVolume;
            bgmSource.clip = bgmClip;

            sfxSource = gameObject.AddComponent<AudioSource>();
            sfxSource.loop = false;
            sfxSource.playOnAwake = false;
            sfxSource.volume = sfxVolume;
        }

        public void PlayBgm()
        {
            if (bgmSource == null || bgmClip == null || bgmSource.isPlaying)
            {
                return;
            }

            bgmSource.clip = bgmClip;
            bgmSource.volume = bgmVolume;
            bgmSource.Play();
        }

        public void PlaySfx(Sfx sfx)
        {
            AudioClip clip = GetClip(sfx);
            if (clip == null || sfxSource == null)
            {
                return;
            }

            sfxSource.PlayOneShot(clip, sfxVolume);
        }

        private AudioClip GetClip(Sfx sfx)
        {
            switch (sfx)
            {
                case Sfx.Lontar: return sfxLontar;
                case Sfx.Burst: return sfxBurst;
                case Sfx.Oil: return sfxOil;
                case Sfx.Hurt: return sfxHurt;
                case Sfx.Victory: return sfxVictory;
                default: return null;
            }
        }
    }
}
