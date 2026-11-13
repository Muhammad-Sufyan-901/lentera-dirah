using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEditor.Animations;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine.SceneManagement;
using UnityEngine.Tilemaps;
using UnityEngine.UI;

namespace LenteraDirah.Editor
{
    public static class LenteraDirahSceneBuilder
    {
        private const int MapWidth = 44;
        private const int MapHeight = 32;

        private const int FloorColumn = 11;
        private const int FloorRow = 6;
        private const int WallColumn = 1;
        private const int WallRow = 3;
        private const int AltarColumn = 7;
        private const int AltarRow = 2;

        private static readonly Color Midnight = new Color32(0x12, 0x13, 0x24, 0xFF);
        private static readonly Color Gold = new Color32(0xFF, 0xB8, 0x4D, 0xFF);
        private static readonly Color Violet = new Color32(0x6B, 0x2D, 0x5C, 0xFF);
        private static readonly Color Cyan = new Color32(0x64, 0xC8, 0xFF, 0xFF);
        private static readonly Color NightBackground = new Color32(0x06, 0x07, 0x0F, 0xFF);

        private static Font uiFont;
        private static readonly HashSet<string> savedPrefabs = new HashSet<string>();

        private sealed class HudRefs
        {
            public GameObject Panel;
            public Image EnergyFill;
            public Text EnergyText;
            public Text LontarText;
            public Text HintText;
            public Image[] Hearts;
        }

        private sealed class UiRefs
        {
            public GameObject MainMenu;
            public GameObject HowToPlay;
            public GameObject Dialog;
            public GameObject Hud;
            public GameObject Victory;
            public GameObject GameOver;
            public Text DialogText;
            public Text VictoryText;
            public Text GameOverText;
            public Button StartButton;
            public Button HowToPlayButton;
            public Button HowToPlayCloseButton;
            public Button QuitButton;
            public Button DialogButton;
            public Button VictoryButton;
            public Button GameOverButton;
            public Image EnergyFill;
            public Text EnergyText;
            public Text LontarText;
            public Text HintText;
            public Image[] Hearts;
        }

        [MenuItem("Tools/Lentera Dirah/1. Configure Pixel Art Assets & Tags", priority = 1)]
        public static void ConfigureAssetsMenu()
        {
            ProjectConfigurator.ConfigureAll();
        }

        [MenuItem("Tools/Lentera Dirah/2. Build Complete Prototype Scene", priority = 2)]
        public static void BuildSceneMenu()
        {
            BuildPrototypeScene();
        }

        [MenuItem("Tools/Lentera Dirah/3. Build macOS App", priority = 3)]
        public static void BuildMacMenu()
        {
            BuildMacApp();
        }

        [MenuItem("Tools/Lentera Dirah/Run Full Setup (1 then 2)", priority = 4)]
        public static void RunFullSetup()
        {
            ProjectConfigurator.ConfigureAll();
            BuildPrototypeScene();
        }

        public static void BuildPrototypeScene()
        {
            if (!ProjectConfigurator.IsConfigured)
            {
                Debug.Log("[LenteraDirah] Aset belum dikonfigurasi. Menjalankan konfigurasi otomatis...");
                ProjectConfigurator.ConfigureAll();
            }

            ProjectConfigurator.EnsureFolders();
            ProjectConfigurator.EnsureTagsAndLayers();
            ProjectConfigurator.EnsureUrpPipeline();

            Material litMaterial = ProjectConfigurator.EnsureLitMaterial();

            Scene scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            bool[,] open = BuildLayout();

            GameObject root = new GameObject("_LenteraDirah");

            CreateGlobalLight(root.transform);
            CreateTilemaps(root.transform, open, litMaterial);
            CreateBalineseProps(root.transform, litMaterial);
            GameObject player = CreatePlayer(root.transform, litMaterial);
            CreateEnemies(root.transform, litMaterial);
            CreateCollectibles(root.transform, litMaterial);
            CreateAltar(root.transform, litMaterial);
            CreateCamera(player.transform);

            CreateManagers(out GameManager gameManager, out AudioManager audioManager, out UIManager uiManager);
            UiRefs uiRefs = CreateUserInterface();

            PlayerController playerController = player.GetComponent<PlayerController>();

            Bind(gameManager, "player", playerController);
            Bind(gameManager, "uiManager", uiManager);
            Bind(gameManager, "audioManager", audioManager);

            BindAudio(audioManager);

            Bind(uiManager, "mainMenuPanel", uiRefs.MainMenu);
            Bind(uiManager, "howToPlayPanel", uiRefs.HowToPlay);
            Bind(uiManager, "dialogPanel", uiRefs.Dialog);
            Bind(uiManager, "hudPanel", uiRefs.Hud);
            Bind(uiManager, "victoryPanel", uiRefs.Victory);
            Bind(uiManager, "gameOverPanel", uiRefs.GameOver);

            Bind(uiManager, "energyFill", uiRefs.EnergyFill);
            Bind(uiManager, "energyText", uiRefs.EnergyText);
            Bind(uiManager, "lontarText", uiRefs.LontarText);
            Bind(uiManager, "hintText", uiRefs.HintText);
            BindArray(uiManager, "hearts", uiRefs.Hearts);
            Bind(uiManager, "dialogText", uiRefs.DialogText);
            Bind(uiManager, "victoryText", uiRefs.VictoryText);
            Bind(uiManager, "gameOverText", uiRefs.GameOverText);
            Bind(uiManager, "startButton", uiRefs.StartButton);
            Bind(uiManager, "howToPlayButton", uiRefs.HowToPlayButton);
            Bind(uiManager, "howToPlayCloseButton", uiRefs.HowToPlayCloseButton);
            Bind(uiManager, "quitButton", uiRefs.QuitButton);
            Bind(uiManager, "dialogButton", uiRefs.DialogButton);
            Bind(uiManager, "victoryButton", uiRefs.VictoryButton);
            Bind(uiManager, "gameOverButton", uiRefs.GameOverButton);

            ProjectConfigurator.EnsureFolder(ProjectConfigurator.ProjectRoot + "/Scenes");

            EditorSceneManager.MarkSceneDirty(scene);
            bool saved = EditorSceneManager.SaveScene(scene, ProjectConfigurator.ScenePath);

            EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(ProjectConfigurator.ScenePath, true) };

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            SceneAsset sceneAsset = AssetDatabase.LoadAssetAtPath<SceneAsset>(ProjectConfigurator.ScenePath);
            Selection.activeObject = sceneAsset;
            EditorGUIUtility.PingObject(sceneAsset);

            Debug.Log($"[LenteraDirah] Scene prototipe dibuat ({saved}): {ProjectConfigurator.ScenePath}");
        }

        private static bool[,] BuildLayout()
        {
            bool[,] open = new bool[MapWidth, MapHeight];

            CarveRect(open, 16, 12, 12, 10);
            CarveRect(open, 21, 21, 2, 4);
            CarveRect(open, 18, 25, 8, 5);
            CarveRect(open, 12, 16, 4, 2);
            CarveRect(open, 4, 14, 9, 7);
            CarveRect(open, 27, 16, 4, 2);
            CarveRect(open, 31, 14, 9, 7);
            CarveRect(open, 21, 10, 2, 2);
            CarveRect(open, 19, 5, 4, 6);

            return open;
        }

        private static void CarveRect(bool[,] open, int startX, int startY, int width, int height)
        {
            for (int y = startY; y < startY + height; y++)
            {
                for (int x = startX; x < startX + width; x++)
                {
                    if (x >= 0 && x < MapWidth && y >= 0 && y < MapHeight)
                    {
                        open[x, y] = true;
                    }
                }
            }
        }

