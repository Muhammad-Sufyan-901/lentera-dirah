using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Animations;
using UnityEngine;
using UnityEngine.Rendering;

namespace LenteraDirah.Editor
{
    public static class ProjectConfigurator
    {
        public const string ProjectRoot = "Assets/_Project";
        public const string ArtRoot = ProjectRoot + "/Art";
        public const string AnimRoot = ProjectRoot + "/Art/Animations";
        public const string MaterialPath = ProjectRoot + "/Art/Materials/SpriteLit.mat";
        public const string BahulaSheet = ArtRoot + "/Characters/Bahula_SpriteSheet.png";
        public const string SpiritSheet = ArtRoot + "/Monsters/ShadowSpirit_SpriteSheet.png";
        public const string BahulaControllerPath = AnimRoot + "/Bahula.controller";
        public const string SpiritControllerPath = AnimRoot + "/ShadowSpirit.controller";
        public const string ScenePath = ProjectRoot + "/Scenes/LenteraDirah_Girah.unity";

        public const int PlayerLayer = 8;
        public const int EnemyLayer = 9;
        public const int ObstacleLayer = 10;

        private const int SheetTileSize = 16;

        public static bool IsConfigured =>
            AssetDatabase.LoadAssetAtPath<AnimatorController>(BahulaControllerPath) != null &&
            AssetDatabase.LoadAssetAtPath<Material>(MaterialPath) != null &&
            GetSprites(BahulaSheet).Length >= 16;

        public static void ConfigureAll()
        {
            EnsureFolders();
            EnsureTagsAndLayers();
            EnsureUrpPipeline();
            ConfigureTextures();
            EnsureLitMaterial();
            BuildAnimations();

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            Debug.Log("[LenteraDirah] Konfigurasi selesai: tag, layer, impor pixel-art (PPU 16 / Point), material lit, dan animasi 4 arah.");
        }

        public static void EnsureFolders()
        {
            string[] folders =
            {
                ProjectRoot,
                ArtRoot,
                ArtRoot + "/Characters",
                ArtRoot + "/Monsters",
                ArtRoot + "/Items",
                ArtRoot + "/Tilesets",
                ArtRoot + "/Environment",
                ArtRoot + "/UI",
                ArtRoot + "/Animations",
                ArtRoot + "/Materials",
                ProjectRoot + "/Audio/BGM",
                ProjectRoot + "/Audio/SFX",
                ProjectRoot + "/Prefabs",
                ProjectRoot + "/Scenes"
            };

            foreach (string folder in folders)
            {
                EnsureFolder(folder);
            }
        }

        public static void EnsureTagsAndLayers()
        {
            UnityEngine.Object[] assets = AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/TagManager.asset");

            if (assets.Length == 0)
            {
                Debug.LogWarning("[LenteraDirah] TagManager.asset tidak ditemukan.");
                return;
            }

            SerializedObject tagManager = new SerializedObject(assets[0]);
            SerializedProperty tags = tagManager.FindProperty("tags");
            SerializedProperty layers = tagManager.FindProperty("layers");

            foreach (string tag in new[] { "Player", "Enemy", "Obstacle" })
            {
                bool exists = false;

                for (int i = 0; i < tags.arraySize; i++)
                {
                    if (tags.GetArrayElementAtIndex(i).stringValue == tag)
                    {
                        exists = true;
                        break;
                    }
                }

                if (!exists)
                {
                    tags.InsertArrayElementAtIndex(tags.arraySize);
                    tags.GetArrayElementAtIndex(tags.arraySize - 1).stringValue = tag;
                }
            }

            EnsureLayer(layers, PlayerLayer, "Player");
            EnsureLayer(layers, EnemyLayer, "Enemy");
            EnsureLayer(layers, ObstacleLayer, "Obstacle");

            tagManager.ApplyModifiedPropertiesWithoutUndo();
        }

