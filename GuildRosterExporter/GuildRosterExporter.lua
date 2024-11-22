local frame = CreateFrame("Frame")

local function GetGuildRoster()
    local guildMembers = {}
    local numMembers = GetNumGuildMembers()

    if numMembers == 0 then
        print("No guild members found or you are not in a guild.")
        return
    end

    for i = 1, numMembers do
        local name, _, _, _, _, _, _, _, _, _ = GetGuildRosterInfo(i)
        if name then
            table.insert(guildMembers, name)
        end
    end

    GuildRosterExporterDB = GuildRosterExporterDB or {}
    GuildRosterExporterDB.members = guildMembers

    print("Guild Members Saved:")
    for _, name in ipairs(guildMembers) do
        print(name)
    end
end

SLASH_GREXPORT1 = "/grexport"
SlashCmdList["GREXPORT"] = function()
    if IsInGuild() then
        GetGuildRoster()
    else
        print("You are not in a guild.")
    end
end