        private static bool IsOpen(bool[,] open, int x, int y)
        {
            return x >= 0 && x < MapWidth && y >= 0 && y < MapHeight && open[x, y];
        }

        private static bool TouchesOpenTile(bool[,] open, int x, int y)
        {
            for (int offsetY = -1; offsetY <= 1; offsetY++)
            {
                for (int offsetX = -1; offsetX <= 1; offsetX++)
                {
                    if (IsOpen(open, x + offsetX, y + offsetY))
                    {
                        return true;
                    }
                }
            }

            return false;
        }

        private static void CreateGlobalLight(Transform parent)
        {
            GameObject lightObject = new GameObject("Global Light 2D");
            lightObject.transform.SetParent(parent, false);

            Light2D light = lightObject.AddComponent<Light2D>();
            light.lightType = Light2D.LightType.Global;
            light.color = Midnight;
            light.intensity = 0.08f;
            light.blendStyleIndex = 0;
        }

        private static void CreateTilemaps(Transform parent, bool[,] open, Material litMaterial)
        {
            int[,] floorCells = { { 11, 6 }, { 13, 6 }, { 18, 6 }, { 19, 6 } };
            Tile[] floorTiles = new Tile[floorCells.GetLength(0)];

            for (int i = 0; i < floorTiles.Length; i++)
            {
                Sprite sprite = ProjectConfigurator.GetSprite(ProjectConfigurator.ArtRoot + "/Tilesets/TilesetFloor.png", floorCells[i, 0], floorCells[i, 1]);
                floorTiles[i] = CreateTileAsset($"Tile_Floor_{i}", sprite, Tile.ColliderType.None);
            }

            Sprite wallSprite = ProjectConfigurator.GetSprite(ProjectConfigurator.ArtRoot + "/Tilesets/TilesetNature.png", WallColumn, WallRow);
            Tile wallTile = CreateTileAsset("Tile_Wall", wallSprite, Tile.ColliderType.Grid);

            GameObject gridObject = new GameObject("Grid", typeof(Grid));
            gridObject.transform.SetParent(parent, false);
            Grid grid = gridObject.GetComponent<Grid>();
            grid.cellSize = new Vector3(1f, 1f, 0f);

            Tilemap ground = CreateTilemap(gridObject.transform, "Tilemap_Ground", 0, false, litMaterial);
            Tilemap walls = CreateTilemap(gridObject.transform, "Tilemap_Walls", 1, true, litMaterial);

            walls.gameObject.tag = "Obstacle";
            int obstacleLayer = LayerMask.NameToLayer("Obstacle");
            if (obstacleLayer >= 0)
            {
                walls.gameObject.layer = obstacleLayer;
            }

            for (int y = 0; y < MapHeight; y++)
            {
                for (int x = 0; x < MapWidth; x++)
                {
                    Vector3Int cell = new Vector3Int(x, y, 0);
                    ground.SetTile(cell, floorTiles[(x * 7 + y * 13) & 3]);

                    if (!IsOpen(open, x, y) && TouchesOpenTile(open, x, y))
                    {
                        walls.SetTile(cell, wallTile);
                    }
                }
            }

            ground.color = new Color(0.82f, 0.88f, 0.95f, 1f);
        }

        private static Tilemap CreateTilemap(Transform parent, string name, int sortingOrder, bool withCollider, Material litMaterial)
        {
            GameObject tilemapObject = new GameObject(name, typeof(Tilemap), typeof(TilemapRenderer));
            tilemapObject.transform.SetParent(parent, false);

            TilemapRenderer renderer = tilemapObject.GetComponent<TilemapRenderer>();
            renderer.sortingOrder = sortingOrder;
            renderer.sharedMaterial = litMaterial;

            if (withCollider)
            {
                tilemapObject.AddComponent<TilemapCollider2D>();
            }

            Tilemap tilemap = tilemapObject.GetComponent<Tilemap>();
            tilemap.color = Color.white;
            tilemap.tileAnchor = new Vector3(0.5f, 0.5f, 0f);

            return tilemap;
        }

        private static Tile CreateTileAsset(string name, Sprite sprite, Tile.ColliderType colliderType)
        {
            string path = ProjectConfigurator.ArtRoot + "/Tilesets/" + name + ".asset";
            Tile tile = AssetDatabase.LoadAssetAtPath<Tile>(path);

            if (tile == null)
            {
                tile = ScriptableObject.CreateInstance<Tile>();
                AssetDatabase.CreateAsset(tile, path);
            }

            tile.sprite = sprite;
            tile.color = Color.white;
            tile.colliderType = colliderType;
            EditorUtility.SetDirty(tile);

            return tile;
        }

        private static void CreateBalineseProps(Transform parent, Material litMaterial)
        {
            GameObject props = new GameObject("BalineseProps");
            props.transform.SetParent(parent, false);

            CreateGapura(props.transform, litMaterial, "GapuraKeluar", new Vector3(21.5f, 9f, 0f), 0.85f);
            CreateGapura(props.transform, litMaterial, "GapuraUtara", new Vector3(21.5f, 24.2f, 0f), 0.85f);

            CreateBeringin(props.transform, litMaterial, "Beringin_Plaza_BaratDaya", new Vector3(17.5f, 14.5f, 0f), true);
            CreateBeringin(props.transform, litMaterial, "Beringin_Plaza_TimurDaya", new Vector3(26.5f, 14.5f, 0f), true);
            CreateBeringin(props.transform, litMaterial, "Beringin_Plaza_BaratLaut", new Vector3(17.5f, 20.5f, 0f), true);
            CreateBeringin(props.transform, litMaterial, "Beringin_Plaza_TimurLaut", new Vector3(26.5f, 20.5f, 0f), true);
            CreateBeringin(props.transform, litMaterial, "Beringin_SektorBarat", new Vector3(4.8f, 19.5f, 0f), true);
            CreateBeringin(props.transform, litMaterial, "Beringin_SektorTimur", new Vector3(38.2f, 19.5f, 0f), true);
            CreateBeringin(props.transform, litMaterial, "Beringin_SektorUtara", new Vector3(19.2f, 28.5f, 0f), false);

            CreateMeru(props.transform, litMaterial, "PuraMeru_SektorBarat", new Vector3(7.5f, 18f, 0f));
            CreateMeru(props.transform, litMaterial, "PuraMeru_SektorTimur", new Vector3(35.5f, 18f, 0f));

            CreateBaleKulkul(props.transform, litMaterial, "BaleKulkul_AlunAlun", new Vector3(25.5f, 18.5f, 0f));
            CreateBaleKulkul(props.transform, litMaterial, "BaleKulkul_SektorUtara", new Vector3(23f, 28.7f, 0f));

            CreatePelinggih(props.transform, litMaterial, "Pelinggih_BaratDaya", new Vector3(16.9f, 13.6f, 0f));
            CreatePelinggih(props.transform, litMaterial, "Pelinggih_TimurDaya", new Vector3(27.1f, 13.6f, 0f));
            CreatePelinggih(props.transform, litMaterial, "Pelinggih_BaratLaut", new Vector3(16.9f, 20.4f, 0f));
            CreatePelinggih(props.transform, litMaterial, "Pelinggih_TimurLaut", new Vector3(27.1f, 20.4f, 0f));

            Vector2[] penjorPositions =
            {
                new Vector2(16.7f, 16.5f), new Vector2(27.3f, 16.5f),
                new Vector2(20f, 13.2f), new Vector2(23.5f, 13.2f),
                new Vector2(20f, 21.3f), new Vector2(23.5f, 21.3f)
            };

            for (int i = 0; i < penjorPositions.Length; i++)
            {
                CreateEnvironmentProp(props.transform, litMaterial, $"Penjor_{i + 1}", "Penjor.png",
                    new Vector3(penjorPositions[i].x, penjorPositions[i].y, 0f), 10, 1f);
            }
        }

