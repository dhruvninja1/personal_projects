using Celeste;
using Monocle;
using System;
using Microsoft.Xna.Framework;

namespace Celeste.Mod.CelesteMod
{
    public class CelesteModModule : EverestModule
    {
        public static CelesteModModule Instance { get; private set; }

        public override Type SettingsType => typeof(CelesteModModuleSettings);
        public static CelesteModModuleSettings Settings => (CelesteModModuleSettings)Instance._Settings;

        public override Type SessionType => typeof(CelesteModModuleSession);
        public static CelesteModModuleSession Session => (CelesteModModuleSession)Instance._Session;

        public override Type SaveDataType => typeof(CelesteModModuleSaveData);
        public static CelesteModModuleSaveData SaveData => (CelesteModModuleSaveData)Instance._SaveData;

        public CelesteModModule()
        {
            Instance = this;
#if DEBUG
            Logger.SetLogLevel(nameof(CelesteModModule), LogLevel.Verbose);
#else
            Logger.SetLogLevel(nameof(CelesteModModule), LogLevel.Info);
#endif
        }

        public override void Load()
        {
            On.Celeste.Player.Update += OnPlayerUpdate;
        }

        public override void Unload()
        {
            On.Celeste.Player.Update -= OnPlayerUpdate;
        }

        private void OnPlayerUpdate(On.Celeste.Player.orig_Update orig, Player self)
        {
            orig(self);

            // Access the current Level and Session.
            Level level = Engine.Scene as Level;

            if (level != null && level.Session != null)
            {
                // Get the current room name from the session.
                string roomName = level.Session.Level;

                // Get the current checkpoint's position from the session.
                Vector2? checkpoint = level.Session.RespawnPoint;

                Logger.Log(LogLevel.Info, "CelesteMod", $"Current Room: {roomName}, Last Checkpoint: {checkpoint}");
            }
        }
    }
}