        public static void EnsureUrpPipeline()
        {
            RenderPipelineAsset urp = AssetDatabase.LoadAssetAtPath<RenderPipelineAsset>("Assets/Settings/UniversalRP.asset");

            if (urp == null)
            {
                Debug.LogWarning("[LenteraDirah] UniversalRP.asset tidak ditemukan. Pastikan proyek memakai template URP 2D.");
                return;
            }

            GraphicsSettings.defaultRenderPipeline = urp;
            QualitySettings.renderPipeline = urp;
        }

        public static Material EnsureLitMaterial()
        {
            Material existing = AssetDatabase.LoadAssetAtPath<Material>(MaterialPath);

            if (existing != null)
            {
                return existing;
            }

            Shader shader = Shader.Find("Universal Render Pipeline/2D/Sprite-Lit-Default");

            if (shader == null)
            {
                shader = Shader.Find("Universal Render Pipeline/2D/Sprite-Unlit-Default");
            }

            if (shader == null)
            {
                shader = Shader.Find("Sprites/Default");
                Debug.LogWarning("[LenteraDirah] Shader Sprite-Lit-Default tidak ditemukan, memakai Sprites/Default.");
            }

            Material material = new Material(shader) { name = "SpriteLit" };
            EnsureFolder(ArtRoot + "/Materials");
            AssetDatabase.CreateAsset(material, MaterialPath);
            AssetDatabase.SaveAssets();

            return material;
        }

        private static void ConfigureTextures()
        {
            string[] guids = AssetDatabase.FindAssets("t:Texture2D", new[] { ArtRoot });

            foreach (string guid in guids)
            {
                string path = AssetDatabase.GUIDToAssetPath(guid);

                if (!path.EndsWith(".png", StringComparison.OrdinalIgnoreCase))
                {
                    continue;
                }

                TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;

                if (importer == null)
                {
                    continue;
                }

                string fileName = Path.GetFileNameWithoutExtension(path);

                importer.textureType = TextureImporterType.Sprite;
                importer.spritePixelsPerUnit = SheetTileSize;
                importer.filterMode = FilterMode.Point;
                importer.textureCompression = TextureImporterCompression.Uncompressed;
                importer.mipmapEnabled = false;
                importer.wrapMode = TextureWrapMode.Clamp;
                importer.alphaIsTransparency = true;
                importer.maxTextureSize = 2048;
                importer.spriteBorder = GetBorder(fileName);

                TextureImporterSettings settings = new TextureImporterSettings();
                importer.ReadTextureSettings(settings);
                settings.spriteMeshType = SpriteMeshType.FullRect;
                settings.spriteBorder = GetBorder(fileName);
                importer.SetTextureSettings(settings);

                bool isSheet = IsSpriteSheet(fileName);

                importer.spriteImportMode = isSheet ? SpriteImportMode.Multiple : SpriteImportMode.Single;

                if (isSheet)
                {
                    importer.spritesheet = BuildSpriteGrid(path, importer.spriteBorder);
                }
                else
                {
                    importer.spritesheet = Array.Empty<SpriteMetaData>();
                }

                importer.SaveAndReimport();
            }

            Debug.Log($"[LenteraDirah] {guids.Length} tekstur diimpor ulang sebagai pixel-art (PPU 16, Point, Uncompressed).");
        }

        private static bool IsSpriteSheet(string fileName)
        {
            return fileName.Contains("SpriteSheet") ||
                   fileName.Contains("IdleSheet") ||
                   fileName.StartsWith("Tileset", StringComparison.Ordinal) ||
                   fileName == "Heart";
        }

        private static Vector4 GetBorder(string fileName)
        {
            switch (fileName)
            {
                case "DialogBox": return new Vector4(6, 6, 6, 6);
                case "PanelBox": return new Vector4(5, 5, 5, 5);
                default: return Vector4.zero;
            }
        }