        private static void CreateGapura(Transform parent, Material material, string name, Vector3 position, float scale)
        {
            GameObject gate = CreateEnvironmentProp(parent, material, name, "Gapura_CandiBentar.png", position, 9, scale);

            AddBoxCollider(gate, new Vector2(-1.9f, -1.3f), new Vector2(1.7f, 2.4f));
            AddBoxCollider(gate, new Vector2(1.9f, -1.3f), new Vector2(1.7f, 2.4f));

            GameObject lightObject = new GameObject("GapuraLight");
            lightObject.transform.SetParent(gate.transform, false);
            lightObject.transform.localPosition = new Vector3(0f, 2.1f, 0f);

            Light2D light = lightObject.AddComponent<Light2D>();
            light.lightType = Light2D.LightType.Point;
            light.color = Gold;
            light.intensity = 0.8f;
            light.pointLightOuterRadius = 3.2f;
            light.pointLightInnerRadius = 0.3f;
        }

        private static void CreateBeringin(Transform parent, Material material, string name, Vector3 position, bool large)
        {
            string spriteFile = large ? "PohonBeringin_Besar.png" : "PohonBeringin_Kecil.png";
            GameObject tree = CreateEnvironmentProp(parent, material, name, spriteFile, position, 11, 1f);

            AddCircleCollider(tree, new Vector2(0f, large ? -2.1f : -1.6f), large ? 0.45f : 0.35f);
        }

        private static void CreateMeru(Transform parent, Material material, string name, Vector3 position)
        {
            GameObject meru = CreateEnvironmentProp(parent, material, name, "PuraMeru.png", position, 11, 1f);
            AddBoxCollider(meru, new Vector2(0f, -2.1f), new Vector2(1.4f, 1.8f));
        }

        private static void CreateBaleKulkul(Transform parent, Material material, string name, Vector3 position)
        {
            GameObject bale = CreateEnvironmentProp(parent, material, name, "BaleKulkul.png", position, 11, 1f);
            AddBoxCollider(bale, new Vector2(0f, -1f), new Vector2(1.6f, 1f));
        }

        private static void CreatePelinggih(Transform parent, Material material, string name, Vector3 position)
        {
            GameObject shrine = CreateEnvironmentProp(parent, material, name, "Pelinggih.png", position, 10, 1f);
            AddBoxCollider(shrine, new Vector2(0f, -0.7f), new Vector2(0.8f, 0.6f));
        }

        private static GameObject CreateEnvironmentProp(Transform parent, Material material, string name, string spriteFile,
            Vector3 position, int sortingOrder, float scale)
        {
            GameObject prop = new GameObject(name);
            prop.transform.SetParent(parent, false);
            prop.transform.position = position;
            prop.transform.localScale = Vector3.one * scale;

            SpriteRenderer renderer = prop.AddComponent<SpriteRenderer>();
            renderer.sprite = ProjectConfigurator.GetSpriteByIndex(ProjectConfigurator.ArtRoot + "/Environment/" + spriteFile, 0);
            renderer.sortingOrder = sortingOrder;
            renderer.sharedMaterial = material;

            return prop;
        }

        private static void AddBoxCollider(GameObject target, Vector2 offset, Vector2 size)
        {
            BoxCollider2D collider = target.AddComponent<BoxCollider2D>();
            collider.offset = offset;
            collider.size = size;
        }

        private static void AddCircleCollider(GameObject target, Vector2 offset, float radius)
        {
            CircleCollider2D collider = target.AddComponent<CircleCollider2D>();
            collider.offset = offset;
            collider.radius = radius;
        }

        private static GameObject CreatePlayer(Transform parent, Material litMaterial)
        {
            GameObject player = new GameObject("Player (Bahula)");
            player.transform.SetParent(parent, false);
            player.transform.position = new Vector3(21f, 7f, 0f);
            player.tag = "Player";

            int playerLayer = LayerMask.NameToLayer("Player");
            if (playerLayer >= 0)
            {
                player.layer = playerLayer;
            }

            SpriteRenderer renderer = player.AddComponent<SpriteRenderer>();
            renderer.sprite = ProjectConfigurator.GetSprite(ProjectConfigurator.BahulaSheet, 0, 0);
            renderer.sortingOrder = 10;
            renderer.sharedMaterial = litMaterial;

            Rigidbody2D body = player.AddComponent<Rigidbody2D>();
            body.bodyType = RigidbodyType2D.Dynamic;
            body.gravityScale = 0f;
            body.constraints = RigidbodyConstraints2D.FreezeRotation;
            body.interpolation = RigidbodyInterpolation2D.Interpolate;
            body.collisionDetectionMode = CollisionDetectionMode2D.Continuous;

            CircleCollider2D collider = player.AddComponent<CircleCollider2D>();
            collider.radius = 0.32f;
            collider.offset = new Vector2(0f, -0.08f);

            Animator animator = player.AddComponent<Animator>();
            animator.runtimeAnimatorController = AssetDatabase.LoadAssetAtPath<AnimatorController>(ProjectConfigurator.BahulaControllerPath);

            GameObject lanternObject = new GameObject("LanternLight");
            lanternObject.transform.SetParent(player.transform, false);
            lanternObject.transform.localPosition = Vector3.zero;

            Light2D lantern = lanternObject.AddComponent<Light2D>();
            lantern.lightType = Light2D.LightType.Point;
            lantern.color = Gold;
            lantern.intensity = 1.4f;
            lantern.pointLightOuterRadius = 6f;
            lantern.pointLightInnerRadius = 0.8f;
            lantern.pointLightInnerAngle = 360f;
            lantern.pointLightOuterAngle = 360f;

            PlayerController controller = player.AddComponent<PlayerController>();

            Bind(controller, "lanternLight", lantern);
            Bind(controller, "spriteRenderer", renderer);
            Bind(controller, "animator", animator);
            BindLayerMask(controller, "enemyMask", LayerMask.GetMask("Enemy"));

            return player;
        }

        private static void CreateEnemies(Transform parent, Material litMaterial)
        {
            AnimatorController spiritController = AssetDatabase.LoadAssetAtPath<AnimatorController>(ProjectConfigurator.SpiritControllerPath);
            PlayerController player = UnityEngine.Object.FindAnyObjectByType<PlayerController>();

            CreateEnemy(parent, litMaterial, spiritController, player, "EnemyBayangan_Utara", new Vector3(22f, 23f, 0f),
                new[] { new Vector3(22f, 22f, 0f), new Vector3(22f, 28f, 0f), new Vector3(20f, 28f, 0f) });

            CreateEnemy(parent, litMaterial, spiritController, player, "EnemyBayangan_Barat", new Vector3(14f, 17f, 0f),
                new[] { new Vector3(13f, 17f, 0f), new Vector3(6f, 17f, 0f), new Vector3(6f, 20f, 0f) });

            CreateEnemy(parent, litMaterial, spiritController, player, "EnemyBayangan_Timur", new Vector3(29f, 17f, 0f),
                new[] { new Vector3(30f, 17f, 0f), new Vector3(37f, 17f, 0f), new Vector3(37f, 20f, 0f) });
        }

        private static void CreateEnemy(Transform parent, Material litMaterial, AnimatorController controller, PlayerController player,
            string name, Vector3 position, Vector3[] waypointPositions)
        {
            GameObject enemy = new GameObject(name);
            enemy.transform.SetParent(parent, false);
            enemy.transform.position = position;
            enemy.tag = "Enemy";

            int enemyLayer = LayerMask.NameToLayer("Enemy");
            if (enemyLayer >= 0)
            {
                enemy.layer = enemyLayer;
            }

            SpriteRenderer renderer = enemy.AddComponent<SpriteRenderer>();
            renderer.sprite = ProjectConfigurator.GetSprite(ProjectConfigurator.SpiritSheet, 0, 0);
            renderer.sortingOrder = 9;
            renderer.sharedMaterial = litMaterial;
            renderer.color = Violet;

            Rigidbody2D body = enemy.AddComponent<Rigidbody2D>();
            body.bodyType = RigidbodyType2D.Dynamic;
            body.gravityScale = 0f;
            body.constraints = RigidbodyConstraints2D.FreezeRotation;
            body.interpolation = RigidbodyInterpolation2D.Interpolate;
            body.collisionDetectionMode = CollisionDetectionMode2D.Continuous;

            CircleCollider2D solid = enemy.AddComponent<CircleCollider2D>();
            solid.radius = 0.28f;

            CircleCollider2D hitZone = enemy.AddComponent<CircleCollider2D>();
            hitZone.radius = 0.45f;
            hitZone.isTrigger = true;

            if (controller != null)
            {
                Animator animator = enemy.AddComponent<Animator>();
                animator.runtimeAnimatorController = controller;
            }

            GameObject auraObject = new GameObject("AuraWabah");
            auraObject.transform.SetParent(enemy.transform, false);
            auraObject.transform.localPosition = Vector3.zero;

            Light2D aura = auraObject.AddComponent<Light2D>();
            aura.lightType = Light2D.LightType.Point;
            aura.color = Violet;
            aura.intensity = 0.55f;
            aura.pointLightOuterRadius = 2.2f;
            aura.pointLightInnerRadius = 0.2f;

            GameObject waypointRoot = new GameObject(name + "_Waypoints");
            waypointRoot.transform.SetParent(parent, false);

            List<Transform> waypoints = new List<Transform>();

            for (int i = 0; i < waypointPositions.Length; i++)
            {
                GameObject waypoint = new GameObject($"Waypoint_{i}");
                waypoint.transform.SetParent(waypointRoot.transform, false);
                waypoint.transform.position = waypointPositions[i];
                waypoints.Add(waypoint.transform);
            }

            EnemyShadowAI ai = enemy.AddComponent<EnemyShadowAI>();

            Bind(ai, "spriteRenderer", renderer);
            Bind(ai, "auraLight", aura);
            Bind(ai, "player", player);
            BindArray(ai, "waypoints", waypoints.ToArray());
        }

        private static void CreateCollectibles(Transform parent, Material litMaterial)
        {
            CreateCollectible(parent, litMaterial, "LontarSuci_Usada", CollectibleType.Lontar, new Vector3(21f, 27f, 0f),
                "Lontar Usada", "Lontar Usada: ilmu pengobatan suci yang menyembuhkan tanpa melukai.");

            CreateCollectible(parent, litMaterial, "LontarSuci_Dharma", CollectibleType.Lontar, new Vector3(6f, 16f, 0f),
                "Lontar Dharma", "Lontar Dharma: kebenaran dan kewajiban, dijaga melalui perbuatan baik.");

            CreateCollectible(parent, litMaterial, "LontarSuci_RwaBhineda", CollectibleType.Lontar, new Vector3(37f, 16f, 0f),
                "Lontar Rwa Bhineda", "Lontar Rwa Bhineda: terang dan gelap selalu hidup berdampingan, saling menyeimbangkan.");

            CreateCollectible(parent, litMaterial, "MinyakObor_Utara", CollectibleType.Oil, new Vector3(24f, 27f, 0f), null, null);
            CreateCollectible(parent, litMaterial, "MinyakObor_Barat", CollectibleType.Oil, new Vector3(10f, 16f, 0f), null, null);
            CreateCollectible(parent, litMaterial, "MinyakObor_Timur", CollectibleType.Oil, new Vector3(33f, 16f, 0f), null, null);
        }

        private static void CreateCollectible(Transform parent, Material litMaterial, string name, CollectibleType type,
            Vector3 position, string lontarName, string wisdomQuote)
        {
            GameObject item = new GameObject(name);
            item.transform.SetParent(parent, false);
            item.transform.position = position;

            SpriteRenderer renderer = item.AddComponent<SpriteRenderer>();
            renderer.sortingOrder = 8;
            renderer.sharedMaterial = litMaterial;

            if (type == CollectibleType.Lontar)
            {
                renderer.sprite = ProjectConfigurator.GetSpriteByIndex(ProjectConfigurator.ArtRoot + "/Items/Lontar.png", 0);
            }
            else
            {
                renderer.sprite = ProjectConfigurator.GetSpriteByIndex(ProjectConfigurator.ArtRoot + "/Items/OilJar.png", 0);
                item.transform.localScale = Vector3.one * 1.6f;
            }

            CircleCollider2D collider = item.AddComponent<CircleCollider2D>();
            collider.radius = 0.45f;
            collider.isTrigger = true;

            GameObject glowObject = new GameObject("Glow");
            glowObject.transform.SetParent(item.transform, false);
            glowObject.transform.localPosition = Vector3.zero;

            Light2D glow = glowObject.AddComponent<Light2D>();
            glow.lightType = Light2D.LightType.Point;
            glow.color = Gold;
            glow.intensity = 0.9f;
            glow.pointLightOuterRadius = 2.4f;
            glow.pointLightInnerRadius = 0.1f;

            CollectibleItem collectible = item.AddComponent<CollectibleItem>();

            BindEnum(collectible, "itemType", (int)type);

            if (!string.IsNullOrEmpty(lontarName))
            {
                BindString(collectible, "lontarName", lontarName);
            }

            if (!string.IsNullOrEmpty(wisdomQuote))
            {
                BindString(collectible, "wisdomQuote", wisdomQuote);
            }

            Bind(collectible, "glowLight", glow);

            if (type == CollectibleType.Lontar)
            {
                SavePrefabCopy(item, "LontarSuci");
            }
            else
            {
                SavePrefabCopy(item, "MinyakObor");
            }
        }

        private static void CreateAltar(Transform parent, Material litMaterial)
        {
            GameObject altar = new GameObject("AltarPenyucian");
            altar.transform.SetParent(parent, false);
            altar.transform.position = new Vector3(22f, 17f, 0f);
            altar.transform.localScale = Vector3.one * 2.2f;

            SpriteRenderer renderer = altar.AddComponent<SpriteRenderer>();
            renderer.sprite = ProjectConfigurator.GetSprite(ProjectConfigurator.ArtRoot + "/Tilesets/TilesetElement.png", AltarColumn, AltarRow);
            renderer.sortingOrder = 5;
            renderer.sharedMaterial = litMaterial;

            BoxCollider2D trigger = altar.AddComponent<BoxCollider2D>();
            trigger.size = new Vector2(0.7f, 0.7f);
            trigger.offset = new Vector2(0f, -0.2f);
            trigger.isTrigger = true;

            GameObject lightObject = new GameObject("AltarLight");
            lightObject.transform.SetParent(altar.transform, false);
            lightObject.transform.localPosition = Vector3.zero;

            Light2D altarLight = lightObject.AddComponent<Light2D>();
            altarLight.lightType = Light2D.LightType.Point;
            altarLight.color = Gold;
            altarLight.intensity = 0.25f;
            altarLight.pointLightOuterRadius = 3.6f;
            altarLight.pointLightInnerRadius = 0.4f;

            AltarPurification altarPurification = altar.AddComponent<AltarPurification>();

            Bind(altarPurification, "altarLight", altarLight);
            Bind(altarPurification, "spriteRenderer", renderer);

            SavePrefabCopy(altar, "AltarPenyucian");
        }