        private static SpriteMetaData[] BuildSpriteGrid(string assetPath, Vector4 border)
        {
            Vector2Int size = ReadPngSize(assetPath);

            if (size.x <= 0 || size.y <= 0)
            {
                return Array.Empty<SpriteMetaData>();
            }

            int columns = size.x / SheetTileSize;
            int rows = size.y / SheetTileSize;
            string baseName = Path.GetFileNameWithoutExtension(assetPath);
            List<SpriteMetaData> metas = new List<SpriteMetaData>(columns * rows);

            for (int row = 0; row < rows; row++)
            {
                for (int column = 0; column < columns; column++)
                {
                    metas.Add(new SpriteMetaData
                    {
                        name = $"{baseName}_{column}_{row}",
                        rect = new Rect(column * SheetTileSize, size.y - (row + 1) * SheetTileSize, SheetTileSize, SheetTileSize),
                        alignment = (int)SpriteAlignment.Center,
                        pivot = new Vector2(0.5f, 0.5f),
                        border = border
                    });
                }
            }

            return metas.ToArray();
        }

        private static Vector2Int ReadPngSize(string assetPath)
        {
            try
            {
                byte[] bytes = File.ReadAllBytes(Path.GetFullPath(assetPath));

                if (bytes.Length < 24)
                {
                    return Vector2Int.zero;
                }

                int width = (bytes[16] << 24) | (bytes[17] << 16) | (bytes[18] << 8) | bytes[19];
                int height = (bytes[20] << 24) | (bytes[21] << 16) | (bytes[22] << 8) | bytes[23];
                return new Vector2Int(width, height);
            }
            catch (Exception exception)
            {
                Debug.LogWarning($"[LenteraDirah] Gagal membaca ukuran PNG {assetPath}: {exception.Message}");
                return Vector2Int.zero;
            }
        }

        public static Sprite[] GetSprites(string assetPath)
        {
            return AssetDatabase.LoadAllAssetsAtPath(assetPath).OfType<Sprite>().ToArray();
        }

        public static Sprite GetSprite(string assetPath, int column, int row)
        {
            string baseName = Path.GetFileNameWithoutExtension(assetPath);
            string target = $"{baseName}_{column}_{row}";
            Sprite[] sprites = GetSprites(assetPath);

            foreach (Sprite sprite in sprites)
            {
                if (sprite.name == target)
                {
                    return sprite;
                }
            }

            Vector2Int size = ReadPngSize(assetPath);
            int columns = size.x > 0 ? Mathf.Max(1, size.x / SheetTileSize) : 4;
            int index = row * columns + column;
            return sprites.Length > 0 ? sprites[Mathf.Clamp(index, 0, sprites.Length - 1)] : null;
        }

        public static Sprite GetSpriteByIndex(string assetPath, int index)
        {
            Sprite[] sprites = GetSprites(assetPath);
            return sprites.Length == 0 ? null : sprites[Mathf.Clamp(index, 0, sprites.Length - 1)];
        }

        private static void BuildAnimations()
        {
            try
            {
                EnsureFolder(AnimRoot);
                BuildBahulaAnimations();
                BuildSpiritAnimations();
            }
            catch (Exception exception)
            {
                Debug.LogWarning($"[LenteraDirah] Animasi gagal dibuat (gameplay tetap berjalan tanpa animasi): {exception}");
            }
        }

        private static void BuildBahulaAnimations()
        {
            Sprite[] frames = new Sprite[4 * 4];

            for (int row = 0; row < 4; row++)
            {
                for (int column = 0; column < 4; column++)
                {
                    frames[row * 4 + column] = GetSprite(BahulaSheet, column, row);
                }
            }

            if (frames.Any(sprite => sprite == null))
            {
                Debug.LogWarning("[LenteraDirah] Sprite Bahula belum terpotong. Animasi dilewati.");
                return;
            }

            string[] directions = { "Down", "Up", "Left", "Right" };
            List<AnimationClip> walkClips = new List<AnimationClip>();
            List<AnimationClip> idleClips = new List<AnimationClip>();

            for (int row = 0; row < directions.Length; row++)
            {
                Sprite[] step = frames.Skip(row * 4).Take(4).ToArray();
                walkClips.Add(CreateAndSaveClip($"Walk_{directions[row]}", step, 8f, true));
                idleClips.Add(CreateAndSaveClip($"Idle_{directions[row]}", new[] { step[0] }, 1f, true));
            }

            if (AssetDatabase.LoadAssetAtPath<AnimatorController>(BahulaControllerPath) != null)
            {
                AssetDatabase.DeleteAsset(BahulaControllerPath);
            }

            AnimatorController controller = AnimatorController.CreateAnimatorControllerAtPath(BahulaControllerPath);
            List<AnimatorState> states = new List<AnimatorState>();

            foreach (AnimationClip clip in idleClips.Concat(walkClips))
            {
                states.Add(controller.AddMotion(clip));
            }

            controller.layers[0].stateMachine.defaultState = states[0];
            EditorUtility.SetDirty(controller);
            AssetDatabase.SaveAssets();
        }