        private static void CreateCamera(Transform target)
        {
            GameObject cameraObject = new GameObject("Main Camera", typeof(Camera));
            cameraObject.tag = "MainCamera";
            cameraObject.transform.position = new Vector3(21f, 8f, -10f);

            Camera camera = cameraObject.GetComponent<Camera>();
            camera.orthographic = true;
            camera.orthographicSize = 8f;
            camera.clearFlags = CameraClearFlags.SolidColor;
            camera.backgroundColor = NightBackground;
            camera.nearClipPlane = 0.1f;
            camera.farClipPlane = 100f;

            cameraObject.AddComponent<AudioListener>();

            if (cameraObject.GetComponent<UniversalAdditionalCameraData>() == null)
            {
                cameraObject.AddComponent<UniversalAdditionalCameraData>();
            }

            CameraFollow2D follow = cameraObject.AddComponent<CameraFollow2D>();
            Bind(follow, "target", target);

            float halfHeight = camera.orthographicSize;
            float halfWidth = halfHeight * (16f / 9f);

            follow.SetBounds(
                new Vector2(halfWidth, halfHeight),
                new Vector2(MapWidth - halfWidth, MapHeight - halfHeight));
        }

        private static void CreateManagers(out GameManager gameManager, out AudioManager audioManager, out UIManager uiManager)
        {
            GameObject managers = new GameObject("_Managers");

            gameManager = managers.AddComponent<GameManager>();
            audioManager = managers.AddComponent<AudioManager>();
            uiManager = managers.AddComponent<UIManager>();
        }

        private static void BindAudio(AudioManager audioManager)
        {
            Bind(audioManager, "bgmClip", AssetDatabase.LoadAssetAtPath<AudioClip>(ProjectConfigurator.ProjectRoot + "/Audio/BGM/bgm_gamelan_girah.ogg"));
            Bind(audioManager, "sfxLontar", AssetDatabase.LoadAssetAtPath<AudioClip>(ProjectConfigurator.ProjectRoot + "/Audio/SFX/pickup_lontar.wav"));
            Bind(audioManager, "sfxBurst", AssetDatabase.LoadAssetAtPath<AudioClip>(ProjectConfigurator.ProjectRoot + "/Audio/SFX/light_burst.wav"));
            Bind(audioManager, "sfxOil", AssetDatabase.LoadAssetAtPath<AudioClip>(ProjectConfigurator.ProjectRoot + "/Audio/SFX/pickup_oil.wav"));
            Bind(audioManager, "sfxHurt", AssetDatabase.LoadAssetAtPath<AudioClip>(ProjectConfigurator.ProjectRoot + "/Audio/SFX/hurt.wav"));
            Bind(audioManager, "sfxVictory", AssetDatabase.LoadAssetAtPath<AudioClip>(ProjectConfigurator.ProjectRoot + "/Audio/SFX/victory.wav"));
        }

        private static UiRefs CreateUserInterface()
        {
            uiFont = LoadFont();

            UiRefs refs = new UiRefs();

            GameObject canvasObject = new GameObject("Canvas UI", typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
            Canvas canvas = canvasObject.GetComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;

            CanvasScaler scaler = canvasObject.GetComponent<CanvasScaler>();
            scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = new Vector2(1920f, 1080f);
            scaler.matchWidthOrHeight = 0.5f;

            new GameObject("EventSystem", typeof(EventSystem), typeof(StandaloneInputModule));

            Sprite panelSprite = ProjectConfigurator.GetSpriteByIndex(ProjectConfigurator.ArtRoot + "/UI/PanelBox.png", 0);
            Sprite dialogSprite = ProjectConfigurator.GetSpriteByIndex(ProjectConfigurator.ArtRoot + "/UI/DialogBox.png", 0);
            Sprite heartSprite = ProjectConfigurator.GetSprite(ProjectConfigurator.ArtRoot + "/UI/Heart.png", 0, 0);
            Sprite mpuPortrait = ProjectConfigurator.GetSpriteByIndex(ProjectConfigurator.ArtRoot + "/Characters/MpuBharada_Faceset.png", 0);

            HudRefs hud = CreateHud(canvas.transform, panelSprite, heartSprite);

            refs.Hud = hud.Panel;
            refs.EnergyFill = hud.EnergyFill;
            refs.EnergyText = hud.EnergyText;
            refs.LontarText = hud.LontarText;
            refs.HintText = hud.HintText;
            refs.Hearts = hud.Hearts;

            refs.MainMenu = CreateMainMenu(canvas.transform, panelSprite, dialogSprite, out Button startButton, out Button howToPlayButton, out Button quitButton);
            refs.StartButton = startButton;
            refs.HowToPlayButton = howToPlayButton;
            refs.QuitButton = quitButton;

            refs.HowToPlay = CreateHowToPlay(canvas.transform, panelSprite, dialogSprite, out Button howToPlayCloseButton);
            refs.HowToPlayCloseButton = howToPlayCloseButton;

            refs.Dialog = CreateDialog(canvas.transform, panelSprite, dialogSprite, mpuPortrait, out Text dialogText, out Button dialogButton);
            refs.DialogText = dialogText;
            refs.DialogButton = dialogButton;

            refs.Victory = CreateEndScreen(canvas.transform, panelSprite, dialogSprite, "Victory_Panel", "DESA GIRAH PULIH", Gold,
                out Text victoryText, out Button victoryButton, "MAIN LAGI");
            refs.VictoryText = victoryText;
            refs.VictoryButton = victoryButton;

            refs.GameOver = CreateEndScreen(canvas.transform, panelSprite, dialogSprite, "GameOver_Panel", "KEGELAPAN MENYELIMUTI",
                new Color(0.85f, 0.35f, 0.42f), out Text gameOverText, out Button gameOverButton, "COBA LAGI");
            refs.GameOverText = gameOverText;
            refs.GameOverButton = gameOverButton;

            refs.Dialog.SetActive(false);
            refs.Victory.SetActive(false);
            refs.GameOver.SetActive(false);
            refs.Hud.SetActive(false);
            refs.HowToPlay.SetActive(false);

            return refs;
        }

        private static HudRefs CreateHud(Transform canvas, Sprite panelSprite, Sprite heartSprite)
        {
            HudRefs refs = new HudRefs();
            RectTransform hud = Stretch(NewRect("HUD_Panel", canvas));
            refs.Panel = hud.gameObject;

            RectTransform title = Place(NewRect("TitleHUD", hud), new Vector2(0.5f, 1f), new Vector2(0.5f, 1f), new Vector2(0f, -26f), new Vector2(800f, 44f));
            AddText(title, "LENTERA DIRAH", 30, Gold, TextAnchor.MiddleCenter);

            refs.Hearts = new Image[3];

            for (int i = 0; i < 3; i++)
            {
                RectTransform heart = Place(NewRect($"Heart_{i + 1}", hud), new Vector2(0f, 1f), new Vector2(0f, 1f),
                    new Vector2(26f + i * 46f, -30f), new Vector2(40f, 40f));
                refs.Hearts[i] = AddImage(heart, heartSprite, Color.white, false);
                refs.Hearts[i].preserveAspect = true;
            }

            RectTransform energyBar = Place(NewRect("EnergyBar", hud), new Vector2(0f, 1f), new Vector2(0f, 1f),
                new Vector2(26f, -96f), new Vector2(430f, 36f));
            AddImage(energyBar, panelSprite, new Color(0.06f, 0.06f, 0.12f, 0.92f), true);

            RectTransform fill = Stretch(NewRect("EnergyFill", energyBar));
            fill.offsetMin = new Vector2(3f, 3f);
            fill.offsetMax = new Vector2(-3f, -3f);
            refs.EnergyFill = AddImage(fill, panelSprite, Gold, false);
            refs.EnergyFill.type = Image.Type.Filled;
            refs.EnergyFill.fillMethod = Image.FillMethod.Horizontal;
            refs.EnergyFill.fillOrigin = 0;
            refs.EnergyFill.fillAmount = 1f;

            RectTransform energyLabel = Stretch(NewRect("EnergyText", energyBar));
            refs.EnergyText = AddText(energyLabel, "ENERGI LENTERA: 100%", 20, Color.white, TextAnchor.MiddleCenter);
            AddOutline(refs.EnergyText, new Color(0f, 0f, 0f, 0.9f));

            RectTransform lontar = Place(NewRect("LontarCounter", hud), new Vector2(1f, 1f), new Vector2(1f, 1f),
                new Vector2(-26f, -30f), new Vector2(460f, 44f));
            refs.LontarText = AddText(lontar, "LONTAR SUCI: 0 / 3", 28, Gold, TextAnchor.MiddleRight);
            AddOutline(refs.LontarText, new Color(0f, 0f, 0f, 0.9f));

            RectTransform hint = Place(NewRect("HintText", hud), new Vector2(0.5f, 0f), new Vector2(0.5f, 0f),
                new Vector2(0f, 150f), new Vector2(1500f, 110f));
            refs.HintText = AddText(hint, string.Empty, 26, Gold, TextAnchor.MiddleCenter);
            AddOutline(refs.HintText, new Color(0f, 0f, 0f, 0.95f));

            RectTransform controls = Place(NewRect("Controls", hud), new Vector2(0f, 0f), new Vector2(0f, 0f),
                new Vector2(26f, 24f), new Vector2(1100f, 60f));
            AddText(controls, "[WASD / Panah] Bergerak    [SPACE] Pancaran Cahaya Suci    [E] Lanjut Dialog", 20,
                new Color(Gold.r, Gold.g, Gold.b, 0.8f), TextAnchor.LowerLeft);
            AddOutline(controls.GetComponent<Text>(), new Color(0f, 0f, 0f, 0.9f));

            return refs;
        }

        private static GameObject CreateMainMenu(Transform canvas, Sprite panelSprite, Sprite buttonSprite,
            out Button startButton, out Button howToPlayButton, out Button quitButton)
        {
            GameObject panel = CreateOverlay(canvas, "MainMenu_Panel", new Color(Midnight.r, Midnight.g, Midnight.b, 0.94f));

            Sprite gapuraBackdrop = ProjectConfigurator.GetSpriteByIndex(ProjectConfigurator.ArtRoot + "/Environment/Gapura_Menu.png", 0);
            Sprite beringinBackdrop = ProjectConfigurator.GetSpriteByIndex(ProjectConfigurator.ArtRoot + "/Environment/PohonBeringin_Besar.png", 0);
            Sprite penjorBackdrop = ProjectConfigurator.GetSpriteByIndex(ProjectConfigurator.ArtRoot + "/Environment/Penjor.png", 0);

            RectTransform backdrop = Stretch(NewRect("Backdrop", panel.transform));

            Image gateBackdrop = AddImage(
                Place(NewRect("GapuraBackdrop", backdrop), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                    new Vector2(0f, 25f), new Vector2(900f, 750f)),
                gapuraBackdrop, new Color(1f, 1f, 1f, 0.26f), false);
            gateBackdrop.preserveAspect = true;

            Image treeBackdropLeft = AddImage(
                Place(NewRect("BeringinBackdrop_Kiri", backdrop), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                    new Vector2(-700f, -40f), new Vector2(420f, 540f)),
                beringinBackdrop, new Color(0.05f, 0.055f, 0.1f, 0.96f), false);
            treeBackdropLeft.preserveAspect = true;

            Image treeBackdropRight = AddImage(
                Place(NewRect("BeringinBackdrop_Kanan", backdrop), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                    new Vector2(700f, -40f), new Vector2(420f, 540f)),
                beringinBackdrop, new Color(0.05f, 0.055f, 0.1f, 0.96f), false);
            treeBackdropRight.preserveAspect = true;

            AddImage(Place(NewRect("PenjorBackdrop_Kiri", backdrop), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                    new Vector2(-645f, -120f), new Vector2(150f, 600f)),
                penjorBackdrop, new Color(1f, 0.72f, 0.3f, 0.38f), false);

            AddImage(Place(NewRect("PenjorBackdrop_Kanan", backdrop), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                    new Vector2(645f, -120f), new Vector2(150f, 600f)),
                penjorBackdrop, new Color(1f, 0.72f, 0.3f, 0.38f), false);

            RectTransform box = Place(NewRect("MenuBox", panel.transform), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                new Vector2(0f, 0f), new Vector2(1120f, 720f));
            AddImage(box, panelSprite, new Color(0.09f, 0.09f, 0.17f, 0.88f), true);

            AddImage(Place(NewRect("Ornament_Atas", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                    new Vector2(0f, 298f), new Vector2(760f, 2f)),
                null, new Color(Gold.r, Gold.g, Gold.b, 0.55f), false);

            AddImage(Place(NewRect("Ornament_Bawah", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                    new Vector2(0f, 104f), new Vector2(760f, 2f)),
                null, new Color(Gold.r, Gold.g, Gold.b, 0.35f), false);

            RectTransform title = Place(NewRect("Title", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                new Vector2(0f, 230f), new Vector2(1000f, 120f));
            AddText(title, "LENTERA DIRAH", 86, Gold, TextAnchor.MiddleCenter);

            RectTransform subtitle = Place(NewRect("Subtitle", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                new Vector2(0f, 140f), new Vector2(1000f, 60f));
            AddText(subtitle, "Lontar Mpu Bharada", 40, new Color(0.86f, 0.86f, 0.95f), TextAnchor.MiddleCenter);

            RectTransform body = Place(NewRect("Body", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                new Vector2(0f, 20f), new Vector2(900f, 150f));
            AddText(body,
                "Kabut wabah dari Setra Gandamayu menyelimuti Desa Girah. Jelajahi kegelapan sebagai Bahula, " +
                "tenangkan Bayangan Wabah dengan cahaya lentera, lalu kembalikan 3 Lontar Suci ke Altar Penyucian.",
                24, new Color(0.88f, 0.85f, 0.8f), TextAnchor.MiddleCenter);

            RectTransform footnote = Place(NewRect("Footnote", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                new Vector2(0f, -282f), new Vector2(900f, 40f));
            AddText(footnote, "Rwa Bhineda — terang dan gelap saling menyeimbangkan", 20, new Color(0.64f, 0.784f, 1f), TextAnchor.MiddleCenter);

            startButton = CreateButton(box, "StartButton", "MULAI PENYUCIAN", buttonSprite, new Vector2(0f, -110f), new Vector2(480f, 84f));
            howToPlayButton = CreateButton(box, "HowToPlayButton", "CARA BERMAIN", buttonSprite, new Vector2(-168f, -206f), new Vector2(320f, 62f));
            quitButton = CreateButton(box, "QuitButton", "KELUAR", buttonSprite, new Vector2(170f, -206f), new Vector2(300f, 62f));

            return panel;
        }

        private static GameObject CreateHowToPlay(Transform canvas, Sprite panelSprite, Sprite buttonSprite, out Button closeButton)
        {
            GameObject panel = CreateOverlay(canvas, "HowToPlay_Panel", new Color(0.02f, 0.02f, 0.04f, 0.93f));

            RectTransform box = Place(NewRect("HowToPlayBox", panel.transform), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                Vector2.zero, new Vector2(1100f, 800f));
            AddImage(box, panelSprite, new Color(0.09f, 0.09f, 0.17f, 0.985f), true);

            RectTransform title = Place(NewRect("HowToPlayTitle", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                new Vector2(0f, 332f), new Vector2(900f, 80f));
            AddText(title, "CARA BERMAIN", 52, Gold, TextAnchor.MiddleCenter);

            AddImage(Place(NewRect("HowToPlayOrnament", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                    new Vector2(0f, 284f), new Vector2(820f, 2f)),
                null, new Color(Gold.r, Gold.g, Gold.b, 0.55f), false);

            RectTransform body = Place(NewRect("HowToPlayBody", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                new Vector2(0f, -8f), new Vector2(940f, 560f));
            Text bodyText = AddText(body,
                "<b>TUJUAN</b>\n" +
                "Kumpulkan 3 Lontar Suci (Usada, Dharma, Rwa Bhineda) di sektor utara, barat, dan timur desa, " +
                "lalu sentuh Altar Penyucian di tengah desa.\n\n" +
                "<b>KONTROL</b>\n" +
                "[WASD / Panah]  Bergerak 4 arah\n" +
                "[SPACE]  Holy Light Burst — membekukan Bayangan Wabah di sekitar selama 3 detik\n" +
                "[E] atau klik tombol  — melanjutkan dialog\n\n" +
                "<b>ENERGI LENTERA</b>\n" +
                "Energi menyusut 2% per detik dan radius cahaya ikut mengecil. Ambil Minyak Obor untuk menambah " +
                "+35% energi. Bila energi habis, permainan berakhir.\n\n" +
                "<b>BAYANGAN WABAH</b>\n" +
                "Hindari patrolinya. Burst memakai 15% energi (cooldown 4 detik, radius 3.5 unit). Tersentuh musuh " +
                "mengurangi 1 nyawa; kamu kebal 1 detik setelahnya.\n\n" +
                "<b>TIPS</b>\n" +
                "Amati pola patroli sebelum mengambil Lontar, dan simpan energi untuk situasi terjepit.",
                20, new Color(0.92f, 0.9f, 0.86f), TextAnchor.UpperLeft);
            bodyText.lineSpacing = 1.15f;

            closeButton = CreateButton(box, "HowToPlayCloseButton", "KEMBALI", buttonSprite, new Vector2(0f, -336f), new Vector2(300f, 62f));

            return panel;
        }

        private static GameObject CreateDialog(Transform canvas, Sprite frameSprite, Sprite buttonSprite, Sprite portrait, out Text dialogText, out Button dialogButton)
        {
            GameObject panel = CreateOverlay(canvas, "Dialog_Panel", new Color(0.03f, 0.03f, 0.06f, 0.55f));

            RectTransform frame = NewRect("DialogFrame", panel.transform);
            frame.anchorMin = new Vector2(0f, 0f);
            frame.anchorMax = new Vector2(1f, 0f);
            frame.pivot = new Vector2(0.5f, 0f);
            frame.offsetMin = new Vector2(90f, 50f);
            frame.offsetMax = new Vector2(-90f, 360f);
            AddImage(frame, frameSprite, new Color(0.1f, 0.09f, 0.16f, 0.98f), true);

            RectTransform portraitRect = Place(NewRect("MpuBharada_Portrait", frame), new Vector2(0f, 0.5f), new Vector2(0f, 0.5f),
                new Vector2(28f, 0f), new Vector2(210f, 210f));
            Image portraitImage = AddImage(portraitRect, portrait, Color.white, false);
            portraitImage.preserveAspect = true;

            RectTransform name = Place(NewRect("SpeakerName", frame), new Vector2(0f, 1f), new Vector2(0f, 1f),
                new Vector2(262f, -24f), new Vector2(700f, 46f));
            AddText(name, "MPU BHARADA", 30, Gold, TextAnchor.MiddleLeft);

            RectTransform body = Place(NewRect("DialogText", frame), new Vector2(0f, 1f), new Vector2(0f, 1f),
                new Vector2(262f, -74f), new Vector2(1420f, 190f));
            dialogText = AddText(body, string.Empty, 24, new Color(0.94f, 0.92f, 0.88f), TextAnchor.UpperLeft);

            dialogButton = CreateButton(frame, "DialogButton", "MENGERTI (E)", buttonSprite, new Vector2(-190f, 52f), new Vector2(320f, 62f));
            RectTransform buttonRect = dialogButton.GetComponent<RectTransform>();
            buttonRect.anchorMin = new Vector2(1f, 0f);
            buttonRect.anchorMax = new Vector2(1f, 0f);
            buttonRect.pivot = new Vector2(1f, 0f);
            buttonRect.anchoredPosition = new Vector2(-30f, 22f);

            return panel;
        }

        private static GameObject CreateEndScreen(Transform canvas, Sprite panelSprite, Sprite buttonSprite, string panelName, string heading, Color headingColor,
            out Text bodyText, out Button actionButton, string buttonLabel)
        {
            GameObject panel = CreateOverlay(canvas, panelName, new Color(0.03f, 0.03f, 0.06f, 0.9f));

            RectTransform box = Place(NewRect("Box", panel.transform), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                Vector2.zero, new Vector2(1000f, 620f));
            AddImage(box, panelSprite, new Color(0.09f, 0.09f, 0.17f, 0.97f), true);

            RectTransform title = Place(NewRect("Heading", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                new Vector2(0f, 200f), new Vector2(900f, 90f));
            AddText(title, heading, 62, headingColor, TextAnchor.MiddleCenter);

            RectTransform body = Place(NewRect("Body", box), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f),
                new Vector2(0f, 30f), new Vector2(840f, 240f));
            bodyText = AddText(body, string.Empty, 26, new Color(0.9f, 0.88f, 0.84f), TextAnchor.MiddleCenter);

            actionButton = CreateButton(box, "ActionButton", buttonLabel, buttonSprite, new Vector2(0f, -210f), new Vector2(360f, 78f));

            return panel;
        }

        private static Button CreateButton(Transform parent, string name, string label, Sprite sprite, Vector2 position, Vector2 size)
        {
            RectTransform rect = Place(NewRect(name, parent), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), position, size);
            Image image = AddImage(rect, sprite, Gold, true);
            image.raycastTarget = true;

            Button button = rect.gameObject.AddComponent<Button>();
            button.targetGraphic = image;

            ColorBlock colors = button.colors;
            colors.normalColor = Color.white;
            colors.highlightedColor = new Color(1f, 0.94f, 0.8f, 1f);
            colors.pressedColor = new Color(0.82f, 0.68f, 0.45f, 1f);
            colors.selectedColor = new Color(1f, 0.94f, 0.8f, 1f);
            button.colors = colors;

            RectTransform labelRect = Stretch(NewRect("Label", rect));
            Text labelText = AddText(labelRect, label, 28, new Color(0.07f, 0.07f, 0.14f), TextAnchor.MiddleCenter);
            labelText.fontStyle = FontStyle.Bold;

            return button;
        }

        private static GameObject CreateOverlay(Transform canvas, string name, Color color)
        {
            RectTransform rect = Stretch(NewRect(name, canvas));
            Image image = AddImage(rect, null, color, false);
            image.raycastTarget = true;
            return rect.gameObject;
        }

        private static RectTransform NewRect(string name, Transform parent)
        {
            GameObject gameObject = new GameObject(name, typeof(RectTransform));
            RectTransform rect = (RectTransform)gameObject.transform;
            rect.SetParent(parent, false);
            return rect;
        }

        private static RectTransform Stretch(RectTransform rect)
        {
            rect.anchorMin = Vector2.zero;
            rect.anchorMax = Vector2.one;
            rect.offsetMin = Vector2.zero;
            rect.offsetMax = Vector2.zero;
            return rect;
        }

        private static RectTransform Place(RectTransform rect, Vector2 anchor, Vector2 pivot, Vector2 position, Vector2 size)
        {
            rect.anchorMin = anchor;
            rect.anchorMax = anchor;
            rect.pivot = pivot;
            rect.anchoredPosition = position;
            rect.sizeDelta = size;
            return rect;
        }

        private static Image AddImage(RectTransform rect, Sprite sprite, Color color, bool sliced)
        {
            Image image = rect.gameObject.AddComponent<Image>();
            image.sprite = sprite;
            image.color = color;
            image.raycastTarget = false;

            if (sliced && sprite != null && sprite.border != Vector4.zero)
            {
                image.type = Image.Type.Sliced;
            }

            return image;
        }

        private static Text AddText(RectTransform rect, string content, int size, Color color, TextAnchor anchor)
        {
            Text text = rect.gameObject.AddComponent<Text>();
            text.font = uiFont;
            text.text = content;
            text.fontSize = size;
            text.color = color;
            text.alignment = anchor;
            text.horizontalOverflow = HorizontalWrapMode.Wrap;
            text.verticalOverflow = VerticalWrapMode.Overflow;
            text.raycastTarget = false;
            return text;
        }

        private static void AddOutline(Text text, Color color)
        {
            Outline outline = text.gameObject.AddComponent<Outline>();
            outline.effectColor = color;
            outline.effectDistance = new Vector2(1.5f, -1.5f);
        }

        private static Font LoadFont()
        {
            Font font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");

            if (font == null)
            {
                font = AssetDatabase.LoadAssetAtPath<Font>(ProjectConfigurator.ArtRoot + "/UI/NormalFont.ttf");
            }

            if (font == null)
            {
                font = Font.CreateDynamicFontFromOSFont("Arial", 24);
            }

            return font;
        }

        private static void SavePrefabCopy(GameObject source, string prefabName)
        {
            string path = ProjectConfigurator.ProjectRoot + "/Prefabs/" + prefabName + ".prefab";
            ProjectConfigurator.EnsureFolder(ProjectConfigurator.ProjectRoot + "/Prefabs");

            if (savedPrefabs.Contains(prefabName))
            {
                return;
            }

            try
            {
                PrefabUtility.SaveAsPrefabAsset(source, path);
                savedPrefabs.Add(prefabName);
            }
            catch (Exception exception)
            {
                Debug.LogWarning($"[LenteraDirah] Gagal membuat prefab {prefabName}: {exception.Message}");
            }
        }

        private static void Bind(UnityEngine.Object target, string fieldName, UnityEngine.Object value, bool required = true)
        {
            if (target == null)
            {
                return;
            }

            SerializedObject serialized = new SerializedObject(target);
            SerializedProperty property = serialized.FindProperty(fieldName);

            if (property == null)
            {
                if (required)
                {
                    Debug.LogError($"[LenteraDirah] Field '{fieldName}' tidak ditemukan pada {target.GetType().Name}.");
                }

                return;
            }

            property.objectReferenceValue = value;
            serialized.ApplyModifiedPropertiesWithoutUndo();

            if (required && value == null)
            {
                Debug.LogWarning($"[LenteraDirah] Referensi '{fieldName}' pada {target.GetType().Name} bernilai kosong.");
            }
        }

        private static void BindArray(UnityEngine.Object target, string fieldName, UnityEngine.Object[] values)
        {
            SerializedObject serialized = new SerializedObject(target);
            SerializedProperty property = serialized.FindProperty(fieldName);

            if (property == null || !property.isArray)
            {
                Debug.LogError($"[LenteraDirah] Array field '{fieldName}' tidak ditemukan pada {target.GetType().Name}.");
                return;
            }

            property.arraySize = values.Length;

            for (int i = 0; i < values.Length; i++)
            {
                property.GetArrayElementAtIndex(i).objectReferenceValue = values[i];
            }

            serialized.ApplyModifiedPropertiesWithoutUndo();
        }

        private static void BindString(UnityEngine.Object target, string fieldName, string value)
        {
            SerializedObject serialized = new SerializedObject(target);
            SerializedProperty property = serialized.FindProperty(fieldName);

            if (property == null)
            {
                Debug.LogError($"[LenteraDirah] Field '{fieldName}' tidak ditemukan pada {target.GetType().Name}.");
                return;
            }

            property.stringValue = value;
            serialized.ApplyModifiedPropertiesWithoutUndo();
        }

        private static void BindEnum(UnityEngine.Object target, string fieldName, int enumIndex)
        {
            SerializedObject serialized = new SerializedObject(target);
            SerializedProperty property = serialized.FindProperty(fieldName);

            if (property == null)
            {
                Debug.LogError($"[LenteraDirah] Field '{fieldName}' tidak ditemukan pada {target.GetType().Name}.");
                return;
            }

            property.enumValueIndex = enumIndex;
            serialized.ApplyModifiedPropertiesWithoutUndo();
        }

        private static void BindLayerMask(UnityEngine.Object target, string fieldName, LayerMask mask)
        {
            SerializedObject serialized = new SerializedObject(target);
            SerializedProperty property = serialized.FindProperty(fieldName);

            if (property == null)
            {
                Debug.LogError($"[LenteraDirah] Field '{fieldName}' tidak ditemukan pada {target.GetType().Name}.");
                return;
            }

            property.intValue = mask.value;
            serialized.ApplyModifiedPropertiesWithoutUndo();
        }

        public static void BuildMacApp()
        {
            if (!File.Exists(ProjectConfigurator.ScenePath))
            {
                BuildPrototypeScene();
            }

            string buildDirectory = Path.GetFullPath(Path.Combine(Application.dataPath, "../Builds/macOS"));
            Directory.CreateDirectory(buildDirectory);

            BuildPlayerOptions options = new BuildPlayerOptions
            {
                scenes = new[] { ProjectConfigurator.ScenePath },
                locationPathName = Path.Combine(buildDirectory, "LenteraDirah.app"),
                target = BuildTarget.StandaloneOSX,
                options = BuildOptions.None
            };

            BuildReport report = BuildPipeline.BuildPlayer(options);

            if (report.summary.result == BuildResult.Succeeded)
            {
                Debug.Log($"[LenteraDirah] Build macOS berhasil: {options.locationPathName} ({report.summary.totalSize / (1024 * 1024)} MB)");
            }
            else
            {
                Debug.LogError($"[LenteraDirah] Build macOS gagal: {report.summary.result}. Cek Build Settings atau lisensi Unity.");
            }
        }
    }
}