        private static void BuildSpiritAnimations()
        {
            Sprite[] frames = new Sprite[4];

            for (int column = 0; column < 4; column++)
            {
                frames[column] = GetSprite(SpiritSheet, column, 0);
            }

            if (frames.Any(sprite => sprite == null))
            {
                Debug.LogWarning("[LenteraDirah] Sprite ShadowSpirit belum terpotong. Animasi dilewati.");
                return;
            }

            AnimationClip clip = CreateAndSaveClip("Float", frames, 6f, true);

            if (AssetDatabase.LoadAssetAtPath<AnimatorController>(SpiritControllerPath) != null)
            {
                AssetDatabase.DeleteAsset(SpiritControllerPath);
            }

            AnimatorController controller = AnimatorController.CreateAnimatorControllerAtPath(SpiritControllerPath);
            AnimatorState state = controller.AddMotion(clip);
            controller.layers[0].stateMachine.defaultState = state;
            EditorUtility.SetDirty(controller);
            AssetDatabase.SaveAssets();
        }

        private static AnimationClip CreateAndSaveClip(string clipName, Sprite[] frames, float fps, bool loop)
        {
            string path = $"{AnimRoot}/{clipName}.anim";
            AnimationClip existing = AssetDatabase.LoadAssetAtPath<AnimationClip>(path);

            if (existing != null)
            {
                AssetDatabase.DeleteAsset(path);
            }

            AnimationClip clip = new AnimationClip { frameRate = fps, name = clipName };
            AnimationClipSettings settings = AnimationUtility.GetAnimationClipSettings(clip);
            settings.loopTime = loop;
            AnimationUtility.SetAnimationClipSettings(clip, settings);

            EditorCurveBinding binding = new EditorCurveBinding
            {
                type = typeof(SpriteRenderer),
                path = string.Empty,
                propertyName = "m_Sprite"
            };

            ObjectReferenceKeyframe[] keys = new ObjectReferenceKeyframe[frames.Length];

            for (int i = 0; i < frames.Length; i++)
            {
                keys[i] = new ObjectReferenceKeyframe { time = i / fps, value = frames[i] };
            }

            AnimationUtility.SetObjectReferenceCurve(clip, binding, keys);
            AssetDatabase.CreateAsset(clip, path);

            return AssetDatabase.LoadAssetAtPath<AnimationClip>(path);
        }

        private static void EnsureLayer(SerializedProperty layers, int index, string layerName)
        {
            if (index < 0 || index >= layers.arraySize)
            {
                return;
            }

            SerializedProperty layer = layers.GetArrayElementAtIndex(index);

            if (string.IsNullOrEmpty(layer.stringValue))
            {
                layer.stringValue = layerName;
            }
        }

        public static void EnsureFolder(string folder)
        {
            if (AssetDatabase.IsValidFolder(folder))
            {
                return;
            }

            string parent = Path.GetDirectoryName(folder)?.Replace('\\', '/');
            string name = Path.GetFileName(folder);

            if (string.IsNullOrEmpty(parent))
            {
                return;
            }

            EnsureFolder(parent);
            AssetDatabase.CreateFolder(parent, name);
        }
    }
}
